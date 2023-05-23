import pandas as pd
import random
import numpy as np
import holidays
import datetime
from st_aggrid import AgGrid
import streamlit as st


from generic_files.config import *


def prepare_dataframes(simulation_time,year_customers, hotel_obj,timesteps):

    customer_data =  {      'customer_id': [cus.id for cus in year_customers],
                            'segment' : [cus.segment for cus in year_customers],
                            'hotel_name':[cus.hotel_name for cus in year_customers],
                            'room_type':[cus.type for cus in year_customers],
                            'length_of_stay':[cus.stay_duration for cus in year_customers],
                            'attempts':[cus.attempts for cus in year_customers], 
                            'customer_perceived_price':[cus.room_value for cus in year_customers],
                            'hotel_price':[cus.actual_hotel_price for cus in year_customers], 
                            'search_day':[cus.initial_search_day for cus in year_customers], 
                            'booked_day':[cus.booked_day for cus in year_customers], 
                            'stay_day':[cus.stay_day for cus in year_customers],
                            'lead_time':[cus.actual_gap for cus in year_customers],
                            'remaining_days':[cus.remaining_days for cus in year_customers], 
                            'cancelled':[cus.booking_cancelled for cus in year_customers], 
                            'cancelled_day':[cus.cancelled_day for cus in year_customers],
                            'booking_status':[cus.booking_status for cus in year_customers]}

    customer_df = pd.DataFrame(customer_data)

    mydataframe = pd.DataFrame()
    for index in customer_df.index:
        if  (customer_df.cancelled[index]!=1) &(customer_df.hotel_name[index]==hotel_obj.name):
            new_row=customer_df.loc[index]
            for day in range(customer_df['stay_day'][index],customer_df['stay_day'][index] + customer_df['length_of_stay'][index] + 1):
                new_row['stay_day']=day   # increasing the initial stay_day within the stay duration                                                      
                mydataframe = pd.concat([mydataframe, new_row.to_frame().T], ignore_index=True)
    mydataframe['Profit']=0
    mydataframe['hotel_price'] = mydataframe.get('hotel_price', np.nan)
    mydataframe['room_type'] = mydataframe.get('room_type', np.nan)
    mydataframe['booking_status'] = mydataframe.get('booking_status', np.nan)
    mydataframe['stay_day'] = mydataframe.get('stay_day', [i for i in range(simulation_time+15)])
    name_room_profit_list=[]
    for i in room_type.keys():
        name_room_cost =i+'_cost'
        name_room_profit =i+'_profit'
        name_room_revenue =i+'_revenue'
        mydataframe[name_room_profit]=0
        mydataframe[name_room_profit][mydataframe.room_type==i] = mydataframe['hotel_price']-getattr(hotel_obj,name_room_cost)
        mydataframe['Profit']+=mydataframe[name_room_profit]
        mydataframe[name_room_revenue]=mydataframe['hotel_price'][mydataframe.room_type==i]
        name_room_profit_list.extend([name_room_profit,name_room_revenue])
    mydataframe=mydataframe[mydataframe['booking_status']=='Booking successful']
    Cust_grpby = mydataframe[['stay_day', 'hotel_price', 'Profit']+name_room_profit_list].groupby('stay_day').sum(numeric_only=False).reset_index()
    Cust_grpby.rename(columns={ 'hotel_price':'Daily_Revenue'},inplace=True)
    df = pd.DataFrame()
    df['stay_day'] = [i for i in range(simulation_time+15)] 
    df['no_of_rooms']=0
    df['total_no_of_booked_rooms']=0
    for i in room_type.keys():
        name_room_schedule=i+'_schedule'
        name_room_count=i+'_count'
        no_of_booked_name_room='no_of_booked_'+i
        name_room_occupancy=i+'_occupancy'
        df[name_room_schedule]=getattr(hotel_obj,name_room_schedule)
        df[name_room_count] = getattr(hotel_obj,name_room_count)
             
        df['no_of_rooms']+=  df[name_room_count]
        df[no_of_booked_name_room] = df[name_room_count] - df[name_room_schedule]
        df[name_room_occupancy]=df[no_of_booked_name_room]/df[name_room_count]*100
        df['total_no_of_booked_rooms']+=df[no_of_booked_name_room]
        df.drop([name_room_count,name_room_schedule,no_of_booked_name_room],axis='columns',inplace=True)
    df = pd.merge(df, Cust_grpby, on='stay_day', how='outer')

    df['Profit'] = df.get('Profit', 0)
    df['Daily_Revenue'] = df.get('Daily_Revenue', 0)
    df['Profit'] = df['Profit'].fillna(0)
    df['Profit'] =df['Profit'] -hotel_obj.daily_cost
    df.Daily_Revenue = df.Daily_Revenue.fillna(0)
    df['Occupancy_rate'] = df.total_no_of_booked_rooms/df.no_of_rooms*100
    df['Average_daily_rate'] = df.Daily_Revenue/df.total_no_of_booked_rooms

    metrics_df = df
    # making a dataframe for room price records
    price_record_cols = [type_of_room+'_price' for type_of_room in room_type]+ ['segment', 'booking_gap']
    hotel_room_price_records = pd.DataFrame( columns= price_record_cols)

    for day in range(simulation_time):
            for lead_day in lead_time_days:
                row_dict = {type_of_room+'_price' : hotel_obj.room_price_records[type_of_room][lead_day][day] for type_of_room in room_type}
                row_dict['booking_gap'] = lead_day
                row_dict['day'] = day
                row = pd.Series(row_dict)
                hotel_room_price_records = pd.concat([hotel_room_price_records, row.to_frame().T], ignore_index=True)


    booking_rec_df = pd.DataFrame({'Day' : timesteps, 
                                   'failed_Customers'  : hotel_obj.failed_customers, 
                                   'Booked_Customers'  : hotel_obj.booked_customers,})

    booking_rec_df['Search_day_count'] = booking_rec_df.failed_Customers + booking_rec_df.Booked_Customers
    booking_rec_df_melt = booking_rec_df[['Day', 'failed_Customers', 'Booked_Customers']].melt(id_vars='Day')

    booking_rec_df = booking_rec_df
    booking_rec_df_melt = booking_rec_df_melt

    multi_hotels_stat=multi_hotels_stats(customer_df)

    return [customer_df ,metrics_df,booking_rec_df,booking_rec_df_melt,multi_hotels_stat,hotel_room_price_records]

def summarize_metrics(hotel_obj,type_of_room,lead_day,time_step):
    conv_cust = hotel_obj.converted_customers[type_of_room][lead_day][time_step] 
    tot_cust = hotel_obj.total_customers[type_of_room][lead_day][time_step]
    room_price = getattr(hotel_obj, (type_of_room + '_price'))[lead_day]
    st_room_price = getattr(hotel_obj, (type_of_room + '_st_price'))
    room_cost = getattr(hotel_obj, (type_of_room + '_cost'))
    profit_per_room = (room_price - room_cost) if (room_price - room_cost)>0 else 0
    static_profit_per_room = st_room_price - room_cost

    expect_total_profit  = profit_per_room * conv_cust
    expected_conv_cust = conv_cust+2 if st_room_price<room_price else conv_cust-2
    static_expect_total_profit = static_profit_per_room * expected_conv_cust
    conversion = round(conv_cust/tot_cust,2) if tot_cust >0 else 0
    expected_ROI = round(profit_per_room/room_cost,2) if tot_cust >0 else 0

    return conv_cust, tot_cust, expect_total_profit, conversion, expected_ROI, room_price, room_cost, static_expect_total_profit


def multi_hotels_stats(customer_df):
    return customer_df[['hotel_name','customer_id']][customer_df.booking_status=='Booking successful'].groupby('hotel_name').count().reset_index().rename(columns={'customer_id':'no_of_customers'})

def comparison_df (rl_df,base_df):
    comparison_df=pd.DataFrame(columns=['Room_type', 'RL_agent_mean_occupancy_rate', 'Base_model_mean_occupancy_Rate',
                                      'RL_agent_mean_profit', 'Base_model_mean_profit', 
                                      'RL_agent_mean_revenue', 'Base_model_mean_revenue',
                                      ])
    for name_room in room_type:

        comparison_df.loc[len(comparison_df.index)] = [name_room, rl_df[1][name_room+'_occupancy'].mean(), base_df[1][name_room+'_occupancy'].mean(),
                                                    rl_df[1][name_room+'_profit'].mean(), base_df[1][name_room+'_profit'].mean(),
                                                        rl_df[1][name_room+'_revenue'].mean(), base_df[1][name_room+'_revenue'].mean()]
    comparison_df.loc[len(comparison_df.index)]=[ 'Total', rl_df[1]['Occupancy_rate'].mean(), base_df[1]['Occupancy_rate'].mean(),
                                                    rl_df[1]['Profit'].mean(), base_df[1]['Profit'].mean(),
                                                    rl_df[1]['Daily_Revenue'].mean(), base_df[1]['Daily_Revenue'].mean()]
    comparison_df.fillna(0, inplace=True)
    return comparison_df
def distribution_df(rl_df,base_df):
   
   rl_df[4].rename(columns={'no_of_customers':'customers_in_RL_hotel_env'},inplace=True)
   base_df[4].rename(columns={'no_of_customers':'customers_in_Static_hotel_env'},inplace=True)
   #merge customer distribution by hotel
   df = pd.merge(rl_df[4],base_df[4],on='hotel_name',how='outer')
   df.loc[len(df.index)]=['Total',df.customers_in_RL_hotel_env.sum(),df.customers_in_Static_hotel_env.sum()]
   return df

def model_comparison(ppo_rl_df,q_learning_rl_df,DQN_rl_df,base_df):
    model_comparison_df=pd.DataFrame(columns=['Room_type',
                                              'PPO_agent_mean_occupancy_rate', 'Q_learning_agent_mean_occupancy_Rate','DQN_agent_mean_occupancy_Rate','Base_model_mean_occupancy_Rate',
                                              'PPO_agent_mean_profit', 'Q_learning_agent_mean_profit', 'DQN_agent_mean_profit', 'Base_model_mean_profit',
                                              'PPO_agent_mean_revenue', 'Q_learning_agent_mean_revenue','DQN_agent_mean_revenue', 'Base_model_mean_revenue',

                                            ])
    for name_room in room_type:
        model_comparison_df.loc[len(model_comparison_df.index)] = [name_room, ppo_rl_df[1][name_room+'_occupancy'].mean(), q_learning_rl_df[1][name_room+'_occupancy'].mean(),DQN_rl_df[1][name_room+'_occupancy'].mean(), base_df[1][name_room+'_occupancy'].mean(),
                                                    ppo_rl_df[1][name_room+'_profit'].mean(), q_learning_rl_df[1][name_room+'_profit'].mean(),DQN_rl_df[1][name_room+'_profit'].mean(), base_df[1][name_room+'_profit'].mean(),
                                                        ppo_rl_df[1][name_room+'_revenue'].mean(), q_learning_rl_df[1][name_room+'_revenue'].mean(),DQN_rl_df[1][name_room+'_revenue'].mean(), base_df[1][name_room+'_revenue'].mean()]
    model_comparison_df.loc[len(model_comparison_df.index)]=[ 'Total', ppo_rl_df[1]['Occupancy_rate'].mean(), q_learning_rl_df[1]['Occupancy_rate'].mean(),DQN_rl_df[1]['Occupancy_rate'].mean(),base_df[1]['Occupancy_rate'].mean(),
                                                    ppo_rl_df[1]['Profit'].mean(), q_learning_rl_df[1]['Profit'].mean(),DQN_rl_df[1]['Profit'].mean(),base_df[1]['Profit'].mean(),
                                                    ppo_rl_df[1]['Daily_Revenue'].mean(), q_learning_rl_df[1]['Daily_Revenue'].mean(),DQN_rl_df[1]['Daily_Revenue'].mean(),base_df[1]['Daily_Revenue'].mean()]
    model_comparison_df.fillna(0, inplace=True)
    return model_comparison_df

def create_holiday_dataframe(start_date, end_date,weekend_weight):
    gap =end_date - start_date
    number_of_days = gap.days
    h_cols = ['date','description','holiday', 'day'] # columns of the holiday df

    segment_weekday_weights = {}
    segment_weekend_weights = {}
    segment_holiday_default_weights = {}
    segment_weekend_and_holiday_weights = {}
    for segment in customer_segments:
        segment_weekday_weights[segment] =0
        segment_weekend_weights[segment] =weekend_weight
        h_cols.append(segment)

    holiday_df = pd.DataFrame(columns=h_cols)
    US_holidays = holidays.US(years = [start_date.year, end_date.year])


    for day in range(number_of_days+1):
        current_date = start_date + datetime.timedelta(day)
        current_day = current_date.timetuple().tm_yday -1
        isweekday_str = 'weekday' if current_date.weekday()<5 else 'weekend'
        is_holiday = current_date in US_holidays
        holiday_str = US_holidays.get(current_date) if is_holiday else 'no'

        row_dict = {'date': current_date, 'description':isweekday_str, 'holiday': holiday_str, 'day': current_day}
        if is_holiday:
            for segment in customer_segments:
                segment_holiday_default_weights[segment] = random.choice([0,1,2])
                segment_weekend_and_holiday_weights[segment] = random.choice([0,1,2])+weekend_weight
    
            weights = segment_holiday_default_weights if current_date.weekday()<5 else segment_weekend_and_holiday_weights
        else:
            weights = segment_weekday_weights if current_date.weekday()<5 else segment_weekend_weights

        row_dict.update(weights)
        row = pd.Series(row_dict)
        holiday_df = pd.concat([holiday_df, row.to_frame().T], ignore_index=True)

        holiday_df['day_index'] = holiday_df.index
        simulation_days = list(holiday_df['day_index'])
    return [holiday_df,simulation_days,number_of_days]

def process_holiday_dataframe(holiday_df):

    # column aggrid definitions
    cols_def = [{"headerName": "date", "field": "date","editable": False},
                {"headerName": "description", "field": "description","editable": False},
                {"headerName": "holiday", "field": "holiday","editable": False}]

    for segment in customer_segments:
        cols_def.append({"headerName": segment, "field": segment, "editable": True})

    input_hdays_df = holiday_df[holiday_df.holiday != 'no'].reset_index()
    grid_options = {'columnDefs':cols_def}

    editable_df_dict = AgGrid(input_hdays_df, grid_options, columns_auto_size_mode= 'FIT_CONTENTS')
    inputs_df = editable_df_dict['data']

    for index in inputs_df.index:
        current_date = inputs_df.iloc[index]['date']
        for segment in customer_segments:
            segment_value = inputs_df.iloc[index][segment]
            holiday_df.loc[(pd.to_datetime(holiday_df['date']) == current_date), segment] = segment_value

    return holiday_df

def unpack_reward(nested_reward):
    reward_tracker = 0
    for type_of_room, lead_days_dict in nested_reward.items():
        for lead_day, reward in lead_days_dict.items():
                reward_tracker+= reward
    return reward_tracker

def seg_rtype_Lday_label_encoder(lead_day_input,type_of_room_input):
    segment_indicator = []
    type_of_room_indicator = []
    lead_day_indicator = []

    # for segment in customer_segments:
    #     if segment==segment_input:
    #         segment_indicator.append(1)
    #     else:
    #         segment_indicator.append(0)

    for type_of_room in room_type:
        if type_of_room==type_of_room_input:
            type_of_room_indicator.append(1)
        else:
            type_of_room_indicator.append(0)
    for lead_day in lead_time_days:
        if lead_day==lead_day_input:
            lead_day_indicator.append(1)
        else:
            lead_day_indicator.append(0)

    return type_of_room_indicator + lead_day_indicator

def action_index_map(type_of_room_in,segment_in,lead_day_in):
    i = 0
    index_dict = {}
    for type_of_room in room_type:
        index_dict[type_of_room] = {}
        for segment in customer_segments:
            index_dict[type_of_room][segment] = {}
            for lead_day in lead_time_days:
                    index_dict[type_of_room][segment][lead_day]= i
                    i+=1
    return index_dict[type_of_room_in][segment_in][lead_day_in]


def check_data(hotel_obj, epi_num,simulation_time):
      df = pd.DataFrame(columns =['room_type','booking_gap','tot_cust'])
      for day in range(simulation_time):
        for type_of_room in room_type:
                for lead_day in lead_time_days:
                    row_dict  = {'room_type':type_of_room, 'booking_gap': lead_day, 'tot_cust':hotel_obj.total_customers[type_of_room][lead_day][day]  }
                    row_series = pd.Series(row_dict)
                    df = pd.concat([df, row_series.to_frame().T], ignore_index=True)
      df.to_excel(f'data{epi_num}.xlsx')

def get_booking_gap_bin(booking_gap):
    bin_identifier = 0
    for lead_day in lead_time_days:
        if booking_gap<lead_day:
           bin_identifier = lead_time_days[lead_time_days.index(lead_day)-1]
           break
        elif booking_gap>=lead_time_days[-1]:
            bin_identifier=lead_time_days[-1]

    return bin_identifier
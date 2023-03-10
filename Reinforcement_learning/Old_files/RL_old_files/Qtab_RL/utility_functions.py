import pandas as pd
import numpy as np


from config import *


def prepare_dataframes(simulation_time,year_customers, hotel_obj,timesteps, failed_customers , booked_customers):

    customer_data =  {'customer_id': [cus.id for cus in year_customers],
                            'room_type':[cus.type for cus in year_customers],
                            'stay_duration':[cus.stay_duration for cus in year_customers],
                            'attempts':[cus.attempts for cus in year_customers], 
                            'customer_perceived_price':[cus.room_value for cus in year_customers],
                            'hotel_price':[cus.actual_hotel_price for cus in year_customers], 
                            'search_day':[cus.initial_search_day for cus in year_customers], 
                            'booked_day':[cus.booked_day for cus in year_customers], 
                            'stay_day':[cus.stay_day for cus in year_customers],
                            'booking_gap':[cus.actual_gap for cus in year_customers],
                            'remaining_days':[cus.remaining_days for cus in year_customers], 
                            'cancelled':[cus.booking_cancelled for cus in year_customers], 
                            'cancelled_day':[cus.cancelled_day for cus in year_customers],
                            'booking_status':[cus.booking_status for cus in year_customers]}

    customer_df = pd.DataFrame(customer_data)


    mydataframe = pd.DataFrame()
    for index in customer_df.index:
        if  (customer_df.cancelled[index]!=1):
            new_row=customer_df.loc[index]
            for day in range(customer_df['stay_day'][index],customer_df['stay_day'][index] + customer_df['stay_duration'][index] + 1):
                new_row['stay_day']=day   # increasing the initial stay_day within the stay duration                                                      
                mydataframe = pd.concat([mydataframe, new_row.to_frame().T], ignore_index=True)
    mydataframe['Profit']=0
    for i in room_type.keys():
        name_room_cost =i+'_cost'
        name_room_profit =i+'_profit'
        mydataframe[name_room_profit]=0
        mydataframe[name_room_profit][mydataframe.room_type==i] = mydataframe['hotel_price']-getattr(hotel_obj,name_room_cost)
        mydataframe['Profit']+=mydataframe[name_room_profit]
    mydataframe=mydataframe[mydataframe['booking_status']=='Booking successful']

    Cust_grpby = mydataframe[['stay_day', 'hotel_price', 'Profit']].groupby('stay_day').sum().reset_index()
    Cust_grpby.rename(columns={ 'hotel_price':'Daily_Revenue'},inplace=True)
    df = pd.DataFrame()
    df['stay_day'] = [i for i in range(simulation_time+10)] 
    df['no_of_rooms']=0
    df['total_no_of_booked_rooms']=0
    for i in room_type.keys():
        name_room_schedule=i+'_schedule'
        name_room_count=i+'_count'
        no_of_booked_name_room='no_of_booked_'+i
        df[name_room_schedule]=getattr(hotel_obj,name_room_schedule)
        df[name_room_count] = getattr(hotel_obj,name_room_count)
        df['no_of_rooms']+=  df[name_room_count]
        df[no_of_booked_name_room] = df[name_room_count] - df[name_room_schedule]
        df['total_no_of_booked_rooms']+=df[no_of_booked_name_room]
        df.drop(name_room_count,axis='columns',inplace=True)
    df = pd.merge(df, Cust_grpby, on='stay_day', how='outer')
    df.Profit = df.Profit.fillna(0)
    df.Daily_Revenue = df.Daily_Revenue.fillna(0)
    df['Occupancy_rate'] = df.total_no_of_booked_rooms/df.no_of_rooms*100
    df['Average_daily_rate'] = df.Daily_Revenue/df.total_no_of_booked_rooms

    metrics_df = df

    booking_rec_df = pd.DataFrame({'Day' : timesteps, 
                                   'failed_Customers'  : failed_customers, 
                                   'Booked_Customers'  : booked_customers,})

    booking_rec_df['Search_day_count'] = booking_rec_df.failed_Customers + booking_rec_df.Booked_Customers
    booking_rec_df_melt = booking_rec_df[['Day', 'failed_Customers', 'Booked_Customers']].melt(id_vars='Day')

    booking_rec_df = booking_rec_df
    booking_rec_df_melt = booking_rec_df_melt

    return customer_df,metrics_df,booking_rec_df,booking_rec_df_melt


def initialize_Q_table(agent_actions, conv_rates_list, profit_bins_list):
    actions = agent_actions
    Q = {}
    Q_full = {}
    n_states = len(conv_rates_list) * len(profit_bins_list)
    for state in range(n_states):
        Q[state] = {}
        for action in actions:
            Q[state][action] = 0
    for type in room_type.keys():
        Q_full[type] = Q
    return Q_full

def initialize_S_table(conv_rates_list, profit_bins_list):
    state = {rate: {} for rate in conv_rates_list}
    i=0
    for rate in conv_rates_list:
      for profit in profit_bins_list:
        state_num = {'s': i}
        state_num.update({type:0 for type in room_type.keys()})
        state[rate][profit] = state_num 
        i+=1
    return state

def best_state_action_value(current_state):
      max_val = np.inf*-1
      for key in current_state.keys():
            if current_state[key] > max_val:
                max_val = current_state[key]
                best_action = key
      return best_action, max_val




def dict_to_df(full_Q_dict, S_dict, profit_bins_list):

    Q_df = pd.DataFrame(columns=['State' , 1 , 1.05 , 0.95])
    Q_df_full = {type: Q_df for type in room_type.keys()}
    for type in room_type.keys():
      for k,v in full_Q_dict[type].items():
        row_dict =v
        row_dict['State'] = k
        new_row = pd.Series(row_dict)
        Q_df_full[type] = pd.concat([Q_df_full[type],new_row.to_frame().T], ignore_index=True)

    cols = profit_bins_list
    S_df = pd.DataFrame(columns = cols.append('conv'))
    for k_,v_ in S_dict.items():
        row_dict_ = {key: (sum(v_[key].values()) - v_[key]['s']) for key in v_.keys()}
        row_dict_['conv'] = k_
        new_row_ = pd.Series(row_dict_)
        S_df = pd.concat([S_df,new_row_.to_frame().T], ignore_index=True)

    return Q_df_full,S_df






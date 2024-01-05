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

    return customer_df ,metrics_df,booking_rec_df,booking_rec_df_melt







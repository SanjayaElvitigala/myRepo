from generic_files.config import *
from generic_files.customer import *
from generic_files.customer_handler import *
from generic_files.hotel import *


def create_objects(simulation_time, simulation_days, holiday_df, n_customers, input_room_list):

    customer_handler = Customer_Handler(n_customers, simulation_days, holiday_df)
    customer_handler.preparing_daily_customers()
    hotels = [Hotel(simulation_time, input_room_list,i+1) for i in range(number_of_hotels)]

    return hotels, customer_handler
from copy import deepcopy



from hotel_handler import *
from customer_handler import *
from utility_functions import *
from config import *

class Simulation_Env:

    def __init__(self,n_customers, simulation_time,cancellation_rate,input_room_list):
        self.input_room_list = input_room_list
        self.simulation_time =simulation_time
        self.n_customers = n_customers
        self.cancellation_rate = cancellation_rate

        self.hotel_handler = Hotel_Handler(simulation_time, input_room_list)
        self.customer_handler = Customer_Handler(n_customers, simulation_time)
        

    def render(self):
        simulation_time = self.simulation_time
        year_customers = self.customer_handler.year_customers
        hotel_object  = self.hotel_handler.hotel
        time_steps = self.timesteps
        failed_customers = self.failed_customers
        booked_customers =self.booked_customers

        # calling the prepare_dataframes function from the utility functions file
        customer_df,metrics_df, booking_rec_df, booking_rec_df_melt=prepare_dataframes(simulation_time, year_customers, hotel_object, time_steps, failed_customers, booked_customers)

        return customer_df,metrics_df,booking_rec_df,booking_rec_df_melt

    def reset(self):
        self.timesteps = [day+1 for day in range(self.simulation_time)]
        self.failed_customers = [0 for day in range(self.simulation_time)]
        self.booked_customers = [0 for day in range(self.simulation_time)]

        self.hotel_handler.initiate_hotel(self.simulation_time, self.input_room_list)
        self.hotel_handler.reset_total_reward()
        self.customer_handler = Customer_Handler(self.n_customers, self.simulation_time)
        self.customer_handler.preparing_daily_customers()


    def execute_logic(self, timestep, booking_process_result, customer_obj, price_of_room, failed_customers, booked_customers, daily_search_day_list, agent_activated= True):
            if booking_process_result == 4 : # Not today Customer
                pass
            else:
                customer_obj.update_attempts()

                if booking_process_result == 2: # No rooms
                    failed_customers[timestep]+=1
                    customer_obj.booking_fail(price_of_room, no_rooms =True)

                elif booking_process_result == 1: # success
                    if agent_activated:
                        self.converted_customers[customer_obj.type]+=1
                    booked_customers[timestep] += 1

                    customer_obj.update_booked_day(timestep)
                    customer_obj.booking_success(price_of_room)

                elif booking_process_result == 3: # customer price too low
                    failed_customers[timestep] += 1

                    customer_obj.booking_fail(price_of_room, low_price =True)
                    
                    if customer_obj.search_day < customer_obj.stay_day:
                        customer_obj.inc_room_price()
                    pre_search_day = customer_obj.search_day
                    customer_obj.update_search_day()

                    if pre_search_day != customer_obj.search_day:
                        daily_search_day_list[customer_obj.search_day].append(customer_obj)
                  
    def step(self, timestep):

        self.converted_customers = {type:0 for type in room_type.keys()}
        self.tot_customers = {type:0 for type in room_type.keys()}

        for customer in self.customer_handler.daily_search_day[timestep]:
            booking_status = self.hotel_handler.hotel.process_booking(timestep, customer)

            name_room_price = customer.type + '_price'
            price_of_room = getattr(self.hotel_handler.hotel,name_room_price)

            self.tot_customers[customer.type]+=1

            self.execute_logic(timestep, booking_status, customer, price_of_room,  self.failed_customers, self.booked_customers, self.customer_handler.daily_search_day)
    

        if sum(self.tot_customers.values())>0: # checking if atleast one customer is present
            self.hotel_handler.take_action(total_customers=self.tot_customers, converted_customers= self.converted_customers)

        if self.cancellation_rate>0:
            for cus in [cuss for cuss in self.customer_handler.year_customers if ((cuss.booking_status=='Booking successful') and (cuss.stay_day>timestep))]:
                cus.remaining_days -=1
                random_value = random.uniform(0,1)
                if random_value < (self.cancellation_rate/100) :
                    self.hotel_handler.hotel.update_cancel_room_schedule(cus)
                    cus.booking_cancel(timestep)


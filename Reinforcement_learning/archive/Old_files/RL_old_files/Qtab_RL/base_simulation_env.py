from copy import deepcopy



from hotel_handler import *
from customer_handler import *
from utility_functions import *
from config import *


class Base_Simulation_Env:

    def __init__(self,n_customers, simulation_time,cancellation_rate,input_room_list):
        self.input_room_list = input_room_list
        self.simulation_time =simulation_time
        self.n_customers = n_customers
        self.cancellation_rate = cancellation_rate

        self.base_cust_list = []

    def render(self):
        
        base_customer_df, base_metrics_df, base_booking_rec_df, base_booking_rec_df_melt = prepare_dataframes(self.simulation_time,self.base_cust_list, self.base_hotel,self.timesteps, self.base_failed_customers , self.base_booked_customers)
        base_model_dataframes = [base_customer_df, base_metrics_df, base_booking_rec_df, base_booking_rec_df_melt]
        return base_model_dataframes


    def reset(self, current_episode, total_episode, daily_search_day_customers):
        # base hotel with deterministic pricing
        if current_episode == (total_episode-1):  # running the base hotel model in the last episode
            self.base_model_customers = deepcopy(daily_search_day_customers)

            
            for cust_list in self.base_model_customers.values():
                for cust in cust_list:
                    self.base_cust_list.append(cust)
            self.base_cust_list = list(dict.fromkeys(self.base_cust_list))

            self.base_hotel = Hotel(self.simulation_time, self.input_room_list, agent_activated = False)
            self.timesteps = [day+1 for day in range(self.simulation_time)]
            self.base_failed_customers = [0 for day in range(self.simulation_time)]
            self.base_booked_customers = [0 for day in range(self.simulation_time)]

    def execute_logic(self, timestep, booking_process_result, customer_obj, price_of_room, failed_customers, booked_customers, daily_search_day_list, agent_activated= True):
            if booking_process_result == 4 : # Not today Customer
                pass
            else:
                customer_obj.update_attempts()

                if booking_process_result == 2: # No rooms
                    failed_customers[timestep]+=1
                    customer_obj.booking_fail(price_of_room, no_rooms =True)

                elif booking_process_result == 1: # success
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

    def step(self, timestep, current_episode, total_episode):
        # for base hotel
        if current_episode == (total_episode-1): # running the base hotel model in the last episode
            for base_customer in self.base_model_customers[timestep]:
                base_booking_status = self.base_hotel.process_booking(timestep, base_customer)

                name_room_price = base_customer.type + '_price'
                base_price_of_room = (getattr(self.base_hotel,name_room_price)+ self.base_hotel.price_change_rate*(base_customer.booking_gap))

                self.execute_logic(timestep, base_booking_status, base_customer, base_price_of_room,  self.base_failed_customers, self.base_booked_customers, self.base_model_customers, agent_activated=False)

        if self.cancellation_rate>0:
            for cus in [cuss for cuss in self.base_cust_list if ((cuss.booking_status=='Booking successful') and (cuss.stay_day>timestep))]:
                cus.remaining_days -=1
                random_value = random.uniform(0,1)
                if random_value < (self.cancellation_rate/100) :
                    self.base_hotel.update_cancel_room_schedule(cus)
                    cus.booking_cancel(timestep)
       
from copy import deepcopy
from collections import OrderedDict
from gym.spaces import Box, Discrete, Tuple, Dict


from pricing_algo import *
from customer_handler import *
from utility_functions import *
from logic_functions import *
from config import *

class Simulation_Env:

    def __init__(self,n_customers, simulation_time,cancellation_rate,input_room_list):
        self.input_room_list = input_room_list
        self.simulation_time =simulation_time
        self.time_step = 0
        self.n_customers = n_customers
        self.cancellation_rate = cancellation_rate

        self.observation_space = Box(low= np.array([0,0]), high = np.array([1,2]) , shape= (2,) ) # conversion_rate = 0-1 , expected_ROI = 0-2 
        self.action_space = Discrete(3)  # 0- 0.95(decrease by 5%) , 1 - 1(stay the same), 2 - 1.05 (increase by 5%)

        self.pricing_algorithm = Pricing_Algo(self.observation_space.shape,self.action_space.n )

        

    def render(self):
        simulation_time = self.simulation_time
        year_customers = self.customer_handler.year_customers
        hotel_object  = self.hotel
        time_steps = self.timesteps
        failed_customers = self.failed_customers
        booked_customers =self.booked_customers

        # calling the prepare_dataframes function from the utility functions file
        rl_customer_df, rl_metrics_df, rl_booking_rec_df, rl_booking_rec_df_melt = prepare_dataframes(simulation_time, 
                                                                                                    year_customers, 
                                                                                                    hotel_object, 
                                                                                                    time_steps, 
                                                                                                    failed_customers, 
                                                                                                    booked_customers)

        base_customer_df, base_metrics_df, base_booking_rec_df, base_booking_rec_df_melt = prepare_dataframes(simulation_time, 
                                                                                                            self.base_customer_handler.year_customers, 
                                                                                                            self.base_hotel, 
                                                                                                            time_steps, 
                                                                                                            self.base_failed_customers, 
                                                                                                            self.base_booked_customers)
        rl_df = [rl_customer_df, rl_metrics_df, rl_booking_rec_df, rl_booking_rec_df_melt]
        base_df = [base_customer_df, base_metrics_df, base_booking_rec_df, base_booking_rec_df_melt]
        
        return rl_df,base_df

    def reset(self):
        self.timesteps = [day+1 for day in range(self.simulation_time)]
        self.failed_customers = [0 for day in range(self.simulation_time)]
        self.booked_customers = [0 for day in range(self.simulation_time)]

        self.hotel = Hotel(self.simulation_time, self.input_room_list)
        self.customer_handler = Customer_Handler(self.n_customers, self.simulation_time)
        self.customer_handler.preparing_daily_customers()

        self.base_failed_customers = [0 for day in range(self.simulation_time)]
        self.base_booked_customers = [0 for day in range(self.simulation_time)]

        self.base_hotel = deepcopy(self.hotel)
        self.base_hotel.agent_activated = False
        self.base_customer_handler = deepcopy(self.customer_handler)
       


        return {type_of_room: np.array([0,0],dtype='float32') for type_of_room in room_type}



    def execute_cancellation(self, year_customers, hotel_obj, timestep):
        for cus in [cuss for cuss in year_customers if ((cuss.booking_status=='Booking successful') and (cuss.stay_day>timestep))]:
                cus.remaining_days -=1
                random_value = random.uniform(0,1)
                if random_value < (self.cancellation_rate/100) :
                    hotel_obj.update_cancel_room_schedule(cus)
                    cus.booking_cancel(timestep)


    def prepare_outputs(self):
        next_state ={}
        reward = {}
        for type_of_room in room_type:
            conversion = round((self.rl_converted_customers[type_of_room]/self.rl_tot_customers[type_of_room]),2) if self.rl_tot_customers[type_of_room]>0 else 0

            room_price = type_of_room +'_price'
            room_cost = type_of_room +'_cost'
            # expected_profit = (getattr(self.hotel,room_price) - getattr(self.hotel,room_cost)) * self.converted_customers[type_of_room]
            expected_ROI = (getattr(self.hotel,room_price) - getattr(self.hotel,room_cost))/getattr(self.hotel,room_cost)

            next_state[type_of_room]=np.array([conversion, expected_ROI],dtype='float32')
            reward[type_of_room]=self.pricing_algorithm.get_reward(conversion, expected_ROI)
        return next_state,reward
    
    def update_timestep(self):
        if self.time_step < self.simulation_time-1:
            self.time_step+=1

    def step(self, action_taken, time_step):

        self.rl_converted_customers = {type:0 for type in room_type.keys()}
        self.rl_tot_customers = {type:0 for type in room_type.keys()}
        
        self.pricing_algorithm.set_price(self.hotel, action_taken)
        execute_logic(self,time_step, self.failed_customers, self.booked_customers, self.hotel, self.customer_handler.daily_search_day)
        execute_logic(self,time_step, self.base_failed_customers, self.base_booked_customers, self.base_hotel, self.base_customer_handler.daily_search_day, agent_activated= False)

        next_state,reward = self.prepare_outputs()

        # if self.cancellation_rate>0:
        #     self.execute_cancellation(self.customer_handler.year_customers, self.hotel, timestep)

        done = False if time_step<(self.simulation_time-1) else True

        info = {}

        return next_state,reward,done,info


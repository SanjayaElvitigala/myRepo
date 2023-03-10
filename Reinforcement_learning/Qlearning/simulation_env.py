from copy import deepcopy
from collections import OrderedDict
from gym.spaces import Box, Discrete, Tuple, Dict

from generic_files.hotel import *
from generic_files.customer_handler import *
from generic_files.utility_functions import *
from generic_files.logic_functions import *
from generic_files.config import *

import pickle

class Simulation_Env:

    def __init__(self,n_customers,simulation_days, holiday_df, simulation_time,cancellation_rate,input_room_list, compare):
        self.compare = compare
        self.input_room_list = input_room_list
        self.simulation_time =simulation_time
        self.simulation_days = simulation_days
        self.holiday_df = holiday_df
        
        self.n_customers = n_customers
        self.cancellation_rate = cancellation_rate

        self.observation_space = Box(low= np.array([0,0,0,-5]), high = np.array([1,2,225,5]) , shape= (4,) ) # conversion_rate = 0-1 , expected_ROI = 0-2 
        self.action_space = Discrete(3)  # 0- 0.95(decrease by 5%) , 1 - 1(stay the same), 2 - 1.05 (increase by 5%)


    def prepare_outputs(self):
        next_state ={}
        reward = {}
        time_step = self.time_step
        for type_of_room in room_type:

            conv_cust, tot_cust, expect_total_profit, conversion, expected_ROI, room_price, room_cost, static_expect_total_profit = summarize_metrics(self.hotel, type_of_room, time_step)
            action = self.hotel.last_action_taken[type_of_room]
            
            next_state[type_of_room]=np.array([tot_cust, conv_cust, conversion, expect_total_profit, expected_ROI, room_price, action], dtype='float32')
            reward[type_of_room]=self.get_reward(conversion, expected_ROI, expect_total_profit,static_expect_total_profit, room_price, room_cost)
        return next_state,reward
    
    
    def update_timestep(self):
            self.time_step+=1

    def get_reward(self, conversion, expected_ROI, expect_total_profit, static_expect_total_profit, room_price, room_cost):
    #   reward_tracker = 0
    #   conv_rewards = 2  if conversion >= self.hotel.target_conversion_rate else -2
    #   ROI_rewards = 2 if expected_ROI >= self.hotel.target_ROI_margin else -10

    #   reward_tracker = conv_rewards + ROI_rewards
    #   return reward_tracker
        return self.hotel.per_day_profit-self.base_hotels[0].per_day_profit 

    def render(self):
        time_steps = [day+1 for day in range(self.simulation_time)]

        # calling the prepare_dataframes function from the utility functions file
        rl_df= prepare_dataframes(self.simulation_time, 
                                    self.customer_handler.year_customers, 
                                    self.hotels[0], 
                                    time_steps)

        base_df= prepare_dataframes(self.simulation_time, 
                                    self.base_customer_handler.year_customers, 
                                    self.base_hotels[0], 
                                    time_steps)

        return rl_df,base_df

    def reset(self, episode, n_episode):

        self.time_step = 0
        if self.compare and (episode == n_episode):
            with open("pickle_objects\hotel_objs.pkl", "rb") as inp1:   # Unpickling
                self.hotels = pickle.load(inp1)
            self.hotel = self.hotels[0]

            with open("pickle_objects\customer_handler_obj.pkl", "rb") as inp2:   # Unpickling
                self.customer_handler = pickle.load(inp2)
        else:
            self.hotels = [Hotel(self.simulation_time, self.input_room_list,i+1) for i in range(number_of_hotels)]
            self.hotel = self.hotels[0]
            self.customer_handler = Customer_Handler(self.n_customers, self.simulation_days, self.holiday_df)
            self.customer_handler.preparing_daily_customers()

        # self.base_hotel = deepcopy(self.hotel)
        self.base_hotels = deepcopy(self.hotels)
        self.base_customer_handler = deepcopy(self.customer_handler)
        # room_type : [total_customers, conv_cust, conversion, total_profit, expected_ROI, room_price, last_price_change ]
        return {type_of_room: np.array([0,0,0,0,0, getattr(self.hotel, type_of_room+'_price'), random.choice([0.95,1,1.05])],dtype='float32') for type_of_room in room_type}


    def step(self, actions):

        self.hotel.set_price(actions)

        execute_logic(self.hotels, self.time_step, self.customer_handler.daily_search_day)
        execute_logic(self.base_hotels, self.time_step, self.base_customer_handler.daily_search_day)

        next_state,reward = self.prepare_outputs()

        if self.cancellation_rate>0:
            execute_cancellation(self.cancellation_rate,self.customer_handler.year_customers, self.hotels, self.time_step)
            execute_cancellation(self.cancellation_rate,self.base_customer_handler.year_customers, self.base_hotels, self.time_step)

        done = False if self.time_step < (self.simulation_time-1) else True

        info = {}
        self.hotel.per_day_profit = 0
        self.base_hotels[0].per_day_profit = 0
        return next_state,reward,done,info

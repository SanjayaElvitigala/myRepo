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

        next_state = {}
        reward = {}
        for type_of_room in room_type:
            lead_day_wise_obs = {}
            lead_day_wise_rew = {}
            for lead_day in lead_time_days:
                conv_cust, tot_cust, expect_total_profit, conversion, expected_ROI, room_price, room_cost, static_expect_total_profit = summarize_metrics(self.hotel, type_of_room,lead_day, time_step)
                action = self.hotel.last_action_taken[type_of_room][lead_day]
                metrics_needed = [tot_cust, conv_cust, expect_total_profit, action]
                metrics_needed = metrics_needed+ seg_rtype_Lday_label_encoder(lead_day,type_of_room)
                lead_day_wise_obs[lead_day] = np.array(metrics_needed, dtype= 'float32')
                lead_day_wise_rew[lead_day] = self.get_reward(type_of_room,lead_day,conversion, expected_ROI, expect_total_profit,static_expect_total_profit, room_price, room_cost)

                next_state[type_of_room]= lead_day_wise_obs
                reward[type_of_room] = lead_day_wise_rew
        return next_state,reward
    
    
    def update_timestep(self):
            self.time_step+=1

    def get_reward(self,type_of_room,lead_day, conversion, expected_ROI, expect_total_profit, static_expect_total_profit, room_price, room_cost):
    #   reward_tracker = 0
    #   conv_rewards = 2  if conversion >= self.hotel.target_conversion_rate else -2
    #   ROI_rewards = 2 if expected_ROI >= self.hotel.target_ROI_margin else -10

    #   reward_tracker = conv_rewards + ROI_rewards

    #   conv_rewards = (conversion - self.hotel.target_conversion_rate)*10

    #   profit_rewards = (expect_total_profit - 1.1*static_expect_total_profit)

    # #   conv_profit_rewards = ((conversion - self.hotel.target_conversion_rate) * (expect_total_profit - 1.1*static_expect_total_profit))/10

    #   price_lower_bound, price_upper_bound = room_cost+20, room_cost*2 


    #   reward_tracker = conv_rewards + profit_rewards
    #   reward_tracker = round(reward_tracker) 
      return self.hotel.per_day_profit[type_of_room][lead_day]-self.base_hotels[0].per_day_profit[type_of_room][lead_day]
    #   return reward_tracker

    def render(self):
        self.timesteps = [day+1 for day in range(self.simulation_time)]
        # calling the prepare_dataframes function from the utility functions file
        rl_df = prepare_dataframes(self.simulation_time, 
                                    self.customer_handler.year_customers, 
                                    self.hotels[0], 
                                    self.timesteps)

        base_df = prepare_dataframes(self.simulation_time, 
                                    self.base_customer_handler.year_customers, 
                                    self.base_hotels[0], 
                                    self.timesteps)

        return rl_df,base_df

    def reset(self):

        self.time_step = 0
        if self.compare:
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

        return {type_of_room:{lead_day : np.array([0,0,0,random.choice([0.95,0.975,1,1.025,1.05])] + [0 for i in range(len(room_type)+len(lead_time_days))],dtype='float32') 
                                        for lead_day in lead_time_days}
                for type_of_room in room_type}


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
        self.hotel.per_day_profit = {type_of_room: {lead_day: 0 for lead_day in lead_time_days} for type_of_room in room_type.keys() }
        self.base_hotels[0].per_day_profit = {type_of_room: {lead_day: 0 for lead_day in lead_time_days}  for type_of_room in room_type.keys() }
        return next_state,reward,done,info


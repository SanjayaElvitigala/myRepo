import pandas as pd
import numpy as np

from hotel import *
from config import * 
from utility_functions import *



class Hotel_Handler:

  conv_rates = [0,0.01,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1]
  profit_bins = [0,1,1001,2001,3001,4001,5001,6001]
  bin_length = 5

  def __init__(self, simulation_time, input_room_list):
      self.state_obs = {type:[0,0] for type in room_type.keys() } # [conversion ratio bin , profit bin ratio bin]
      self.actions = [1, 1.05, 0.95]
      self.action_taken = {type:random.choice(self.actions) for type in room_type.keys()}

      self.total_epi_reward = 0
      self.Q_dict = initialize_Q_table(self.actions, self.conv_rates, self.profit_bins) # initialising the q table  
      self.S_dict = initialize_S_table(self.conv_rates, self.profit_bins) # initialising the state table
      self.EPSILON = 0.8
      self.epsilon_decay = 0.001
      self.LEARNING_RATE = 0.05
      self.DISCOUNT = 0.95
      self.target_ROI_margin = 0.4 # 40 percent ROI margin
      self.target_conversion_rate  = 0.1 # 20 percent conversion rate

  def initiate_hotel(self,simulation_time, input_room_list):
    self.hotel = Hotel(simulation_time, input_room_list)

  def update_state_table(self,type):
      conversion_bin = self.state_obs[type][0]
      profit_bin = self.state_obs[type][1]
      self.S_dict[conversion_bin][profit_bin][type]+=1
      

  def get_reward(self, tot_cust, conv_cust, type):
      reward_tracker = 0

      conv_rate = conv_cust[type]/ tot_cust[type] 
      conv_rewards = 2  if conv_rate >= self.target_conversion_rate else -2

      room_price, room_cost = type+'_price', type+'_cost'
      actual_ROI = (getattr(self.hotel,room_price) - getattr(self.hotel,room_cost))/getattr(self.hotel,room_cost)      
      ROI_rewards = 2 if actual_ROI >= self.target_ROI_margin else -10
    
      reward_tracker = conv_rewards + ROI_rewards
      return reward_tracker


  def set_price(self, action, type):
    self.action_taken[type] = action
    room_price = type+'_price'
    setattr(self.hotel, room_price, getattr(self.hotel,room_price)*action)


  def set_state_obs(self, tot_cust, conv_cust,type):
      conv_bin_pointer = -1 # placeholder to identify the correct conversion rate bin
      profit_bin_pointer =-1 # placeholder to identify the correct profit rate bin

      conversion = round((conv_cust[type]/tot_cust[type]),2) if tot_cust[type]>0 else 0

      room_price = type+'_price'
      room_cost = type+'_cost'
      profit = (getattr(self.hotel,room_price) - getattr(self.hotel,room_cost)) * conv_cust[type] 

      for conv in self.conv_rates:
        if conversion<conv:
            conv_bin_pointer = self.conv_rates[self.conv_rates.index(conv)-1]
            break
        elif conversion==conv:
            conv_bin_pointer = self.conv_rates[self.conv_rates.index(conv)]
            break

      for profit_bin in self.profit_bins:
        if profit<profit_bin:
            profit_bin_pointer = self.profit_bins[self.profit_bins.index(profit_bin)-1]
            break
        elif profit==profit_bin:
            profit_bin_pointer = self.profit_bins[self.profit_bins.index(profit_bin)]
            break

      self.state_obs[type] = [conv_bin_pointer,profit_bin_pointer]


  def take_action(self,total_customers, converted_customers):
    Q_dict= self.Q_dict 
    for type in room_type.keys():
      if  total_customers[type]:    
        prev_state = self.S_dict[ self.state_obs[type][0] ][ self.state_obs[type][1] ]['s']
        prev_action = self.action_taken[type]
      
        self.set_state_obs(total_customers,converted_customers,type)
        self.update_state_table(type)
        
        current_state = self.S_dict[self.state_obs[type][0]][self.state_obs[type][1]]['s']
        
        if np.random.uniform() > self.EPSILON:
              action, max_qt1 = best_state_action_value(Q_dict[type][current_state])
        else:
              action = np.random.choice(self.actions)
              max_qt1 = Q_dict[type][current_state][action]
        

        if total_customers[type]>0:
          self.set_price(action,type)
          reward = self.get_reward(total_customers, converted_customers,type)
          self.Q_dict[type][prev_state][prev_action] += self.LEARNING_RATE*(reward +self.DISCOUNT*max_qt1- self.Q_dict[type][prev_state][prev_action])
          self.total_epi_reward+=reward
    
    if self.EPSILON >0:
     self.EPSILON-=self.epsilon_decay

  def reset_total_reward(self):
    self.total_epi_reward = 0
  
  
    
    
    
    


        
    

   
import pandas as pd
import numpy as np
import random
from collections import deque
from operator import itemgetter 

import copy 
import torch
import torch.nn as nn
import torch.nn.functional as F

from generic_files.config import * 

class DeepQNetwork(nn.Module):
    def __init__(self, learning_rate, state_shape, action_shape, n_dense_1, n_dense_2):
        super(DeepQNetwork, self).__init__()
        self.layer_1 =  nn.Linear(state_shape, n_dense_1)
        self.layer_2 =  nn.Linear(n_dense_1, n_dense_2)
        self.layer_3 =  nn.Linear(n_dense_2, action_shape, dtype= torch.float32)
        self.optimizer = torch.optim.Adam(self.parameters(), lr = learning_rate)
        self.cost_func = nn.MSELoss()
        
    def forward(self, state):
        x = F.relu(self.layer_1(state))
        x = F.relu(self.layer_2(x))
        actions = self.layer_3(x)
        return actions

class DQN:

  def __init__(self, state_shape, action_shape, observation_indexes, is_training):
       #{type_of_room: {segment: {lead_day : [] for lead_day in lead_time_days} for segment in customer_segments} for type_of_room in room_type} 
      self.current_state_mem = {type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}
      self.new_state_mem = {type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}
      self.actions_mem = {type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}
      self.actions_indexes_mem ={type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}
      self.rewards_mem ={type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}
      self.dones_mem ={type_of_room: {lead_day : [] for lead_day in lead_time_days} for type_of_room in room_type}

      self.EPSILON = 0.7 if is_training else 0
      self.epsilon_min = 0.01
      self.epsilon_decay = 0.01
      self.ALPHA = 0.05
      self.learning_rate = 0.001
      self.DISCOUNT = 0.95
      self.cost_tracker = 0
      
      self.actions =  [0.95,0.975,1,1.025,1.05]#[-2,0,2]
      self.action_indexes = list(range(len(self.actions)))
      self.observation_indexes = observation_indexes
      self.batch_size = 80
      self.batch_start = 0
      self.batch_end = self.batch_size

      if is_training:
          self.main_model =DeepQNetwork(self.learning_rate,state_shape, action_shape, n_dense_1=100, n_dense_2=100)
        
      else:
          self.main_model =DeepQNetwork(self.learning_rate,state_shape, action_shape, n_dense_1=100, n_dense_2=100)
          self.main_model.load_state_dict(torch.load(f'DQN\models\model_lead_day_2.pkl'))

      self.target_model = DeepQNetwork(self.learning_rate, state_shape, action_shape, n_dense_1=100, n_dense_2=100)
      self.target_model.load_state_dict(self.main_model.state_dict())


  def store_data(self, curr_obs, nxt_obs, action, reward, done):
        done_val = 1 if done else 0
        for type_of_room in room_type:
                for lead_day in lead_time_days:
                    if curr_obs[type_of_room][lead_day][0]>0:
                        self.current_state_mem[type_of_room][lead_day].append(curr_obs[type_of_room][lead_day])
                        self.new_state_mem[type_of_room][lead_day].append(nxt_obs[type_of_room][lead_day])
                        self.actions_mem[type_of_room][lead_day].append(action[type_of_room][lead_day])
                        self.actions_indexes_mem[type_of_room][lead_day].append(self.action_mapping(action[type_of_room][lead_day], reversed= True))
                        self.rewards_mem[type_of_room][lead_day].append(reward[type_of_room][lead_day])
                        self.dones_mem[type_of_room][lead_day].append(done_val)

  def action_mapping(self,action , reversed = False): 
        if reversed:
            action_index = self.actions.index(action)
            return action_index 
        else:
            action_index = action
            return self.actions[action_index]
            

  def take_action(self,observation, action_space):
        actions = {}
        for type_of_room in room_type:
            actions[type_of_room] = {}
            for lead_day in lead_time_days:
                if np.random.uniform() > self.EPSILON:
                    predicted = self.main_model.forward(torch.tensor(observation[type_of_room][lead_day]))
                    action_index = np.argmax(predicted.tolist())
                    actions[type_of_room][lead_day] = self.action_mapping(action_index)
                else:
                    action_index = random.choice(action_space)
                    actions[type_of_room][lead_day] = self.action_mapping(action_index)
        return actions

  def train(self,done): 
    current_cost_tracker = 0
    MIN_REPLAY_SIZE = self.batch_size
    
    for type_of_room in room_type:
            for lead_day in lead_time_days:
                if len(self.current_state_mem[type_of_room][lead_day]) > MIN_REPLAY_SIZE:
                    batch_sample = random.sample(list(range(len(self.current_state_mem[type_of_room][lead_day]))), self.batch_size) 
                    batch_indexes = list(range(self.batch_size)) 

                    self.main_model.optimizer.zero_grad()
                    curr_obs_batch = torch.tensor(itemgetter(*batch_sample)(self.current_state_mem[type_of_room][lead_day]), dtype= torch.float32)
                    nxt_obs_batch  = torch.tensor(itemgetter(*batch_sample)(self.new_state_mem[type_of_room][lead_day]), dtype= torch.float32)
                    actions_indexes_batch = itemgetter(*batch_sample)(self.actions_indexes_mem[type_of_room][lead_day])
                    rewards_batch = torch.tensor(itemgetter(*batch_sample)(self.rewards_mem[type_of_room][lead_day]), dtype= torch.float32)
                    dones_batch = itemgetter(*batch_sample)(self.dones_mem[type_of_room][lead_day])  # [0,0,0,1]
                    not_dones_batch = torch.tensor(np.ones(len(dones_batch))-dones_batch, dtype= torch.float32, requires_grad= True) # [1,1,1,0]
                    
                    curr_qs_batch = self.main_model.forward(curr_obs_batch)[batch_indexes, actions_indexes_batch]
                    nxt_qs_batch = self.target_model.forward(nxt_obs_batch)

                    q_target = torch.add(rewards_batch,not_dones_batch*self.DISCOUNT*torch.max(nxt_qs_batch, dim=1)[0])
                    # changed_q = curr_qs_batch + ALPHA * (q_target - curr_qs_batch)
                    cost = self.main_model.cost_func(curr_qs_batch, q_target)
                    current_cost_tracker+=cost
                    cost.backward()
                    self.main_model.optimizer.step()
                
    self.batch_start = self.batch_end
    self.batch_end += self.batch_size
    self.cost_tracker = current_cost_tracker

    
  def get_min_len(self):
    min_len = np.inf
    
    for type_of_room in room_type:
        for segment in customer_segments:
            for lead_day in lead_time_days:
                len_tracker = len(self.current_state_mem[type_of_room][segment][lead_day])
                if min_len>len_tracker:
                    min_len = len_tracker
                    details = [type_of_room,segment,lead_day]

    return min_len,details
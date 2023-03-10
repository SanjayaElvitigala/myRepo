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

      self.replay_memory = []
      self.current_state_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}
      self.new_state_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}
      self.actions_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}
      self.actions_indexes_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}
      self.rewards_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}
      self.dones_mem = {type_of_room: {segment: [] for segment in customer_segments} for type_of_room in room_type}

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
          self.main_model =DeepQNetwork(self.learning_rate,state_shape, action_shape, n_dense_1=50, n_dense_2=50)
        
      else:
          self.main_model =DeepQNetwork(self.learning_rate,state_shape, action_shape, n_dense_1=50, n_dense_2=50)
          self.main_model.load_state_dict(torch.load(f'DQN\models\model_seg.pkl'))

      self.target_model = DeepQNetwork(self.learning_rate, state_shape, action_shape, n_dense_1=50, n_dense_2=50)
      self.target_model.load_state_dict(self.main_model.state_dict())


  def store_data(self, curr_obs, nxt_obs, action, reward, done):
        done_val = 1 if done else 0
        for type_of_room in room_type:
            for segment in customer_segments:
                if curr_obs[type_of_room][segment][0]>0:
                    self.current_state_mem[type_of_room][segment].append(curr_obs[type_of_room][segment])
                    self.new_state_mem[type_of_room][segment].append(nxt_obs[type_of_room][segment])
                    self.actions_mem[type_of_room][segment].append(action[type_of_room][segment])
                    self.actions_indexes_mem[type_of_room][segment].append(self.action_mapping(action[type_of_room][segment], reversed= True))
                    self.rewards_mem[type_of_room][segment].append(reward[type_of_room][segment])
                    self.dones_mem[type_of_room][segment].append(done_val)

  def action_mapping(self,action , reversed = False): 
        if reversed:
            action_index = self.actions.index(action)
            return action_index 
        else:
            action_index = action
            return self.actions[action_index]
            

  def take_action(self,observation, action_space):
        actions_dict = {}
        for type_of_room in room_type.keys():
            segmentwise_actions = {}
            for segment in customer_segments:
                if np.random.uniform() > self.EPSILON:
                    encoded = observation[type_of_room][segment]
                    predicted = self.main_model.forward(torch.tensor(encoded))
                    action_index = np.argmax(predicted.tolist())
                    segmentwise_actions[segment] = self.action_mapping(action_index)
                else:
                    action_index = random.choice(action_space)
                    segmentwise_actions[segment] = self.action_mapping(action_index)
            actions_dict[type_of_room] = segmentwise_actions
        
        return actions_dict

  def train(self,done):
    current_cost_tracker = 0
    MIN_REPLAY_SIZE = self.batch_end + self.batch_size
    if self.get_min_len() < MIN_REPLAY_SIZE:
        return
    else:
        batch_sample = random.sample(list(range(self.get_min_len())), self.batch_size)
        batch_indexes = list(range(self.batch_size))
        
        for type_of_room in room_type:
            for segment in customer_segments:
                self.main_model.optimizer.zero_grad()
                curr_obs_batch = torch.tensor(itemgetter(*batch_sample)(self.current_state_mem[type_of_room][segment]), dtype= torch.float32, requires_grad= True)
                nxt_obs_batch  = torch.tensor(itemgetter(*batch_sample)(self.new_state_mem[type_of_room][segment]), dtype= torch.float32, requires_grad= True)
                actions_indexes_batch = itemgetter(*batch_sample)(self.actions_indexes_mem[type_of_room][segment])
                rewards_batch = torch.tensor(itemgetter(*batch_sample)(self.rewards_mem[type_of_room][segment]), dtype= torch.float32, requires_grad= True)
                dones_batch = itemgetter(*batch_sample)(self.dones_mem[type_of_room][segment])  # [0,0,0,1]
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
            len_tracker = len(self.current_state_mem[type_of_room][segment])
            if min_len>len_tracker:
                min_len = len_tracker
    return min_len
        
import pandas as pd
import numpy as np
from collections import deque
import tensorflow as tf

import copy 
import torch
import torch.nn as nn

from generic_files.config import * 



class DQN:

  def __init__(self, state_shape, action_shape, observation_indexes, is_training):

      self.replay_memory = []
      self.EPSILON = 0.8 if is_training else 0.01
      self.epsilon_min = 0.01
      self.epsilon_decay = 0.001
      self.ALPHA = 0.05
      self.learning_rate = 0.01
      self.DISCOUNT = 0.95

      
      
      self.actions =  [0.95,1,1.05]#[-2,0,2]
      self.observation_indexes = observation_indexes
      self.batch_size = 80
      self.batch_start = 0
      self.batch_end = self.batch_size

      if is_training:
          self.main_model =self.create_model(state_shape, action_shape, n_dense_1=200, n_dense_2=200, n_dense_3= 200)
      else:
          self.main_model =self.create_model(state_shape, action_shape, n_dense_1=200, n_dense_2=200, n_dense_3= 200)
          self.main_model.load_state_dict(torch.load('combined_RL\h5_files\model1.pkl'))

   
      self.target_model = self.create_model(state_shape, action_shape, n_dense_1=200, n_dense_2=200, n_dense_3= 200)
      self.target_model.load_state_dict(self.main_model.state_dict())

      self.optimizer = torch.optim.SGD(self.main_model.parameters(), lr = self.learning_rate)
      self.cost_func = nn.HuberLoss()


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
            if np.random.uniform() > self.EPSILON:
                  
                encoded = observation[type_of_room][self.observation_indexes ]
                predicted = self.main_model(torch.tensor(encoded))
                action_index = np.argmax(predicted.tolist())
                actions_dict[type_of_room] = self.action_mapping(action_index)
            else:
                action_index = action_space.sample()
                actions_dict[type_of_room] = self.action_mapping(action_index)
        
        return actions_dict

  def create_model(self, state_shape, action_shape, n_dense_1, n_dense_2, n_dense_3):
    model = nn.Sequential(
        nn.Linear(state_shape, n_dense_1),
        nn.ReLU(),
    
        nn.Linear(n_dense_1, n_dense_2),
        nn.ReLU(),
        
        nn.Linear(n_dense_2, n_dense_3),
        nn.ReLU(),
    
        nn.Linear(n_dense_3, action_shape),)
    return model

  def single_training_round(self):
    pass

  def train(self,done):
    ALPHA = self.ALPHA # Learning rate
    DISCOUNT =self.DISCOUNT
    batch_size = self.batch_size
    observation_indexes = [1,3,4,5] # conversion, expected_roi, room_price, action

    MIN_REPLAY_SIZE = self.batch_end + batch_size
    if len(self.replay_memory) < MIN_REPLAY_SIZE:
        return
    else:
        
        mini_batch = self.replay_memory[self.batch_start : self.batch_end]
        self.batch_start = self.batch_end
        self.batch_end += batch_size

        for type_of_room in room_type:
            for index, (observation, new_observation, action, reward,  done) in enumerate(mini_batch):
                if observation[type_of_room][0] > 0:
                        current_state = observation[type_of_room][self.observation_indexes ]
                        current_qs = self.main_model(torch.tensor(current_state))

                        next_state = new_observation[type_of_room][self.observation_indexes ]
                        future_qs = self.target_model(torch.tensor(next_state))

                        if not done:
                            target_q = reward[type_of_room] + DISCOUNT * np.max(future_qs.tolist())
                        else:
                            target_q = reward[type_of_room]

                        action_index = self.action_mapping(action[type_of_room], reversed= True)
                        # current_qs[0][action_index] += ALPHA * (max_future_q - current_qs[0][action_index])
                        # current_qs[0][action_index] = target_q 
                        changed_current_qs = current_qs.clone()
                        changed_current_qs[action_index] += ALPHA * (target_q - changed_current_qs[action_index])
                        cost = self.cost_func(current_qs, changed_current_qs)

                        self.optimizer.zero_grad()
                        cost.backward()
                        self.optimizer.step()



#   def train(self,done):
#     ALPHA = self.ALPHA # Learning rate
#     DISCOUNT =self.DISCOUNT
#     batch_size = self.batch_size
#     observation_indexes = [1,3,4,5] # conversion, expected_roi, room_price, action

#     MIN_REPLAY_SIZE = self.batch_end + batch_size
#     if len(self.replay_memory) < MIN_REPLAY_SIZE:
#         return
#     else:
        
#         mini_batch = self.replay_memory[self.batch_start : self.batch_end]
#         self.batch_start = self.batch_end
#         self.batch_end += batch_size

#         for type_of_room in room_type:
#             X = []
#             Y = []
#             for index, (observation, new_observation, action, reward,  done) in enumerate(mini_batch):
#                 if observation[type_of_room][0] > 0:
#                         current_state = observation[type_of_room][self.observation_indexes ]
#                         current_state = current_state.reshape([1, current_state.shape[0]])
#                         current_qs = self.main_model.predict(current_state, verbose = 0)

#                         next_state = new_observation[type_of_room][self.observation_indexes ]
#                         next_state = next_state.reshape([1, next_state.shape[0]])
#                         future_qs =  self.target_model.predict(next_state, verbose = 0)

#                         if not done:
#                             max_future_q = reward[type_of_room] + DISCOUNT * np.max(future_qs)
#                         else:
#                             max_future_q = reward[type_of_room]

#                         action_index = self.action_mapping(action[type_of_room], reversed= True)
#                         # current_qs[0][action_index] += ALPHA * (max_future_q - current_qs[0][action_index])
#                         current_qs[0][action_index] = max_future_q 

#                         X.append(observation[type_of_room][self.observation_indexes])
#                         Y.append(current_qs)

#             self.main_model.fit(np.array(X), np.array(Y), batch_size=batch_size, verbose=0)

        
  


  


  
  
    
    
    
    


        
    

   
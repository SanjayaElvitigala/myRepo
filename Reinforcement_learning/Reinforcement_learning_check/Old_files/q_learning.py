import pandas as pd
import numpy as np

from generic_files.config import * 


class Q_Learning:

  conv_rate_bins = [0,0.01,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1]
  profit_bins = [0,1,1001,2001,3001,4001,5001,6001]
  ROI_bins = [0,0.01,0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00,1.01,1.10,1.20,1.30,1.40,1.50,1.60,1.70,1.80,1.90,2.00]
  all_bins  = [conv_rate_bins, profit_bins, ROI_bins]
  bin_length = 5

  def __init__(self, n_actions, bin_numbers, observation_indexes):
      self.bin_numbers = bin_numbers # specified as a list ex: [0,2] indicates to consider conv_rate_bins and ROI_bins
      self.metric_1_num, self.metric_2_num = observation_indexes[0], observation_indexes[1]
      self.n_actions = n_actions
      self.actions =  [0.95,1,1.05]
      self.Q_dict = self.initialize_Q_table(self.all_bins[bin_numbers[0]], self.all_bins[bin_numbers[1]]) # initialising the q table  
      self.S_dict = self.initialize_S_table( self.all_bins[bin_numbers[0]], self.all_bins[bin_numbers[1]]) # initialising the state table
      self.replay_memory = []
      self.EPSILON = 0.8
      self.epsilon_min = 0.01
      self.epsilon_decay = 0.001
      self.ALPHA = 0.05
      self.DISCOUNT = 0.95


  def update_state_table(self, metrics_list, type):
        bin_pointers = []
        for index, metric in enumerate(metrics_list):
            bin_pointers.append(self.bin_identifier(metric, self.all_bins[index]))
        self.S_dict[bin_pointers[0]][bin_pointers[1]][type]+=1

  def get_state_number(self, metrics_list):
      bin_pointers = []
      for index, metric in enumerate(metrics_list):
        bin_pointers.append(self.bin_identifier(metric, self.all_bins[index]))

      state_num =  self.S_dict[bin_pointers[0]][bin_pointers[1]]['s']
      return state_num

  def bin_identifier(self, metric , bins_list):
      bin_pointer = -1 
      for bin in bins_list:
        if metric < bin:
            bin_pointer = bins_list[bins_list.index(bin)-1]
            break
        elif metric == bin:
            bin_pointer = bin
            break
        else:
            if bin == bins_list[-1]:
                bin_pointer = bin
      return bin_pointer

  def action_mapping(self,action , reversed = False): 
        if reversed:
            action_index = self.actions.index(action)
            return action_index 
        else:
            action_index = action
            return self.actions[action_index]
            

  def take_action(self, observation, action_space):
    actions = {}
    for type_of_room in room_type:
        metrics = [observation[type_of_room][self.metric_1_num], observation[type_of_room][self.metric_2_num]]
        self.update_state_table(metrics, type_of_room)

        if np.random.uniform() > self.EPSILON:
            state_num = self.get_state_number(metrics)
            action_index = np.argmax(list(self.Q_dict[type_of_room][state_num].values()))
            action = self.action_mapping(action_index)
        else:
            action_index = action_space.sample()
            action = self.action_mapping(action_index)
            
        actions[type_of_room] = action

    return actions

 

  def train(self, done):
    ALPHA = self.ALPHA # Learning rate
    DISCOUNT =self.DISCOUNT

    current_state, next_state, actions_by_room_type, reward, done = self.replay_memory[-1]

    for type_of_room in room_type:
        if current_state[type_of_room][0] > 0:
            current_metrics = [current_state[type_of_room][self.metric_1_num], current_state[type_of_room][self.metric_2_num]]
            next_metrics  = [next_state[type_of_room][self.metric_1_num], next_state[type_of_room][self.metric_2_num]]
            current_state_num = self.get_state_number(current_metrics)
            next_state_num = self.get_state_number(next_metrics)
            action = actions_by_room_type[type_of_room]
            if not done:
                max_future_q = reward[type_of_room] + DISCOUNT * np.max(list(self.Q_dict[type_of_room][next_state_num].values()))
            else:
                max_future_q = reward[type_of_room]

            self.Q_dict[type_of_room][current_state_num][action]+= ALPHA *(max_future_q - self.Q_dict[type_of_room][current_state_num][action])
            self.Q_dict[type_of_room][current_state_num][action] = round(self.Q_dict[type_of_room][current_state_num][action],3)


  def initialize_Q_table(self, bin_type_1, bin_type_2):
    actions = [self.action_mapping(i) for i in range(self.n_actions)]
    Q = {}
    Q_full = {}
    n_states = len(bin_type_1) * len(bin_type_2)
    for state in range(n_states):
        Q[state] = {}
        for action in actions:
            Q[state][action] = 0
    for type in room_type.keys():
        Q_full[type] = Q
    return Q_full

  def initialize_S_table(self, bin_type_1, bin_type_2):
    state = {bin_1: {} for bin_1 in bin_type_1}
    i=0
    for bin_1 in bin_type_1:
        for bin_2 in bin_type_2:
            state_num = {'s': i}
            state_num.update({type:0 for type in room_type.keys()})
            state[bin_1][bin_2] = state_num 
            i+=1
    return state


  def dict_to_df(self): # converting Q_table and states_table to dataframes for displaying purposes
    full_Q_dict = self.Q_dict
    S_dict = self.S_dict

    q_cols = ['State']
    for action_index in range(self.n_actions):
        q_cols.append(self.action_mapping(action_index))

    Q_df = pd.DataFrame(columns=q_cols)
    Q_df_full = {type: Q_df for type in room_type.keys()}
    for type in room_type.keys():
      for k,v in full_Q_dict[type].items():
        row_dict =v
        row_dict['State'] = k
        new_row = pd.Series(row_dict)
        Q_df_full[type] = pd.concat([Q_df_full[type],new_row.to_frame().T], ignore_index=True)

    s_cols = ['Conversion']
    for bin in self.all_bins[self.bin_numbers[1]]:
        s_cols.append(bin)

    S_df = pd.DataFrame(columns = s_cols)
    for k_,v_ in S_dict.items():
        row_dict_ = {key: (sum(v_[key].values()) - v_[key]['s']) for key in v_.keys()}
        row_dict_['Conversion'] = k_
        new_row_ = pd.Series(row_dict_)
        S_df = pd.concat([S_df,new_row_.to_frame().T], ignore_index=True)

    return Q_df_full,S_df



 





  
  
    
    
    
    


        
    

   
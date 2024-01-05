import pandas as pd
import numpy as np
from collections import deque

from model_utility_functions import *
from hotel import *
from config import * 
from utility_functions import *



class Pricing_Algo:

  def __init__(self, state_shape, action_shape):

      self.replay_memory = []
      

      self.EPSILON = 0.8
      self.epsilon_decay = 0.001
      self.ALPHA = 0.05
      self.learning_rate = 0.001
      self.DISCOUNT = 0.95
      self.target_ROI_margin = 0.4 # 40 percent ROI margin
      self.target_conversion_rate  = 0.1 # 20 percent conversion rate

      self.batch_start = 0
      self.batch_end = 130

    #   self.main_model = tf.keras.models.load_model('dqn_mod2.h5') 
      self.main_model =create_model(self.learning_rate ,state_shape, action_shape) 
      self.target_model = create_model(self.learning_rate ,state_shape, action_shape)
      self.target_model.set_weights(self.main_model.get_weights())

      

  def get_reward(self, conversion, expected_ROI):
      reward_tracker = 0
 
      conv_rewards = 4  if conversion >= self.target_conversion_rate else -2
      ROI_rewards = 2 if expected_ROI >= self.target_ROI_margin else -10
    
      reward_tracker = conv_rewards + ROI_rewards
      return reward_tracker

  def set_price(self, hotel_obj, action):
    for type_of_room in room_type:
        if action[type_of_room] == 0 :
            selected_action = 0.95
        elif action[type_of_room] == 1 : 
            selected_action = 1
        elif action[type_of_room] == 2:
            selected_action = 1.05
        room_price = type_of_room+'_price'
        setattr(hotel_obj, room_price, getattr(hotel_obj,room_price)*selected_action)


  def take_action(self,observation, action_space):
        actions_dict = {}
        for type_of_room in room_type.keys():
            if np.random.uniform() > self.EPSILON:
                  
                    encoded = observation[type_of_room]
                    encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
                    predicted = self.main_model.predict(encoded_reshaped).flatten()
                    actions_dict[type_of_room] = np.argmax(predicted)
            else:
                actions_dict[type_of_room] = action_space.sample()
        
        return actions_dict
        
  


  


  
  
    
    
    
    


        
    

   
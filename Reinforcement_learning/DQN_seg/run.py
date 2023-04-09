import numpy as np

import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from generic_files.config import *
from DQN_seg.simulation_env import * 
from DQN_seg.deep_q_learning import *
from generic_files.utility_functions import *

n_episodes = 1
def run(n_customers,simulation_days, simulation_time,cancellation_rate,input_room_list, compare = False):
    a = time.time()
    is_training = False

    simu_env = Simulation_Env(n_customers, simulation_days, simulation_time,cancellation_rate,input_room_list, compare = compare)

    model = DQN(4+10, 5, observation_indexes= [0,1,3,6], is_training= is_training)
    
    total_reward = []
    epsilon_values = []
    steps_to_update_models = 0
    for episode in range(1,n_episodes+1):
        total_epi_reward = 0
        observation  = simu_env.reset()

        done = False
        while not done:
            steps_to_update_models += 1

            actions_by_room_type = model.take_action(observation, model.action_indexes)
            next_state,reward,done,info = simu_env.step(actions_by_room_type)

            model.store_data(observation, next_state, actions_by_room_type, reward, done)
            

            total_epi_reward+=unpack_reward(reward)
            observation = next_state


            if (steps_to_update_models % 4 == 0 or done) and is_training:
                model.train(done)
            
            if (steps_to_update_models % 10 == 0) and is_training:
                model.target_model.load_state_dict(model.main_model.state_dict())
                    # for index,t_model in enumerate(model.target_models):
                    #     t_model.load_state_dict(model.main_models[index].state_dict())

            # eps_decay_start_day = int(simulation_time- (0.9/(model.epsilon_decay* (n_episodes/2)) ))  if n_episodes>=3 else 60
            # if (simu_env.time_step > eps_decay_start_day) and (model.EPSILON > model.epsilon_min):
            #     model.EPSILON-= model.epsilon_decay

            simu_env.update_timestep()

        total_reward.append(total_epi_reward)
        epsilon_values.append(model.EPSILON)
        print(f'episode : {episode} reward : {total_epi_reward} , cost: {model.cost_tracker}, epsilon : {model.EPSILON}')
        if is_training:
            torch.save(model.main_model.state_dict(), f'DQN\models\model.pkl')
            # for index,m_model in enumerate(model.main_models):
            #     torch.save(m_model.state_dict(), f'DQN\models\model_seg_{index}.pkl')
        if episode%6==0 and model.EPSILON>= model.epsilon_min:
            model.EPSILON-= model.epsilon_decay
    reward_df = pd.DataFrame({'epi': [i for i in range(1,n_episodes+1)], 'Reward': total_reward, 'Epsilon': epsilon_values})

        
    rl_df,base_df= simu_env.render()
    arrival_df = simu_env.customer_handler.arrival_real
    
    b = time.time()
    print(f'time_taken : {(b-a)} secs')
    print('___________________END___________________')   
   
    return  reward_df, rl_df, base_df, arrival_df


   
            


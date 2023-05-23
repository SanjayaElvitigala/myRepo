import numpy as np
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from generic_files.config import *
from Qlearning.simulation_env import * 
from Qlearning.q_learning import *
from generic_files.utility_functions import *

n_episodes = 4
def run(n_customers,simulation_days, simulation_time, cancellation_rate,input_room_list, compare=False):
    a = time.time()

    simu_env = Simulation_Env(n_customers, simulation_days, simulation_time,cancellation_rate,input_room_list,compare= compare)
    model = Q_Learning(simu_env.action_space.n, bin_numbers=[0,1], observation_indexes= [2,3])

    total_reward = []
    epsilon_values = []
    steps_to_update_models = 0
    for episode in range(1,n_episodes+1):
        total_epi_reward = 0
        observation  = simu_env.reset(episode, n_episodes)

        done = False
        while not done:
            steps_to_update_models += 1

            actions_by_room_type = model.take_action(observation, simu_env.action_space)
            next_state,reward,done,info = simu_env.step(actions_by_room_type)

            model.replay_memory.append([observation, next_state, actions_by_room_type, reward, done])

            total_epi_reward+=sum(reward.values())
            observation = next_state

            model.train(done)

            eps_decay_start_day = 70
            if (simu_env.time_step > eps_decay_start_day) and (model.EPSILON > model.epsilon_min):
                model.EPSILON-= model.epsilon_decay

            simu_env.update_timestep()

        total_reward.append(total_epi_reward)
        epsilon_values.append(model.EPSILON)

        print(f'episode : {episode} reward : {total_epi_reward} , epsilon : {model.EPSILON}')

      


    reward_df = pd.DataFrame({'epi': [i for i in range(1,n_episodes+1)], 'Reward': total_reward, 'Epsilon': epsilon_values})

        
    rl_df,base_df= simu_env.render()

    arrival_df = simu_env.customer_handler.arrival_real

    # q_df_full , s_df = pricing_algorithm.dict_to_df()
    b = time.time()
    print(f'time_taken : {(b-a)} secs')
    print('___________________END___________________')  
   
    return  reward_df, rl_df, base_df, arrival_df #, q_df_full, s_df


   
            


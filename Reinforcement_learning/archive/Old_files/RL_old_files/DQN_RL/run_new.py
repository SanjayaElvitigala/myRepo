import numpy as np
import pandas as pd



from simulation_env import * 
from utility_functions import *
from model_utility_functions import *

n_episodes = 3
def run(n_customers, simulation_time,cancellation_rate,input_room_list):

    simu_env = Simulation_Env(n_customers, simulation_time,cancellation_rate,input_room_list)
 
    total_reward = []
    epsilon_values = []
    steps_to_update_models = 0
    for episode in range(n_episodes):
        total_epi_reward = 0
        observation  = simu_env.reset()
        time_step = 0
        done = False
        while not done:
            steps_to_update_models += 1

            actions_by_room_type = simu_env.pricing_algorithm.take_action(observation, simu_env.action_space)
            next_state,reward,done,info = simu_env.step(actions_by_room_type,time_step)
            simu_env.pricing_algorithm.replay_memory.append([observation, next_state, actions_by_room_type, reward, done])

            if steps_to_update_models % 4 == 0 or done:
                train(simu_env.pricing_algorithm,done)

            observation = next_state
            total_epi_reward+=sum(reward.values())
            
            

            if steps_to_update_models % 12 == 0:
                    simu_env.pricing_algorithm.target_model.set_weights(simu_env.pricing_algorithm.main_model.get_weights())
   
            if time_step > 150 and simu_env.pricing_algorithm.EPSILON>0.02:
                simu_env.pricing_algorithm.EPSILON-= simu_env.pricing_algorithm.epsilon_decay

            if time_step < simulation_time-1:
                time_step+=1
            
            

     

        total_reward.append(total_epi_reward)
        epsilon_values.append(simu_env.pricing_algorithm.EPSILON)
        simu_env.pricing_algorithm.main_model.save(f'h5_files\dqn_{episode}.h5')
    


    rew_df = pd.DataFrame({'epi': [i for i in range(n_episodes)], 'Reward': total_reward, 'Epsilon': epsilon_values})

        
    rl_df,base_df= simu_env.render()

    arrival_df = simu_env.customer_handler.arrival_real
   
    return  rew_df, rl_df, base_df, arrival_df


   
            


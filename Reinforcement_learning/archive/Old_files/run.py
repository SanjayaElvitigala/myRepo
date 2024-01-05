import numpy as np
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from generic_files.config import *
from combined_RL.simulation_env import * 
from combined_RL.q_learning import *
from combined_RL.deep_q_learning import *
from generic_files.utility_functions import *

n_episodes = 2
def run(n_customers, simulation_time,cancellation_rate,input_room_list):
    a = time.time()
    using_qtab = False
    is_training = False

    simu_env = Simulation_Env(n_customers, simulation_time,cancellation_rate,input_room_list)

    if using_qtab:
        model = Q_Learning(simu_env.action_space.n, bin_numbers=[0,1], observation_indexes= [2,3])
    else:
        model = DQN(4, 3, observation_indexes= [0,1,3,6], is_training= is_training)
    
    total_reward = []
    epsilon_values = []
    steps_to_update_models = 0
    for episode in range(1,n_episodes+1):
        total_epi_reward = 0
        observation  = simu_env.reset()

        done = False
        while not done:
            steps_to_update_models += 1

            actions_by_room_type = model.take_action(observation, simu_env.action_space)
            next_state,reward,done,info = simu_env.step(actions_by_room_type)

            model.replay_memory.append([observation, next_state, actions_by_room_type, reward, done])

            total_epi_reward+=sum(reward.values())
            observation = next_state

            if using_qtab:
                model.train(done)

            if (steps_to_update_models % 4 == 0 or done) and not using_qtab and is_training:
                model.train(done)
            
            if (steps_to_update_models % 13 == 0) and not using_qtab and is_training:
                    # model.target_model.set_weights(model.main_model.get_weights())
                    model.target_model.load_state_dict(model.main_model.state_dict())

            eps_decay_start_day = int(simulation_time- (0.9/(model.epsilon_decay* (n_episodes/2)) ))  if n_episodes>=3 else 60
            if (simu_env.time_step > eps_decay_start_day) and (model.EPSILON > model.epsilon_min):
                model.EPSILON-= model.epsilon_decay

            simu_env.update_timestep()

        total_reward.append(total_epi_reward)
        epsilon_values.append(model.EPSILON)

        print(f'episode : {episode} reward : {total_epi_reward} , epsilon : {model.EPSILON}')
    if is_training and not using_qtab:
        torch.save(model.main_model.state_dict(), 'combined_RL\h5_files\model.pkl')
        # model.main_model.save(f'combined_RL\h5_files\dqn_model.h5')
    b = time.time()
    print(f'time_taken : {(b-a)/60} mins')
    print('___________________END___________________')    


    reward_df = pd.DataFrame({'epi': [i for i in range(1,n_episodes+1)], 'Reward': total_reward, 'Epsilon': epsilon_values})

        
    rl_df,base_df= simu_env.render()

    arrival_df = simu_env.customer_handler.arrival_real

    # q_df_full , s_df = pricing_algorithm.dict_to_df()
   
    return  reward_df, rl_df, base_df, arrival_df #, q_df_full, s_df


   
            


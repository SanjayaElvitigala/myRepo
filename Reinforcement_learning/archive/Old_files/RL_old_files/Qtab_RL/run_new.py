import numpy as np
import pandas as pd



from simulation_env import *
from base_simulation_env import *
from utility_functions import *

n_episodes = 5
def run(n_customers, simulation_time,cancellation_rate,input_room_list):

    simu_env = Simulation_Env(n_customers, simulation_time,cancellation_rate,input_room_list)
    base_simu_env  = Base_Simulation_Env(n_customers, simulation_time,cancellation_rate,input_room_list)
    total_reward = []
    epsilon_values = []

    for episode in range(n_episodes):
        simu_env.reset()
        base_simu_env.reset(episode,n_episodes, simu_env.customer_handler.daily_search_day)
        done = False
        time_step =0
        while not done:
            simu_env.step(time_step)
            base_simu_env.step(time_step,episode,n_episodes)

            if time_step < simu_env.simulation_time-1:
                    time_step+=1
            elif time_step == simu_env.simulation_time-1:
                done =True
        total_reward.append(simu_env.hotel_handler.total_epi_reward)
        epsilon_values.append(simu_env.hotel_handler.EPSILON)
        
    # calling the dict_to_df function in utility functions file
    Q_df_all, S_df = dict_to_df(simu_env.hotel_handler.Q_dict, simu_env.hotel_handler.S_dict, simu_env.hotel_handler.profit_bins )

    rew_df = pd.DataFrame({'epi': [i for i in range(n_episodes)], 'Reward': total_reward, 'Epsilon': epsilon_values})


    customer_df, metrics_df, booking_rec_df, booking_rec_df_melt = simu_env.render()
    base_model_dataframes = base_simu_env.render()


    arrival_df = simu_env.customer_handler.arrival_real
   
    return Q_df_all, S_df, rew_df, customer_df, metrics_df, booking_rec_df, booking_rec_df_melt, arrival_df, base_model_dataframes


   
            


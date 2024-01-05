import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#import plotly.express as px

from run_new import *
from config import *

st.write(""" 
# Hotel Booking Simulation
""")

st.sidebar.write("""
### Please enter your expected values here
""")

# strealit inputs
n_customers = st.sidebar.slider('Expected number of Customers' , 3500, 10000, 3500)
simulation_time = st.sidebar.slider('Number of Days' , 31, 1000, 365)
input_room_list=[]
for i in room_type:
  name_room_count=i+'_count'
  locals()[name_room_count]= st.sidebar.slider(name_room_count , 5, 50, 15)
  input_room_list.append(locals()[name_room_count])

cancellation_rate = st.sidebar.slider("Cancellation Rate (%)", 0, 100, 0)

Simulate = st.button(label="Simulate")
if Simulate:
  #, customer_df, rl_df[1], booking_rec_df, booking_rec_df_melt,arrival_df
  rew_df, rl_df, base_df, arrival_df= run(n_customers, simulation_time,cancellation_rate,input_room_list)
  st.write(f"""
  Following data and visualisations is from a simulation of ***{n_customers} customers*** coming into a hotel  and attempting to book within a timeline of ***{simulation_time} days***.
  """)
  st.write(f""" 
  ### RL agent
  1. Mean daily Occupancy rate = {rl_df[1]['Occupancy_rate'].sum()/len(arrival_df)}
  2. Mean daily profit = {rl_df[1]['Profit'].sum()/len(arrival_df)}
  3. Mean daily revenue = {rl_df[1]['Daily_Revenue'].sum()/len(arrival_df)}

  ### Base model
  1. Mean daily Occupancy rate = {base_df[1]['Occupancy_rate'].sum()/len(arrival_df)}
  2. Mean daily profit = {base_df[1]['Profit'].sum()/len(arrival_df)}
  3. Mean daily revenue = {base_df[1]['Daily_Revenue'].sum()/len(arrival_df)}
  """)
  st.dataframe(rew_df)



  st.write(""" ### Customer Data 
  ***Note:***
  1. Booking Status being 1 means a successfull booking and 0 otherwise.
  2. Entries with -1 in some of the columns indicate that those customers were unable to book and for these customers number of attempts, search day and expected stay duration are recorded.
  """) 
  st.write(' ### RL agent customer data')
  st.dataframe(data = rl_df[0])
  st.write(' ### Base model customer data')
  st.dataframe(data = base_df[0])

  st.write(""" ### Daily Booking Data 

  This shows how many customers failed and succeeded in the booking process. The total number of customers coming in equals to the addition of failed and succeeded counts.

  """)
  st.dataframe(data = rl_df[2])

  st.write("""
  ### Data related to Metrics
  ***Note:***
  1. ***Average Daily Rate*** has been calculated using division of ***Daily Revenue*** by the ***Number of Booked Rooms*** for a particular stay_day.
  2. ***Occupancy Rate*** has been calculated using division of ***Number of Booked Rooms*** by ***Number of Total Rooms*** for each of the stay_days.
  """)
  st.dataframe(rl_df[1])

  st.write('''### Arrival Distribution by day''')
  st.dataframe(arrival_df)

  plt.rcParams["figure.figsize"] = (12,8)

  fig1, ax_1, = plt.subplots(figsize = (15 ,8) )
  sns.barplot(x="stay_day", y='Occupancy_rate', data=rl_df[1], ax=ax_1)

  fig2, ax_2, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data=rl_df[1].Profit, ax = ax_2)

  fig3, ax_3, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data=rl_df[1].Daily_Revenue, ax = ax_3)

  fig4, ax_4, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data=rl_df[1].Average_daily_rate, ax = ax_4)

  fig5, ax_5, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot( x = 'Day', y = 'value', hue = 'variable', data = rl_df[3], ax = ax_5)

  fig6, ax_6, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data = arrival_df['Arrival_count'] , ax = ax_6)


  fig7, ax_7, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data=rl_df[2]['Search_day_count'] , ax = ax_7)

  st.write('### Occupancy Rate')
  st.pyplot(fig1)
  st.write('### Profit')
  st.pyplot(fig2)
  st.write('### Daily Revenue')
  st.pyplot(fig3)
  st.write('### Average Daily Rate')
  st.pyplot(fig4)
  st.write('### Counts of Failed Customers vs Booked Customers')
  st.pyplot(fig5)
  st.write('### Arrival Count')
  st.pyplot(fig6)
  st.write('### Search Day Count')
  st.pyplot(fig7)

  

else:
    st.write('### Please input values and click Simulate')

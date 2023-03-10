import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt

from generic_files.config import *
from generic_files.hotel import *

from generic_files.customer import *
from generic_files.customer_handler import *
from generic_files.utility_functions import *
import plotly.express as px



st.write(""" 
# Hotel Booking Simulation
""")

st.sidebar.write("""
### Please enter your expected values here
""")
st.write('#### Please input a integer weight value for the Holidays within the date range selected.')
st.write('***eg : if you put 5 as the value for a particular holiday and customer segment, this means you will expect extra 5 customers on this holiday as well as 5 days period prior to this holiday. You can apply the week end weights in the same way.***')
# strealit inputs
col1,col2,col3,col4 = st.columns(4)
with col1:
        weekend_weight = st.number_input('Week end weight',step = 1, min_value = 1) 

n_customers = st.sidebar.slider('Expected number of Customers' , 7500, 20000, 10000)
start_date = st.sidebar.date_input('Start Date', value= dt.date(2023,1,1))
end_date = st.sidebar.date_input('End Date', min_value =start_date+dt.timedelta(2), value= dt.date(2024,1,1))

input_room_list=[]
for i in room_type:
  name_room_count=i+'_count'
  locals()[name_room_count]= st.sidebar.slider(name_room_count , 5, 50, 35)
  input_room_list.append(locals()[name_room_count])

cancellation_rate = st.sidebar.slider("Cancellation Rate (%)", 0, 100, 0)
model_name=st.sidebar.selectbox("Select Model",('DQN','Qlearning'))

output_list = create_holiday_dataframe(start_date, end_date, weekend_weight)

if 'holiday_df' not in st.session_state:
      st.session_state['holiday_df'] = output_list[0] 
default_holiday_df = st.session_state['holiday_df']
  
holiday_df = process_holiday_dataframe(default_holiday_df)

Simulate = st.button(label="Simulate")

simulation_time = output_list[2]
simulation_days = output_list[1]


imported_module_run = __import__(model_name+'.run')

if Simulate:
  #, customer_df, rl_df[1], booking_rec_df, booking_rec_df_melt,arrival_df
  reward_df, rl_df, base_df, arrival_df= imported_module_run.run.run(n_customers, simulation_days, holiday_df, simulation_time, cancellation_rate, input_room_list)
  st.write(f"""
  Following data and visualisations is from a simulation of ***{n_customers} customers*** coming into a hotel  and attempting to book within a timeline of ***{simulation_time} days***.
  """)

  comparison_df=comparison_df(rl_df,base_df)
  distribution_df=distribution_df(rl_df,base_df)

  rl_df[1]['cumulative_profit']=rl_df[1]['Profit'].cumsum()
  base_df[1]['cumulative_profit']=base_df[1]['Profit'].cumsum()
  rl_df[1]['chain']='RL agent'
  base_df[1]['chain']='Base model'
  full_metrics_df=pd.concat([rl_df[1],base_df[1]])

  rl_df[3]['variable']=rl_df[3]['variable']+'_RL_agent'
  base_df[3]['variable']=base_df[3]['variable']+'_Base_model'
  full_booking_rec_df_melt=pd.concat([rl_df[3],base_df[3]])

  rl_df[2]['chain']='RL agent'
  base_df[2]['chain']='Base model'
  full_booking_rec_df=pd.concat([rl_df[2],base_df[2]])
  
  fig = px.bar(comparison_df, x="Room_type", y=["RL_agent_mean_occupancy_rate",'Base_model_mean_occupancy_Rate'],barmode='group', title="Mean occupancy rate by room type")
  fig.update_layout(yaxis_title="Mean Occupancy Rate")
  st.plotly_chart(fig, use_container_width=True)
  
  fig = px.bar(comparison_df, x="Room_type", y=["RL_agent_mean_revenue",'Base_model_mean_revenue'],barmode='group', title="Mean daily revenue by room type")
  fig.update_layout(yaxis_title="Mean Daily Revenue")
  st.plotly_chart(fig, use_container_width=True)

  fig = px.bar(comparison_df, x="Room_type", y=["RL_agent_mean_profit",'Base_model_mean_profit'],barmode='group', title="Mean profit by room type")
  fig.update_layout(yaxis_title="Mean Daily Profit")
  st.plotly_chart(fig, use_container_width=True)
 

  for i in room_type:
     fig=px.line(rl_df[5],y=i,title=f'{i} price Change over time')
     st.plotly_chart(fig, use_container_width=True)

 

  fig = px.line(full_metrics_df, x='stay_day', y="Occupancy_rate", color='chain', title='Occupancy rate')
  st.plotly_chart(fig, use_container_width=True)
  
  fig = px.line(full_metrics_df, x='stay_day', y="cumulative_profit", color='chain', title='Profit ')
  st.plotly_chart(fig, use_container_width=True)

  fig = px.line(full_metrics_df, x='stay_day', y="Daily_Revenue", color='chain', title='Daily Revenue')
  st.plotly_chart(fig, use_container_width=True)

  fig = px.line(full_metrics_df, x='stay_day', y="Average_daily_rate", color='chain', title='Average daily rate')
  st.plotly_chart(fig, use_container_width=True)

 

  
  fig = px.line(full_booking_rec_df_melt, x='Day', y="value", color='variable', title='Counts of Failed Customers vs Booked Customers')
  st.plotly_chart(fig, use_container_width=True)

  

  fig = px.line(full_booking_rec_df, x='Day', y="Search_day_count", color='chain', title='Search Day Count')
  st.plotly_chart(fig, use_container_width=True)
  
  st.write('''### Comparison of RL agent and base model''')
  st.dataframe(comparison_df)
 

  st.write('''### Customer distribution by hotel''')
  st.dataframe(distribution_df)

  st.write('''### Reward df''')
  st.dataframe(reward_df)



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
  st.dataframe(base_df[1])

  st.write('''### Arrival Distribution by day''')
  st.dataframe(arrival_df)
  st.write(arrival_df['Arrival_count'].sum())
 



else:
    st.write('### Please input values and click Simulate')
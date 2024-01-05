import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
n_customers = st.sidebar.slider('Expected number of Customers' , 100, 10000, 200)
simulation_time = st.sidebar.slider('Number of Days' , 31, 1000, 365)
input_room_list=[]
for i in room_type:
  name_room_count=i+'_count'
  locals()[name_room_count]= st.sidebar.slider(name_room_count , 5, 50, 5)
  input_room_list.append(locals()[name_room_count])

cancellation_rate = st.sidebar.slider("Cancellation Rate (%)", 0, 100, 10)

Simulate = st.button(label="Simulate")
if Simulate:
  
  Q_df, S_df, rew_df, customer_df, metrics_df, booking_rec_df, booking_rec_df_melt,arrival_df,base_model_dataframes= run(n_customers, simulation_time,cancellation_rate,input_room_list)
  st.write(f"""
  Following data and visualisations is from a simulation of ***{n_customers} customers*** coming into a hotel  and attempting to book within a timeline of ***{simulation_time} days***.
  """)
  st.write(f""" 
  ### RL agent
  1. Mean daily Occupancy rate = {metrics_df['Occupancy_rate'].sum()/len(arrival_df)}
  2. Mean daily profit = {metrics_df['Profit'].sum()/len(arrival_df)}
  3. Mean daily revenue = {metrics_df['Daily_Revenue'].sum()/len(arrival_df)}

  ### Base model
  1. Mean daily Occupancy rate = {base_model_dataframes[1]['Occupancy_rate'].sum()/len(arrival_df)}
  2. Mean daily profit = {base_model_dataframes[1]['Profit'].sum()/len(arrival_df)}
  3. Mean daily revenue = {base_model_dataframes[1]['Daily_Revenue'].sum()/len(arrival_df)}
  """)
  st.dataframe(rew_df)
  st.dataframe(Q_df['single_room'])
  st.dataframe(S_df)


  st.write(""" ### Customer Data 
  ***Note:***
  1. Booking Status being 1 means a successfull booking and 0 otherwise.
  2. Entries with -1 in some of the columns indicate that those customers were unable to book and for these customers number of attempts, search day and expected stay duration are recorded.
  """) 
  st.write(' ### RL agent customer data')
  st.dataframe(data = customer_df)
  st.write(' ### Base model customer data')
  st.dataframe(data=base_model_dataframes[0] )

  st.write(""" ### Daily Booking Data 

  This shows how many customers failed and succeeded in the booking process. The total number of customers coming in equals to the addition of failed and succeeded counts.

  """)
  st.dataframe(data = booking_rec_df)

  st.write("""
  ### Data related to Metrics
  ***Note:***
  1. ***Average Daily Rate*** has been calculated using division of ***Daily Revenue*** by the ***Number of Booked Rooms*** for a particular stay_day.
  2. ***Occupancy Rate*** has been calculated using division of ***Number of Booked Rooms*** by ***Number of Total Rooms*** for each of the stay_days.
  """)
  st.dataframe(metrics_df)

  st.write('''### Arrival Distribution by day''')
  st.dataframe(arrival_df)

  plt.rcParams["figure.figsize"] = (12,8)

  #fig1, ax_1, = plt.subplots(figsize = (15 ,8) )
  #sns.barplot(x="stay_day", y='Occupancy_rate', data=metrics_df, ax=ax_1)

  #fig2, ax_2, = plt.subplots(figsize = (15 ,8) )
  #sns.lineplot(data=metrics_df.Profit, ax = ax_2)

  #fig3, ax_3, = plt.subplots(figsize = (15 ,8) )
  #sns.lineplot(data=metrics_df.Daily_Revenue, ax = ax_3)

  #fig4, ax_4, = plt.subplots(figsize = (15 ,8) )
  #sns.lineplot(data=metrics_df.Average_daily_rate, ax = ax_4)

  fig5, ax_5, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot( x = 'Day', y = 'value', hue = 'variable', data = booking_rec_df_melt, ax = ax_5)

  #fig6, ax_6, = plt.subplots(figsize = (15 ,8) )
  #sns.lineplot(data = arrival_df['Arrival_count'] , ax = ax_6)


  fig7, ax_7, = plt.subplots(figsize = (15 ,8) )
  sns.lineplot(data=booking_rec_df['Search_day_count'] , ax = ax_7)

  # chart = st.line_chart(chart_data)
  # testing animated graph

  


  data = metrics_df.Profit  
  data



  ### 
  '''
  def plot_sales(self):
    names = list(self.sales.keys())

    fig = go.Figure(data=[go.Scatter(name=names[0],x=self.sales.index,y=self.sales[names[0]]),go.Scatter(name=names[1],x=self.sales.index,y=self.sales[names[1]])])

    fig.update_yaxes(title_text="Number of Sales")
    fig.update_xaxes(title_text="date")

    return fig '''

  #print(data.loc[5])


  frames = []
  for frame in range(1,375):
    x_axis_frame = np.arange(frame)

    y_axis_frame = list(data.iloc[1:frame])

    curr_frame = go.Frame(data = [go.Scatter(x = x_axis_frame, y=y_axis_frame, mode="lines")])
    frames.append(curr_frame)
    

  figure = go.Figure(
    data = [go.Scatter(x=np.array([1]), y=np.array([603]), mode="lines")],
    layout = {"title": "Line chart",
              "updatemenus": [{"type":"buttons",
                              "buttons":[{"label":"Play",
                                          "method":"animate",
                                          "args":[None]}]}],
              "xaxis":{"range":[0,data.shape[0]]}},
    frames = frames

  )

  st.write("#### Profit")
  profit_chart = st.empty()

  profit_chart.plotly_chart(figure)

#####################


  data1 = metrics_df.Occupancy_rate
  
  frames1 = []
  for frame in range(1,375):
    x_axis_frame = np.arange(frame)

    y_axis_frame = list(data1.iloc[1:frame])

    curr_frame1 = go.Frame(data = [go.Scatter(x = x_axis_frame, y=y_axis_frame, mode="lines")])
    frames1.append(curr_frame1)
    

  fig_occupancy = go.Figure(
    data = [go.Scatter(x=np.array([1]), y=np.array([603]), mode="lines")],
    layout = {"title": "Line chart",
              "updatemenus": [{"type":"buttons",
                              "buttons":[{"label":"Play",
                                          "method":"animate",
                                          "args":[None]}]}],
              "xaxis":{"range":[0,data1.shape[0]]}},
    frames = frames1

  )

  st.write("#### Occupancy Rate")
  occupancy_chart = st.empty()

  occupancy_chart.plotly_chart(fig_occupancy)

  #figure.show()

##################

  data2 = metrics_df.Daily_Revenue
  
  frames2 = []
  for frame in range(1,375):
    x_axis_frame = np.arange(frame)

    y_axis_frame = list(data2.iloc[1:frame])

    curr_frame2 = go.Frame(data = [go.Scatter(x = x_axis_frame, y=y_axis_frame, mode="lines")])
    frames2.append(curr_frame2)
    

  fig_daily_rev = go.Figure(
    data = [go.Scatter(x=np.array([1]), y=np.array([603]), mode="lines")],
    layout = {"title": "Line chart",
              "updatemenus": [{"type":"buttons",
                              "buttons":[{"label":"Play",
                                          "method":"animate",
                                          "args":[None]}]}],
              "xaxis":{"range":[0,data2.shape[0]]}},
    frames = frames2

  )

  st.write("#### Daily Revenue")
  daily_rev_chart = st.empty()

  daily_rev_chart.plotly_chart(fig_daily_rev)

####################


  data3 = metrics_df.Average_daily_rate
  
  frames3 = []
  for frame in range(1,375):
    x_axis_frame = np.arange(frame)

    y_axis_frame = list(data3.iloc[1:frame])

    curr_frame3 = go.Frame(data = [go.Scatter(x = x_axis_frame, y=y_axis_frame, mode="lines")])
    frames3.append(curr_frame3)
    

  fig_avg_daily_rate = go.Figure(
    data = [go.Scatter(x=np.array([1]), y=np.array([603]), mode="lines")],
    layout = {"title": "Line chart",
              "updatemenus": [{"type":"buttons",
                              "buttons":[{"label":"Play",
                                          "method":"animate",
                                          "args":[None]}]}],
              "xaxis":{"range":[0,data3.shape[0]]}},
    frames = frames3

  )

  st.write("#### Average Daily Rate")
  avg_daily_rate_chart = st.empty()

  avg_daily_rate_chart.plotly_chart(fig_avg_daily_rate)


#####################


  data4 = arrival_df['Arrival_count']
  
  frames4 = []
  for frame in range(1,375):
    x_axis_frame = np.arange(frame)

    y_axis_frame = list(data4.iloc[1:frame])

    curr_frame4 = go.Frame(data = [go.Scatter(x = x_axis_frame, y=y_axis_frame, mode="lines")])
    frames4.append(curr_frame4)
    

  fig_arrival_count = go.Figure(
    data = [go.Scatter(x=np.array([1]), y=np.array([603]), mode="lines")],
    layout = {"title": "Line chart",
              "updatemenus": [{"type":"buttons",
                              "buttons":[{"label":"Play",
                                          "method":"animate",
                                          "args":[None]}]}],
              "xaxis":{"range":[0,data4.shape[0]]}},
    frames = frames4

  )

  st.write("#### Arrival count")
  arrival_count = st.empty()

  arrival_count.plotly_chart(fig_arrival_count)





  #st.write('### Occupancy Rate')
  #st.pyplot(fig1)
  #st.write('### Profit')
  #st.pyplot(fig2)
  #st.write('### Daily Revenue')
  #st.pyplot(fig3)
  #st.write('### Average Daily Rate')
  #st.pyplot(fig4)
  st.write('### Counts of Failed Customers vs Booked Customers')
  st.pyplot(fig5)
  #st.write('### Arrival Count')
  #st.pyplot(fig6)
  st.write('### Search Day Count')
  st.pyplot(fig7)

  

else:
    st.write('### Please input values and click Simulate')

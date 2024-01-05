import pandas as pd
import datetime as dt

is_simu_h_df = True # A boolean for specifying whether using the simulated holiday df or actual holiday df

# _____________________________STREAMLIT CONFIG VALUES__________________________________________________________________________________________________
min_expected_cust, default_cust, max_expected_cust = 7500, 20000, 400000
default_start_date = dt.date(2019,1,1)
default_end_date = dt.date(2020,1,1)
 

#_______________________________________________________________________________________________________________________________________________________

# _____________________________CUSTOMER CONFIG VALUES__________________________________________________________________________________________________
e_suffix = '_e_lambda' # suffix for the effective lambda value creation
leadtime_low_lim, leadtime_up_lim = 4, 14  # Customer booking gap lower limit and upper limit
stay_dur_lambda = 2.206 # lambda value for the poisson distribution from which stay duration value is sampled
rvalue_appr_low_lim , rvalue_appr_up_lim = 1, 1.15 # room value appreciation rate limits of customers if they are likely to increase their perceived value
#customer segments and their price with discount
customer_segments = {'Ret':{'price':1.0},
                    'Corp':{'price':0.9},
                    'Leisure':{'price':1.0},
                    'OTA':{'price':0.9},
                    'Discount':{'price':0.85},
                    'Promo':{'price':0.85},
                    'Group':{'price':0.8},
                    'Consortia':{'price':0.8},
                    'Misc':{'price':1.0}
                    }
# start day and end day of each month when looping for 365 days : 0 1 2 .... 364
month_start_end_days = { 1: [0,30], 2: [31,58], 3:[59,89], 4:[90,119] , 
                        5:[120,150], 6:[151,180], 7:[181,211], 8:[212,242], 
                        9:[243,272], 10:[273,303], 11:[304,333], 12: [334,364]}

#  # dataframe to specify the daily lambda for each month

# per_month_base_daily_lambda = pd.DataFrame({'month':[i for i in range(1,13)], 'base_lambda': [1 for i in range(1,13)]}) 
#_______________________________________________________________________________________________________________________________________________________


# _____________________________HOTEL CONFIG VALUES__________________________________________________________________________________________________
#  add needed room type to get it in to the system
room_type={'single_room':{'type_no':1 ,'price':[97,101],'cost':60,'cus_will_pay':[100,1]},
            'double_room':{'type_no':2 ,'price':[196,202],'cost':110,'cus_will_pay':[200,1]},
           'luxury_room':{'type_no':3 ,'price':[220,225],'cost':150,'cus_will_pay':[222,1]}

            }
#no of hotel defined
number_of_hotels=1

hotel_daily_cost=450

min_room_cnt, default_room_cnt, max_room_cnt = 5, 49, 250 # room counts for each room type given to streamlit slider

#_______________________________________________________________________________________________________________________________________________________
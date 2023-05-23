import pandas as pd


#  add needed room type to get it in to the system

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

room_type={'single_room':{'type_no':1 ,'price':[97,101],'cost':60,'cus_will_pay':[100,6]},
            'double_room':{'type_no':2 ,'price':[196,202],'cost':110,'cus_will_pay':[200,6]},
           'luxury_room':{'type_no':3 ,'price':[220,225],'cost':150,'cus_will_pay':[222,6]}

            }

# start day and end day of each month when looping for 365 days : 0 1 2 .... 364
month_start_end_days = { 1: [0,30], 2: [31,58], 3:[59,89], 4:[90,119] , 
                        5:[120,150], 6:[151,180], 7:[181,211], 8:[212,242], 
                        9:[243,272], 10:[273,303], 11:[304,333], 12: [334,364]}

 # dataframe to specify the daily lambda for each month

per_month_base_daily_lambda = pd.DataFrame({'month':[i for i in range(1,13)], 'base_lambda': [1 for i in range(1,13)]}) 

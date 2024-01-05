import numpy as np
import pandas as pd


from customer import *
from config import *


class Customer_Handler:
    cust_segments_list = list(customer_segments.keys())
    def __init__(self,n_customers, simulation_time):
        self.simulation_time = simulation_time
        self.n_customers = n_customers
        
        self.customers = [Customer( i+1) for i in range(n_customers)]
        self.customers_by_seg = { seg:[] for seg in self.cust_segments_list }
        for cust in self.customers:
           self.customers_by_seg[cust.segment].append(cust)

        self.df_holiday = pd.read_csv("holiday_weights.csv")
        self.year_customers = []
        self.daily_customers = {i:[] for i in range(simulation_time)}
        self.daily_search_day={i:[] for i in range(simulation_time)}

        self.customers_dict, self.arrival_real, self.df_holiday_updated = self.customer_sampling_daily()
        

    def preparing_daily_customers(self):
        for day in range(self.simulation_time):
            if day in self.customers_dict.keys():
                sample_dict= self.customers_dict[day]  # accessing the customers by segment for the current day

                if sample_dict:
                    keys, values = zip(*sample_dict.items())
                    for i in values: # accessing the list in the values tuple
                        for j in i:    # iterating over each element in the list of the tuple
                            self.daily_customers[day].append(j)
        
            else:
                break

        for day in range(self.simulation_time):
            for cus in self.daily_customers[day]:
                    if type(cus)!= type([]):   
                        cus.initiate_stay_day(day) #if (cus.stay_day - cus.booking_gap > 0) else 0
                        cus.initiate_search_day(cus.stay_day - cus.booking_gap)
                        
                        if cus.search_day > 0:
                            self.year_customers.append(cus)
                            self.daily_search_day[cus.search_day].append(cus)
            


    def modify_holiday_dataframe(self):
        
        months_day_records = month_start_end_days
        month_daily_lamda = pd.DataFrame({'month':[i for i in range(1,13)], 'base_lambda': [self.n_customers/3500 for i in range(1,13)]}) 

        self.df_holiday['month'] = self.df_holiday['day'].apply(lambda x: self.month_indicator(x,months_day_records))
        self.df_holiday = self.df_holiday.merge(month_daily_lamda, how = 'inner', on='month')


    def dist_value_generator(self,segment ,unsampled_customers,day):
        df = self.df_holiday.copy()
        col_name = segment+'_e_lambda'
        dist_value=np.random.poisson(df.at[df[df.day==day].index[0],col_name])  #generate a poisson value for given lamdha
        dist_value = dist_value if dist_value<=len(unsampled_customers[segment]) else len(unsampled_customers[segment])
        return dist_value

    # function to generate the effective lambda out of the 
    def effective_lambda_generator(self):
        self.modify_holiday_dataframe()
        df = self.df_holiday
        segments = self.cust_segments_list
        lambda_cols = [(seg+'_e_lambda') for seg in segments]
        weight_cols = list(df.columns[1:len(segments)+1])

        for col_ in lambda_cols:
            df[col_] = df.base_lambda
        for i in df.index:
            current_row = df.iloc[i]
            for col in weight_cols:
                if current_row[col]!=0:
                    if current_row['day']- current_row[col]>=0:
                        start_day = int(current_row['day']- current_row[col])
                        for j in range(start_day,i + 1):
                            previous_row =df.iloc[j]
                            df[lambda_cols[weight_cols.index(col)]].iloc[j]= previous_row.base_lambda*( 1+ current_row[col] )
                    else:
                        continue
                else:
                    continue
        return df
    # sampling customers daily based on a effective lambda value 
    def customer_sampling_daily(self): #daily sampling

        unsampled_customers = self.customers_by_seg.copy()
        unsampled_customers = {seg: sample for seg,sample in unsampled_customers.items() if sample} # removes segments with empty customers

        sample_allocation = {}
        df_holiday = self.effective_lambda_generator() # calling the effective lambda generator function
        arrival_real=pd.DataFrame()

        for day in range(len(df_holiday)):

            dist_val_dict = {seg: self.dist_value_generator(seg,unsampled_customers,day) for seg in unsampled_customers.keys()}

            sample_dict = {seg: random.sample(unsampled_customers[seg],dist_val_dict[seg]) for seg in unsampled_customers.keys()}
            sample_dict = {seg: sample for seg,sample in sample_dict.items() if sample} # removes segments with empty customers

            sample_allocation[day] = sample_dict.copy()

            if unsampled_customers:
                for seg in self.cust_segments_list:
                    if seg in sample_dict.keys(): 
                        for cust in sample_dict[seg]:
                            unsampled_customers[seg].remove(cust)
                            unsampled_customers = {seg: sample for seg,sample in unsampled_customers.items() if sample} # removes segments with empty customers
                    else:
                        continue
            else:
                break

            new_row = pd.Series({'Day':day, 'Arrival_count': sum(dist_val_dict.values())})
            arrival_real = pd.concat([arrival_real, new_row.to_frame().T], ignore_index=True)
            

            # clearing the dictionaries to prepare for the next day
            dist_val_dict.clear()
            sample_dict.clear()

        return sample_allocation,arrival_real, df_holiday

    #function to get the month currently in according to the current day
    def month_indicator(self, current_day , month_start_end_dict):
        for month in range(1,13):
            if (month_start_end_dict[month][0] <= current_day) and (month_start_end_dict[month][1] >= current_day):
                return month
            else:
                continue
    
    
            


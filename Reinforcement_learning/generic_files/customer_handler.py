import numpy as np
import pandas as pd


from generic_files.customer import *
from generic_files.config import *


class Customer_Handler:
    cust_segments_list = list(customer_segments.keys())
    def __init__(self,n_customers, simulation_days):
        self.simu_days = simulation_days

        self.n_customers = n_customers
        
        self.customers = [Customer( i+1) for i in range(n_customers)]
        self.customers_by_seg = { seg:[] for seg in self.cust_segments_list }
        for cust in self.customers:
           self.customers_by_seg[cust.segment].append(cust)

        self.df_holiday = pd.read_csv('generic_files/h_df.csv')if is_simu_h_df else pd.read_csv('generic_files/arrival_data.csv') # assigning the holiday dataframe
        
        self.year_customers = []
        self.daily_customers = {i:[] for i in self.simu_days}
        s_day_list = list(range(-1*leadtime_up_lim,0))+self.simu_days # altering the simulation days list to include customers who will search on the first day of the simulation
        self.daily_search_day={i:[] for i in s_day_list}

        self.customers_dict, self.arrival_real, self.df_holiday_updated = self.customer_sampling_daily()
        if is_simu_h_df:
             self.h_days_list, self.hday_room_val_boost_rates = self.boosted_value_rates()
        

    def preparing_daily_customers(self):
        for day in self.simu_days:
            if day in self.customers_dict.keys():
                sample_dict= self.customers_dict[day]  # accessing the customers by segment for the current day
                
                if sample_dict: # unpacking the customers in each segment for each day and assigning it to daily_cusomters dict
                    keys, values = zip(*sample_dict.items())
                    for i in values: # accessing the list in the values tuple
                        for j in i:    # iterating over each element in the list of the tuple
                            self.daily_customers[day].append(j)
        
            else:
                break

        for day in self.simu_days:
            for cus in self.daily_customers[day]:
                    if type(cus)!= type([]):
                        if is_simu_h_df:
                            rate = self.hday_room_val_boost_rates[day][cus.segment] if day in self.h_days_list else 1
                        else:
                            value = (self.df_holiday.iloc[day][cus.segment]/self.df_holiday.iloc[day][cus.segment])
                            if value>1.30:
                                value=1.30
                            else:
                                if value<0.95:
                                    value = 0.95  
                            rate = value

                        cus.initiate_stay_day(day,rate)
                        cus.initiate_search_day(cus.stay_day - cus.booking_gap)
                        
                        self.year_customers.append(cus)
                        self.daily_search_day[cus.search_day].append(cus)
            


    def modify_holiday_dataframe(self):
        
        months_day_records = month_start_end_days
        month_daily_lamda = pd.DataFrame({'month':[i for i in range(1,13)], 'base_lambda': [self.n_customers/min_expected_cust for i in range(1,13)]}) 

        self.df_holiday['month'] = self.df_holiday['day'].apply(lambda x: self.month_indicator(x,months_day_records))
        self.df_holiday = self.df_holiday.merge(month_daily_lamda, how = 'inner', on='month')
        self.df_holiday = self.df_holiday.sort_values(["date"]).reset_index(drop=True)


    def dist_value_generator(self,segment ,unsampled_customers,day):
        df = self.df_holiday.copy()
        col_name = segment+e_suffix if is_simu_h_df else segment
        dist_value=np.random.poisson(df.at[df[df.day_index==day].index[0],col_name])  #generate a poisson value for given lamdha
        dist_value = dist_value if dist_value<=len(unsampled_customers[segment]) else len(unsampled_customers[segment])
        return dist_value

    # function to generate the effective lambda out of the 
    def effective_lambda_generator(self):
        self.modify_holiday_dataframe()
        df = self.df_holiday
       
        segments = self.cust_segments_list
        lambda_cols = [(seg+e_suffix) for seg in segments]
        weight_cols = segments

        for col_ in lambda_cols:
            df[col_] = df.base_lambda
        for i in df.index:
            current_row = df.iloc[i]
            for col in weight_cols:
                if current_row[col]!=0:           
                    day_exists, day_index, day =self.cust_buildup_start_day(current_row['day_index'],int(current_row['customer_build_up']))
                    if day_exists:
                        start_day_index = day_index
                        added_expected_cust = df.loc[i,'base_lambda']*df.loc[i,col]
                        df.loc[start_day_index:i,col+e_suffix] +=added_expected_cust
                    else:
                        continue
                else:
                    continue
        self.df_holiday = df
        return df
    # sampling customers daily based on a effective lambda value 
    def customer_sampling_daily(self): #daily sampling

        unsampled_customers = self.customers_by_seg.copy()
        unsampled_customers = {seg: sample for seg,sample in unsampled_customers.items() if sample} # removes segments with empty customers

        sample_allocation = {}
        df_holiday = self.effective_lambda_generator() if is_simu_h_df else self.df_holiday # calling the effective lambda generator function
        arrival_real=pd.DataFrame()

        for day in self.simu_days:

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

    def cust_buildup_start_day(self, current_day, build_up_factor):
        current_day_index = self.simu_days.index(current_day)
        index_exists = True if current_day_index-build_up_factor>=0 else False
        buildup_day = self.simu_days[current_day_index-build_up_factor] if index_exists else -1
        return (index_exists, current_day_index-build_up_factor, buildup_day)
    
    def boosted_value_rates(self):
        c_names = [seg+e_suffix for seg in customer_segments]
        df= self.df_holiday.copy()
        df_filtered = df.apply(lambda x : x[c_names]-x.base_lambda, axis=1) # altering the df to check whether atleast one segment has a greater expected customers than the base lambda
        df = df[(df_filtered>0).any(axis=1)]
        cols_denominator = ['customer_build_up']+c_names
        rates ={}
        for day in list(df.day_index):
            d = int(df[cols_denominator][df.day_index==day].sum(axis=1)) # denominator
            rates[day] = {}
            for seg in customer_segments:
                cols_numerator = ['customer_build_up', seg+e_suffix]
                n = int(df[cols_numerator][df.day_index==day].sum(axis=1)) # numerator 
                rates[day][seg]= round((1+n/d),2)
        return list(df.day_index), rates
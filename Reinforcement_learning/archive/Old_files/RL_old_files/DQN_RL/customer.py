import numpy as np
import random

from config import *




class Customer:

  customer_segment = list(customer_segments.keys())

  def __init__(self, id_num):
    self.segment = random.choice(self.customer_segment) # adding customer segment

    self.room_value_appr = random.uniform(1,1.15) # to appreciate the value that the customer is willing to pay if a booking attempt was not successfull
    self.stay_duration_place_holder = np.random.poisson(2.206)
    self.stay_duration = self.stay_duration_place_holder if self.stay_duration_place_holder!=0 else 1  # stay duration for the customer from the stay day
    
    # randomizing customer room selection

    self.type = random.choice([i for i in room_type])
    
    name_room=self.type
    self.room_value_expected = customer_segments[self.segment]['price']
    self.room_value=round(np.random.normal(room_type[name_room]['cus_will_pay'][0],room_type[name_room]['cus_will_pay'][1],1)[0],2) * self.room_value_expected
    self.actual_hotel_price = 0
  
    self.stay_day = np.nan  # 0 is the 1st day of the month and 30th is the 31st of the month, this was done due python having 0 as the starting index
    self.booking_gap = random.randint(4,14)
    self.initial_search_day = np.nan # searching day prior to the actual needed stay date
    self.search_day = np.nan # placeholder to update the search day if initial attempt fails
    self.booked_day = np.nan
    
    self.actual_gap = 0
    self.remaining_days = 0

    self.attempts = 0
    self.booking_status = np.nan
    
    self.id = id_num

    self.booking_cancelled = 0
    self.cancelled_day = -1
    self.stay_day_passsed_or_not=0

  def inc_room_price(self): # method to appreciate double room value
    self.room_value *= self.room_value_appr

  def update_search_day(self):

    if self.search_day < self.stay_day:
      self.search_day += 1
      self.booking_gap = self.stay_day - self.search_day # updating the booking gap as the search day is being updated


  def update_attempts(self):
    self.attempts += 1
  
  def booking_success(self, hotel_price):
    self.booking_status = 'Booking successful'
    self.actual_hotel_price = hotel_price
  
  def booking_fail(self, hotel_price,no_rooms = False, low_price = False):
    if no_rooms:
      self.booking_status = 'Rooms are not available'
      self.actual_hotel_price = hotel_price
    if low_price:
      self.booking_status = 'Customer price is low'
      self.actual_hotel_price = hotel_price

  def booking_cancel(self,day):
    self.booking_status = 'Booking Cancelled'
    self.booking_cancelled = 1
    self.cancelled_day = day

  def initiate_stay_day(self, day):
    self.stay_day = day

  def initiate_search_day(self, day):
    self.search_day = day
    self.initial_search_day = day
    
  
  
  def update_booked_day(self, day):
    self.booked_day = day
    self.actual_gap = self.stay_day - self.booked_day
    self.remaining_days = self.actual_gap

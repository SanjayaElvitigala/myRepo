import random
from config import *


class Hotel:
  
  def __init__(self, simulationtime, input_room_list, agent_activated = True):
    self.agent_activated = agent_activated

    # making room type count as instance variable
    for i,j in zip(room_type,input_room_list): 
      name_room_count=i+'_count'
      setattr(self, name_room_count, j)
      

    # making room type price,schedule,cost as instance variable
    for i in room_type:
      name_room_price=i+'_price'
      name_room_schedule=i+'_schedule'
      name_room_cost=i+'_cost'
      name_room_count=i+'_count'

      price=random.randint(room_type[i]['price'][0],room_type[i]['price'][1])
      schedule= [getattr(self,name_room_count) for i in range(simulationtime+10)]
      cost=room_type[i]['cost']
      setattr(self, name_room_price, price)
      setattr(self, name_room_schedule, schedule)
      setattr(self, name_room_cost, cost)
      self.local=locals()
  
    self.price_change_rate =  random.uniform(2,3)

  
  def update_room_schedule(self, customer):
    checkIn = customer.stay_day 
    checkOut = customer.stay_day + customer.stay_duration

    name_room_schedule=customer.type+'_schedule'
    getattr(self,name_room_schedule)[checkIn:checkOut+1]=[ getattr(self,name_room_schedule)[i]-1 for i in range(checkIn,checkOut+1)]
    
          
  def update_cancel_room_schedule(self,customer):
    checkIn = customer.stay_day 
    checkOut = customer.stay_day + customer.stay_duration

    name_room_schedule=customer.type+'_schedule'
    getattr(self,name_room_schedule)[checkIn:checkOut+1]=[ getattr(self,name_room_schedule)[i]+1 for i in range(checkIn,checkOut+1)]
  
  def book_room(self, customer):
    if not self.is_fully_booked(customer):
      self.update_room_schedule(customer)


  def is_fully_booked(self, customer):
    checkIn = customer.stay_day 
    checkOut = customer.stay_day + customer.stay_duration

    name_room_schedule=customer.type+'_schedule'
    if all(getattr(self,name_room_schedule)[i]>0 for i in range(checkIn, checkOut +1)):
      return False
    else:
      return True

  def check_price_feasibility(self, customer):
    if self.agent_activated: # price checker for RL agent
      name_room_price=customer.type+'_price'
      room_price_check = True if getattr(self,name_room_price)<= customer.room_value else False
      return room_price_check
    else: # price checker for base model 
      name_room_price=customer.type+'_price'
      room_price_check = True if (getattr(self,name_room_price)+ self.price_change_rate*(customer.booking_gap)) <= customer.room_value else False
      return room_price_check
   

  def process_booking(self, timestep, customer):
    ''' 1 --> success
        2 --> No rooms
        3 --> customer price too low
        4 --> Not today customer
    '''

    today_customer = True if customer.search_day == timestep else False
    rooms_available = not self.is_fully_booked(customer)
    price_check = self.check_price_feasibility(customer)
    
    if today_customer:
      if rooms_available:
        if price_check:
           self.book_room(customer)
           return 1 # success
        else:
          return 3 # customer price too low
      else:
        return 2 # No rooms
    else:
      return 4 # Not today customer
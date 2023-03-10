import random
from generic_files.config import *


def execute_logic(hotels, timestep, daily_search_day_list):

        # recording the hotels sorted by price for each room type and by each segment
        sorted_hotels_by_room_type_and_segment = {}
        for type_of_room in room_type:
            segment_wise_sorted = {}
            for segment in customer_segments:
                segment_wise_sorted[segment] = sort_hotels_by_price(hotels, type_of_room,segment)
            sorted_hotels_by_room_type_and_segment[type_of_room] = segment_wise_sorted
            

        # recording hotel prices set on each day
        for hotel_obj in hotels:
            for type_of_room in room_type:
                name_room_price = type_of_room + '_price'
                for segment in customer_segments:
                    hotel_obj.room_price_records[type_of_room][segment][timestep] = getattr(hotel_obj,name_room_price)[segment]
         
        for customer in daily_search_day_list[timestep]:
            r_type = customer.type # room type needed by the customer
            segment = customer.segment # segment of the customer
            name_room_price = r_type + '_price'
            name_room_cost = r_type + '_cost'
            

            sorted_hotels = sorted_hotels_by_room_type_and_segment[r_type][segment]
            
            for hotel in sorted_hotels:
                hotel_obj = hotel
                hotel_obj.total_customers[r_type][segment][timestep]+=1
                hotel_obj.daily_customers=+1
                price_of_room = getattr(hotel_obj,name_room_price)[segment]
                booking_process_result = hotel_obj.process_booking(timestep, customer)

                if booking_process_result == 4 : # Not today Customer
                    pass
                else:
                    customer.update_attempts()
                    customer.hotel_name = hotel_obj.name

                    if booking_process_result == 2: # No rooms
                        hotel_obj.failed_customers[timestep]+=1
                        customer.booking_fail(price_of_room, no_rooms =True)

                    elif booking_process_result == 1: # success
                        hotel_obj.converted_customers[r_type][segment][timestep]+=1
                        hotel_obj.booked_customers[timestep] += 1

                        customer.update_booked_day(timestep)
                        customer.booking_success(price_of_room)
                        hotel_obj.per_day_profit[customer.type][customer.segment] += price_of_room-getattr(hotel_obj,name_room_cost)
                        break

                    elif booking_process_result == 3: # customer price too low
                        hotel_obj.failed_customers[timestep] += 1

                        customer.booking_fail(price_of_room, low_price =True)
                        
                        if customer.search_day < customer.stay_day:
                            customer.inc_room_price()
                        pre_search_day = customer.search_day
                        customer.update_search_day()

                        if (pre_search_day != customer.search_day) & customer.trying_again==1:
                            daily_search_day_list[customer.search_day].append(customer)
                        break

def execute_cancellation(cancellation_rate, year_customers, hotel_objs, timestep):
        for cus in [cuss for cuss in year_customers if ((cuss.booking_status=='Booking successful') and (cuss.stay_day>timestep))]:
                cus.remaining_days -=1
                random_value = random.uniform(0,1)
                if random_value < (cancellation_rate/100) :
                    hotel_obj=[i for i in hotel_objs if i.name==cus.hotel_name][0]
                    hotel_obj.update_cancel_room_schedule(cus)
                    cus.booking_cancel(timestep)


def sort_hotels_by_price(hotels_list, type_of_room,segment):
    room_price_str = type_of_room + '_price'
    sorted_hotels_list = sorted(hotels_list, key=lambda x: getattr(x,room_price_str)[segment], reverse=False)
    return sorted_hotels_list


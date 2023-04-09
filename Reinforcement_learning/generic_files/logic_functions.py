import random
from generic_files.config import *


def execute_logic(hotels, timestep, daily_search_day_list, is_seg_pricing = False):

        # recording the hotels sorted by price for each room type
        if is_seg_pricing:
            sorted_hotels_by_room_type = {type_of_room : {seg: sort_hotels_by_price(hotels, type_of_room, seg) 
                                                           for seg in customer_segments}
                                            for type_of_room in room_type}
        else:
            sorted_hotels_by_room_type = {type_of_room : sort_hotels_by_price(hotels, type_of_room) for type_of_room in room_type}

        # recording hotel prices set on each day
        if is_seg_pricing:
            for hotel_obj in hotels:
                for type_of_room in room_type:
                    name_room_price = type_of_room + '_price'
                    for segment in customer_segments:
                        hotel_obj.room_price_records[type_of_room][segment][timestep] = getattr(hotel_obj,name_room_price)[segment]
        else:
            for hotel_obj in hotels:
                for type_of_room in room_type:
                    name_room_price = type_of_room + '_price'
                    hotel_obj.room_price_records[type_of_room][timestep] = getattr(hotel_obj,name_room_price)
                    hotel_obj.arrival_count={i:0 for i in room_type.keys()}

        for customer in daily_search_day_list[timestep]:
            r_type = customer.type # room type needed by the customer
            segment = customer.segment # segment of the customer
            name_room_price = r_type + '_price'
            name_room_cost = r_type + '_cost'
            

            sorted_hotels = sorted_hotels_by_room_type[r_type][segment] if is_seg_pricing else sorted_hotels_by_room_type[r_type]
            
            for hotel in sorted_hotels:
                hotel_obj = hotel

                if is_seg_pricing:
                    hotel_obj.total_customers[r_type][segment][timestep]+=1
                else:
                    hotel_obj.total_customers[r_type][timestep]+=1

                hotel_obj.daily_customers=+1
                price_of_room = getattr(hotel_obj,name_room_price)[segment] if is_seg_pricing else getattr(hotel_obj,name_room_price)
                booking_process_result = hotel_obj.process_booking(timestep, customer)

                if booking_process_result == 4 : # Not today Customer
                    pass
                else:
                    customer.update_attempts()
                    if customer.attempts == 1:
                        hotel_obj.arrival_count[r_type]+=1

                    customer.hotel_name = hotel_obj.name

                    if booking_process_result == 2: # No rooms
                        hotel_obj.failed_customers[timestep]+=1
                        customer.booking_fail(price_of_room, no_rooms =True)

                    elif booking_process_result == 1: # success
                        if is_seg_pricing:
                            hotel_obj.converted_customers[r_type][segment][timestep]+=1
                        else:
                            hotel_obj.converted_customers[r_type][timestep]+=1
                        hotel_obj.booked_customers[timestep] += 1

                        customer.update_booked_day(timestep)
                        customer.booking_success(price_of_room)
                        if is_seg_pricing:
                            hotel_obj.per_day_profit[r_type][segment] += price_of_room-getattr(hotel_obj,name_room_cost)
                        else:
                            hotel_obj.per_day_profit+= price_of_room-getattr(hotel_obj,name_room_cost)
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


def sort_hotels_by_price(hotels_list, type_of_room, segment = None):
    if segment is None:
        room_price_str = type_of_room + '_price'
        sorted_hotels_list = sorted(hotels_list, key=lambda x: getattr(x,room_price_str), reverse=False)
    else:
        room_price_str = type_of_room + '_price'
        sorted_hotels_list = sorted(hotels_list, key=lambda x: getattr(x,room_price_str)[segment], reverse=False)
    return sorted_hotels_list


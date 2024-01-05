def execute_logic(simu_obj, timestep, failed_customers, booked_customers,hotel_obj, daily_search_day_list, agent_activated= True):
         
         for customer in daily_search_day_list[timestep]:
            if agent_activated:
                simu_obj.rl_tot_customers[customer.type]+=1 

            name_room_price = customer.type + '_price'
            price_of_room = getattr(hotel_obj,name_room_price)

              
            booking_process_result = hotel_obj.process_booking(timestep, customer)

            if booking_process_result == 4 : # Not today Customer
                pass
            else:
                customer.update_attempts()

                if booking_process_result == 2: # No rooms
                    failed_customers[timestep]+=1
                    customer.booking_fail(price_of_room, no_rooms =True)

                elif booking_process_result == 1: # success
                    if agent_activated:
                        simu_obj.rl_converted_customers[customer.type]+=1
                    booked_customers[timestep] += 1

                    customer.update_booked_day(timestep)
                    customer.booking_success(price_of_room)

                elif booking_process_result == 3: # customer price too low
                    failed_customers[timestep] += 1

                    customer.booking_fail(price_of_room, low_price =True)
                    
                    if customer.search_day < customer.stay_day:
                        customer.inc_room_price()
                    pre_search_day = customer.search_day
                    customer.update_search_day()

                    if pre_search_day != customer.search_day:
                        daily_search_day_list[customer.search_day].append(customer)
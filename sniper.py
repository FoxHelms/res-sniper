from resbot import TimeChecker, Booker
from typing import List
from time import sleep
import resy_config as rc
from read_db import get_rest_lists

'''
Top level module
To run every day at 9:00am eastern time
This module reads a local database of user provided restaurant information
It decides the best time to make a reservation and that restaurant, and then books the reservation
'''


'''Read the local database and parse out the venue IDs and restaurant names into two lists'''
all_rests = get_rest_lists()
all_ids = [rest[2] for rest in all_rests]
all_names: List[int] = [rest[1] for rest in all_rests]

def sort_rest_list():
    '''Iterate through restaurants
    query the API url of each restaurant and get a list of available reservation slots,
    remove the restaurant name/ID if there are no available slots
    Create list of tuples of (venue ID, list of slots)
    Sort this list by ascending order of number of slots
    Return sorted list
    '''
    avail_slots_all_rest = []
    sorted_rests = []
    for u, i in zip(all_names, all_ids):
        restList = TimeChecker.check_if_slots(u.replace(' ','-').lower())
        if restList == False:
            all_names.remove(u)
            all_ids.remove(i)
        else:
            avail_slots_all_rest.append((i, restList))
    for k in sorted(avail_slots_all_rest, key=lambda k: len(k[1])):
        sorted_rests.append((k[0], k[1]))
    return sorted_rests

def get_best_non_overelap_times():
    '''
    While holding the shortest list of dates as the "priority dates", 
    remove dates from all other lists that also appear on the priority list
    This ensures there's no date overlap. 
    Resy does not allow you to make reservations that are too close together in time.
    With this shorter list of non-overlapping dates:
    Determine the best time for each restaurant and get the conf id for that time
    Return a dictionary of best_time:conf_ids
    '''
    sorted_rests = sort_rest_list() # {ID: avail_days}
    # print(sorted_rests)
    priority_tuple = sorted_rests.pop(0)
    trimmed_list = []
    date_set = priority_tuple[1]
    trimmed_list.append(priority_tuple)
    for i in sorted_rests:
        new_times = list(set(i[1]).difference(date_set)) # alt: new_times = list(set(priority_tuple[1])^set(i[1]))
        date_set += new_times
        trimmed_list.append((i[0],new_times))
    to_book = {}
    for rest in trimmed_list:
        all_times_and_configs = TimeChecker.get_times_confs_for_ven(rest[0], rest[1]) # {date+time : config_id}
        best_time = TimeChecker.select_time(all_times_and_configs) # returns date+time
        to_book[best_time] = all_times_and_configs[best_time] # (date+time, conf_id)
    return to_book # {date+time : config_id}


if __name__ == '__main__':
    # INSTEAD of importing rc, just import login data and do decryption here. 
    # bot = Booker(rc.email, rc.pw)
    to_book = get_best_non_overelap_times()
    for slot in to_book:
        print('nice')
        # bot.make_reservation(bot.create_book_token(slot, to_book[slot]))


        

    
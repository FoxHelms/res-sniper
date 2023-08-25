from app import db, Restaurants
from resbot import *
from typing import List
from time import sleep


all_id_tuple: List[tuple] = Restaurants.query.with_entities(Restaurants.venId).all()
all_ids: List[int] = [id[0] for id in all_id_tuple]

def crawl(bot,vid):
    avail_times = bot.get_avail_times_for_venue(vid)
    best_time = bot.select_slot(avail_times)
    conf_id = bot.create_config_id(best_time)
    book_token = bot.create_book_token(conf_id)
    response = bot.make_reservation(book_token)
    print(bot.booked_dates)
    return response



if __name__ == '__main__':

    bot = ResBot()
    for _ in all_ids:
        response = crawl(bot,_)
        if response == 201:
            print(f'Reservation booked at {_}')
        else:
            print(f'Error! {response}')


        

    
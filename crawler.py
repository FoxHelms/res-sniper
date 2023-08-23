from app import db, Restaurants
from resbot import *
from typing import List
from time import sleep


all_id_tuple: List[tuple] = Restaurants.query.with_entities(Restaurants.venId).all()
all_ids: List[int] = [id[0] for id in all_id_tuple]

def crawl(vid):
    bot = ResBot()
    avail_times = bot.get_avail_times_for_date(vid)
    best_time = bot.select_slot(avail_times)
    conf_id = bot.create_config_id(best_time)
    book_token = bot.create_book_token(conf_id)
    response = bot.make_reservation(book_token)
    return response



if __name__ == '__main__':

    for _ in all_ids:
        response = crawl(_)
        if response == 201:
            break


        

    
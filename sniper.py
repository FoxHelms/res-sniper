from app import db, Restaurants
from resbot import *
from typing import List
from time import sleep

'''
Top level module
To run every day at 9:00am eastern time
'''


all_id_tuple: List[tuple] = Restaurants.query.with_entities(Restaurants.venId).all()
all_ids: List[int] = [id[0] for id in all_id_tuple]

def crawl(bot: ResBot, vid: int) -> int:
    avail_times: List[dict] = bot.get_avail_times_for_venue(vid)
    best_time: dict = bot.select_slot(avail_times)
    conf_id: str = bot.create_config_id(best_time)
    book_token: str = bot.create_book_token(conf_id)
    response: int = bot.make_reservation(book_token)
    return response



if __name__ == '__main__':

    bot = ResBot()
    for _ in all_ids:
        response = crawl(bot,_)
        if response == 201:
            print(f'Reservation booked at {_}')
        else:
            print(f'Error! {response}')


        

    
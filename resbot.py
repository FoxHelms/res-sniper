from dataclasses import dataclass
from typing import List
from xmlrpc.client import Boolean
import requests as r
import resy_config as rc
import datetime as DT
from cryptic import *
from adj_date import adjust_date
import re

class NoSlotsError(Exception): pass
class BookingError(Exception): pass
class InvalidMethod(Exception): pass


def requester(m,upath, *params, **data): # (optional data)
    hdrs: dict = {
            'accept-language': 'en-US,en;q=0.9',
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
    if m == 'postj':
        response: r.models.Response = r.post(upath, headers=hdrs, json=data)
    elif m == 'post':
        # hdrs['x-resy-auth-token'] = params[0] >> need to create as addnl header
        response: r.models.Response = r.post(upath, headers=hdrs, data=data)
    elif m == 'get':
        if params:
            response: r.models.Response = r.get(upath, headers=hdrs, params=params)
        response: r.models.Response = r.get(upath, headers=hdrs)
    else:
        raise InvalidMethod
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()


class Authenticator:
    @classmethod
    def get_auth_and_payment(cls,usr,pw):
        '''get auth token and payment method from resy'''
        res_data = requester('post', 'https://api.resy.com/3/auth/password', email=usr, password=pw)
        auth_token = res_data['token']
        payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
        return auth_token,payment_method_string

class RestaurantIdentifier:
    @classmethod
    def convert_url(cls, url_string):
        # https://resy.com/cities/ny/shukette?date=2023-09-12&seats=2
        rname_q = re.search('cities/(.*)date.*', url_string)
        rest_string = rname_q.group(1)[:-1]
        rest_package = rest_string.split('/')
        return rest_package

    @classmethod
    def get_venue_id(cls, url_string: str) -> int:
        '''return resy venue ID based on query'''
        r_city, r_name = cls.convert_url(url_string)
        url_path = f'https://api.resy.com/3/venue?url_slug={r_name}&location={r_city}'
        dat = requester('get',url_path)
        resyID = dat['id']['resy']
        return resyID

class TimeChecker:
    @classmethod
    def check_if_slots(cls, resQuery):
        '''check if there are open slots or not. returns list or false'''
        time_delta: int = 7
        today: DT.date = DT.date.today()
        date =  today.strftime('%Y-%m-%d') # '2023-08-22'

        data = {"slot_filter":{"day":date,"party_size":2},"query":resQuery}

        urlpath = 'https://api.resy.com/3/venuesearch/search'

        t = requester('postj',urlpath, **data)

        available_dates = t['search']['hits'][0]['inventory_reservation']

        if available_dates:
            return available_dates
        else:
            return False
    @classmethod
    def get_times_confs_for_ven(cls, venue_id: int, avail_dates) -> List[dict]:
        '''
        I want to create a dictionary of all available times at a venue and their coresponding config ids. 

        I'm guessing that things will probably go like this:
        For each restaurant, create all_time : >> get_avail_times
        Find out how long each all_times is per restaurant. >> main.py
        Find shortest list of all_dates >> main.py
        get times and configs for this restaurant >> get_avail_times
        Choose a time >> select_time
        Create config id >> get_times

        ''' 
        def get_conf():
            for slot in open_slots:
                start_time = slot['date']['start']
                conf_t = slot['config']['token']
                all_times_confs[start_time] = conf_t

        all_times_confs = {}
        for d in avail_dates:
            url_path = f'https://api.resy.com/4/find?lat=0&long=0&day={d}&party_size=2&venue_id={venue_id}'
            data = requester('get',url_path)
            results = data['results']
            if results['venues'][0]['slots']:
                open_slots: List[dict] = results['venues'][0]['slots']
                get_conf()
        return all_times_confs

    @classmethod
    def select_time(cls, all_time_confs) -> dict:
        '''Choose first slot OR first slot that starts after 8:00pm'''
        # 'date': {'end': '2023-08-21 18:45:00', 'start': '2023-08-21 17:15:00'}
        for key in all_time_confs:
            start_time: str = key[-8:-6]
            start_time_int: int = int(start_time)
            if start_time_int >= 20:
                return key
        return next(iter(all_time_confs))

class Booker:
    def __init__(self) -> None:
        self.booked_dates: List[str] = [] # get_ids()
        usr = ''
        pw = ''
        self.auth, self.payment_id = Authenticator.get_auth_and_payment(usr,pw)

    def keep_track_of_booked_dates(self, day) -> None:
        '''Adds booked to list'''
        self.booked_dates.append(day)
        
    def create_book_token(self, all_time_confs_key, all_time_confs_value) -> str:
        '''takes params and makes book token'''
        params = (
            ('x-resy-auth-token', self.auth),
            ('config_id', all_time_confs_value),
            ('day', all_time_confs_key[:10]),
            ('party_size', '2')
        )
        details = requester('get', 'https://api.resy.com/3/details', *params)
        return details['book_token']['value']
    
    def make_reservation(self, book_token: str) -> int:
        '''take book token and post reservation'''
        data = {
        'book_token': book_token,
        'struct_payment_method': self.payment_id,
        'source_id': 'resy.com-venue-details'
        }
        requester('post','https://api.resy.com/3/book', self.auth, **data)
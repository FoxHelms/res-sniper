from dataclasses import dataclass
from typing import List
from xmlrpc.client import Boolean
import requests as r
import resy_config as rc
import datetime as DT
from cryptic import *
from adj_date import adjust_date

class NoSlotsError(Exception): pass
class BookingError(Exception): pass

def requester(m,upath,*params, **data): # (optional data)
    hdrs: dict = {
            'accept-language': 'en-US,en;q=0.9',
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
    if m == 'postj':
        response: r.models.Response = r.post(upath, headers=hdrs, json=data)
    if m == 'post':
        response: r.models.Response = r.post(upath, headers=hdrs, data=data)
    if m == 'get':
        if params:
            response: r.models.Response = r.get(upath, headers=hdrs, params=params)
        response: r.models.Response = r.get(upath, headers=hdrs)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()


class Authenticator:
    def __init__(self, usr, pw) -> None: 
        self.usr: str = usr
        self.pw: str = pw
    
    def get_auth_and_payment(self):
        '''get auth token and payment method from resy'''
        res_data = requester('post', 'https://api.resy.com/3/auth/password', email=self.usr, password=self.pw)
        auth_token = res_data['token']
        payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
        return auth_token,payment_method_string


class TimeChecker:
    @classmethod
    def get_venue_id(cls, resQuery: str) -> int:
        '''return resy venue ID based on query'''
        url_path = f'https://api.resy.com/3/venue?url_slug={resQuery}&location=ny'
        dat = requester('get',url_path)
        resyID = dat['id']['resy']
        return resyID
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
    def get_avail_times_for_venue(cls, venue_id: int, resQuery) -> List[dict]:
        '''
        I want to create a dictionary of all available times at a venue and their coresponding config ids. 



        I'm guessing that things will probably go like this:
        For each restaurant, create all_times
        Find out how long each all_times is per restaurant. 
        Start with the first index on the shortest all_times list
        Get all slots for that
        Get best slot for that, 
        Create config id


        ''' 
        def get_conf():
            for slot in open_slots:
                start_time = slot['date']['start']
                conf_t = slot['config']['token']
                all_times_confs[start_time] = conf_t

        avail_dates = cls.check_if_slots(resQuery)
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
    def select_slot(cls, all_time_confs) -> dict:
        '''Choose first slot OR first slot that starts after 8:00pm'''
        # 'date': {'end': '2023-08-21 18:45:00', 'start': '2023-08-21 17:15:00'}
        best_slot = None
        for key in all_time_confs:
            start_time: str = key[-8:-6]
            start_time_int: int = int(start_time)
            if start_time_int >= 20:
                return key
        return all_time_confs[0]



a = TimeChecker.get_avail_times_for_venue(8579,'Shukette')

b = TimeChecker.select_slot(a)

print(b)

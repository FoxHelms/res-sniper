from dataclasses import dataclass
from typing import List
from xmlrpc.client import Boolean
import requests as r
import datetime as DT
from encryption import *
import re

class NoSlotsError(Exception): pass
class BookingError(Exception): pass
class InvalidMethod(Exception): pass
class BadLogin(Exception): pass
class NoJson(Exception): pass


def requester(m,upath, *params, **data): 
    '''
    A wrapper function for using the python requests library
    takes method as string, url path, and any additional arguments mostly for post requests
    Methods: post json, post, get'''
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
        if response.status_code != 200 or response.status_code != 201:
            return response.status_code
    elif m == 'get':
        if params:
            response: r.models.Response = r.get(upath, headers=hdrs, params=params)
        response: r.models.Response = r.get(upath, headers=hdrs)
    else:
        raise InvalidMethod
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        try:
            return response.json()
        except:
            raise NoJson


class Authenticator:
    '''
    Behavior class that generates an auth. token and payment string from the resy website
    Bad Login is usually due to a 500: Internal Server Error, 
    This means that the Resy server has recognized this program as bot activity
    '''
    @classmethod
    def get_auth_and_payment(cls,usr,pw):
        '''get auth token and payment method from resy'''
        try:
            res_data = requester('post', 'https://api.resy.com/3/auth/password', email=usr, password=pw)
            auth_token = res_data['token']
            payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
            return auth_token,payment_method_string
        except:
            raise BadLogin

class RestaurantIdentifier:
    '''
    Behavior class for any method that gets info about a restaurant from a resy url or a resy page'''
    @classmethod
    def convert_url(cls, url_string):
        '''
        Takes a url and parses out the city name and restaurant name
        Returns a list: [city abbrev, restaurant name]
        '''
        # https://resy.com/cities/ny/shukette?date=2023-09-12&seats=2
        rname_q = re.search('cities/(.*)date.*', url_string)
        rest_string = rname_q.group(1)[:-1]
        rest_package = rest_string.split('/')
        return rest_package

    @classmethod
    def get_venue_id(cls, url_string: str) -> int:
        '''Takes human url to a resy page and performs a get request to the API version of the url
        Parses the page and returns the venue ID for the restaurant
        '''
        r_city, r_name = cls.convert_url(url_string)
        url_path = f'https://api.resy.com/3/venue?url_slug={r_name}&location={r_city}'
        dat = requester('get',url_path)
        resyID = dat['id']['resy']
        return resyID

class TimeChecker:
    '''Behavior class for all methods related to getting dates and times from the resy website'''
    @classmethod
    def check_if_slots(cls, resQuery):
        '''Perform post json request to API url of a restaurant
        Parses response for all open reservations on the calendar
        If no openings are present, returns false
        Otherwise, returns list of available dates'''
        today: DT.date = DT.date.today()
        date =  today.strftime('%Y-%m-%d') # '2023-08-22'
        data = {"slot_filter":{"day":date,"party_size":2},"query":resQuery}
        urlpath = 'https://api.resy.com/3/venuesearch/search'
        t = requester('postj',urlpath, **data)
        try:
            available_dates = t['search']['hits'][0]['inventory_reservation']
        except:
            return False
        if not available_dates:
            return False
        return available_dates


    @classmethod
    def get_times_confs_for_ven(cls, venue_id: int, avail_dates) -> List[dict]:
        '''
        Goes through every available date and gets the slot time and slot configuration code
        Returns a dictionary of slot time: slot code
        ''' 
        def get_conf():
            '''Local method for parsing the restaurant page for the config code
            Adds to dictionary'''
            for slot in open_slots:
                start_time = slot['date']['start']
                conf_t = slot['config']['token']
                all_times_confs[start_time] = conf_t

        all_times_confs = {}
        for d in avail_dates:
            url_path = f'https://api.resy.com/4/find?lat=0&long=0&day={d}&party_size=2&venue_id={venue_id}'
            data = requester('get',url_path)
            results = data['results']['venues'][0]['slots']
            if results:
                open_slots: List[dict] = results
                get_conf()
        return all_times_confs

    @classmethod
    def select_time(cls, all_time_confs) -> dict:
        '''
        Iterates through dictionary of slot times
        Returns the first time that starts after 8pm
        if there are no times that start after 8pm, returns first slot
        '''
        # 'date': {'end': '2023-08-21 18:45:00', 'start': '2023-08-21 17:15:00'}
        for key in all_time_confs:
            start_time: str = key[-8:-6]
            start_time_int: int = int(start_time)
            if start_time_int >= 20:
                return key
        return next(iter(all_time_confs))

class Booker:
    '''
    Class for anything related to making a reservation
    '''
    def __init__(self, usr, pw) -> None:
        '''
        Instantiating this class is similar to creating a session on resy's website
        It generates an auth token and payment id
        '''
        self.booked_dates: List[str] = [] # get_ids()
        self.auth, self.payment_id = Authenticator.get_auth_and_payment(usr,pw)
        
    def create_book_token(self, all_time_confs_key, all_time_confs_value) -> str:
        # CHANGE TO POST JSON
        '''uses best time slot and best config id as parameters,
        post json request to API url of the restaurant
        parse the book token from the response
        return book token'''
        data = {'x-resy-auth-token': self.auth, 'config_id': all_time_confs_value,
        'day': all_time_confs_key[:10],'party_size': '2'}
        details = requester('postj', 'https://api.resy.com/3/details', **data)
        return details['book_token']['value']
    
    def make_reservation(self, book_token: str) -> int:
        '''using auth token, payment id, and book token as parameters
        post request to API url
        If no error is returned, then the reservation was successfully booked'''
        data = {
        'book_token': book_token,
        'struct_payment_method': self.payment_id,
        'source_id': 'resy.com-venue-details'
        }
        requester('post','https://api.resy.com/3/book', self.auth, **data)
        
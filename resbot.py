from typing import List
import requests as r
import resy_config as rc
import datetime

class NoSlotsError(Exception): pass

class ResBot():
    '''Spawn to click on buttons and input/submit data on webpage'''
    def __init__(self) -> None:
        self.usr = rc.email
        self.pw = rc.pw
        self.headers = rc.headers
        self.test_day = '2023-08-21'
        self.test_id = '59705'

        def get_auth_token_and_payment_method_id() -> (str, str):
            '''get auth token and payment method from resy'''
            data = {
            'email': self.usr,
            'password': self.pw
            }

            response = r.post('https://api.resy.com/3/auth/password', headers=self.headers, data=data)
            res_data = response.json()
            auth_token = res_data['token']
            payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
            return auth_token,payment_method_string
        self.auth, self.payment_id = get_auth_token_and_payment_method_id()

    def get_venue_id(self, resQuery: str) -> int:
        '''return resy venue ID based on query'''
        url_path = f'https://api.resy.com/3/venue?url_slug={resQuery}&location=ny'
        params = (
        ('x-resy-auth-token',  self.auth),
        ('lat', '0'),
        ('long', '0')
        )
        response = r.get(url_path, headers=self.headers, params=params)
        dat = response.json()
        resyID = dat['id']['resy']
        return resyID
    
    def get_avail_times_for_date(self, res_date: str, venue_id: int) -> List[str]: 
        url_path = f'https://api.resy.com/4/find?lat=0&long=0&day={res_date}&party_size=2&venue_id={venue_id}'
        response = r.get(url_path,headers=self.headers)
        data = response.json()
        results = data['results']
        if len(results['venues'][0]['slots']) > 0:
            open_slots = results['venues'][0]['slots']
            return open_slots
        else:
            raise NoSlotsError('There are no open tables at that restaurant')



    def get_rest_dets_from_link(self, resLink: str) -> List[str]:
        '''take link as input and return rest name, loc'''
    def get_time_reservations_update(self, resLink: str) -> str:
        '''
        Scrape time reservation updates from website
        Will this return a string or an int or some sort of datetime object?
        '''
    def add_rest_to_check_list(self, resLink: str) -> None:
        '''Take link and add to list of places to check'''
    def get_length_check_list(self, checkList: list) -> int:
        '''get lenght of the checklist, return int or None (or zero?)'''
    def create_config_id(self, open_slots: list) -> str:
        '''create config id token'''
        for slot in open_slots:
            config_id = slot['config']['token']
            return config_id
        
    def create_book_token(self, conf_id: str) -> str:
        '''takes params and makes book token'''
        params = (
                    ('x-resy-auth-token', self.auth),
                    ('config_id', conf_id),
                    ('day', self.test_day),
                    ('party_size', '2')
                    )
        
        details_request = r.get('https://api.resy.com/3/details', headers=self.headers, params=params)
        details = details_request.json()
        book_token = details['book_token']['value']
        return book_token



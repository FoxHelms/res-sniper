from tracemalloc import start
from typing import List
import requests as r
import resy_config as rc
import datetime as DT





class NoSlotsError(Exception): pass
class BookingError(Exception): pass

class ResBot():
    '''Spawn to click on buttons and input/submit data on webpage'''
    def __init__(self) -> None:
        self.usr = rc.email
        self.pw = rc.pw
        self.headers = rc.headers
        self.booked_dates: List[str] = [] # get_ids()
        self.time_delta = 7
        self.test_id = '59679' # '8579'

        def create_date():
            '''create date '''
            today = DT.date.today()
            nextweek: DT.date = today + DT.timedelta(days=self.time_delta)
            return nextweek.strftime('%Y-%m-%d') # '2023-08-22'

        self.date = create_date()

        def get_auth_token_and_payment_method_id():
            '''get auth token and payment method from resy'''
            data = {
            'email': self.usr,
            'password': self.pw
            }

            response = r.post('https://api.resy.com/3/auth/password', headers=self.headers, data=data)
            response.raise_for_status()  # raises exception when not a 2xx response
            if response.status_code != 204:
                res_data = response.json()
            auth_token = res_data['token']
            payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
            return auth_token,payment_method_string
        self.auth, self.payment_id = get_auth_token_and_payment_method_id()
        self.headers['x-resy-auth-token'] = self.auth
        self.headers['x-resy-universal-auth'] = self.auth

    def adjust_date(self):
            '''create date '''
            today = DT.date.today()
            nextweek: DT.date = today + DT.timedelta(days=7)
            adjusted_date: DT.date = nextweek + DT.timedelta(days=self.time_delta)
            return adjusted_date.strftime('%Y-%m-%d') # '2023-08-22'

    def get_venue_id(self, resQuery: str) -> int:
        '''return resy venue ID based on query'''
        url_path = f'https://api.resy.com/3/venue?url_slug={resQuery}&location=ny'
        params = (
        ('x-resy-auth-token',  self.auth),
        ('lat', '0'),
        ('long', '0')
        )
        response = r.get(url_path, headers=self.headers) #, params=params)
        dat = response.json()
        resyID = dat['id']['resy']
        return resyID
    
    def get_avail_times_for_venue(self, venue_id: int) -> List[dict]: 
        if len(self.booked_dates) == 1:
            self.time_delta += 7
            self.date = self.adjust_date()
            print('Entered len = 1 loop')
        if len(self.booked_dates) > 1:
            self.time_delta += 1
            self.date = self.adjust_date()
            print('Entered len > 1 loop')
        url_path = f'https://api.resy.com/4/find?lat=0&long=0&day={self.date}&party_size=2&venue_id={venue_id}'
        response = r.get(url_path,headers=self.headers)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            data = response.json()
        results = data['results']
        if len(results['venues'][0]['slots']) > 0:
            open_slots = results['venues'][0]['slots']
            return open_slots
        else:
            raise NoSlotsError('There are no open tables at that restaurant')

    def select_slot(self, open_slots: List[dict]) -> dict:
        '''Choose first slot OR first slot that starts after 8:00pm'''
        # 'date': {'end': '2023-08-21 18:45:00', 'start': '2023-08-21 17:15:00'}
        # next(x for x in the_iterable if x > 3)
        best_slot = None
        for slot in open_slots:
            slot_date: dict = slot.get('date')
            start_time: str = slot_date.get('start')[-8:-6]
            start_time_int: int = int(start_time)
            if start_time_int >= 20:
                best_slot = slot
                return best_slot
        return open_slots[0]

    def create_config_id(self, open_slot: dict) -> str:
        '''create config id token'''
        config_id = open_slot['config']['token']
        # config_dict = open_slot.get('config')
        # config_id = config_dict.get('token')
        return config_id
        
    def create_book_token(self, conf_id: str) -> str:
        '''takes params and makes book token'''
        params = (
                    ('x-resy-auth-token', self.auth),
                    ('config_id', conf_id),
                    ('day', self.date),
                    ('party_size', '2')
                    )
        
        details_request = r.get('https://api.resy.com/3/details', headers=self.headers, params=params)
        details = details_request.json()
        book_token = details['book_token']['value']
        return book_token

    def keep_track_of_booked_dates(self) -> None:
        '''Adds booked to list'''
        self.booked_dates.append(self.date)
    
    def make_reservation(self, book_token: str) -> None:
        # take params and post reservation
        # self.headers['x-resy-auth-token'] = self.auth
        data = {
        'book_token': book_token,
        'struct_payment_method': self.payment_id,
        'source_id': 'resy.com-venue-details'
        }

        response = r.post('https://api.resy.com/3/book', headers=self.headers, data=data)
        response_sc = response.status_code
        response.close()
        if response.status_code != 201:
            raise BookingError(f'There was an error and no reservation was booked. Status code: {response.status_code}')
        self.keep_track_of_booked_dates()
        return response_sc
    '''

    def make_reservation(self,config_id):
        
        params = (
            ('x-resy-auth-token', self.auth),
            ('config_id', config_id),
            ('day', self.date),
            ('party_size', '2'),
        )
        details_request = r.get('https://api.resy.com/3/details', headers=self.headers, params=params)
        details = details_request.json()
        book_token = details['book_token']['value']
        data = {
            'book_token': book_token,
            'struct_payment_method': self.payment_id,
            'source_id': 'resy.com-venue-details'
        }
        response = r.post('https://api.resy.com/3/book', headers=self.headers, data=data)
        response.close()
    '''

    def close_session(self) -> None:
        '''Explicitly close session'''
        data = {
        'struct_payment_method': self.payment_id,
        'source_id': 'resy.com-venue-details'
        }
        closeSes = r.post(url='https://api.resy.com/3/book', data=data, headers={'Connection':'close'})



from typing import List
import requests as r
import resy_config as rc

'''
I feel like I should split all these functions into different files. 
'''

class ResBot():
    '''Spawn to click on buttons and input/submit data on webpage'''
    def __init__(self) -> None:
        self.usr = rc.email
        self.pw = rc.pw
        self.headers = rc.headers

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
    
    def find_table_at_rest(self, venue_id: int, day: int) -> List[str]:






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
    def go_to_link(self, resLink: str) -> None:
        '''Use selenium webdriver to visit the link'''

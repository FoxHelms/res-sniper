from typing import List

'''
I feel like I should split all these functions into different files. 
All selenium stuff in one file
'''

class ResBot():
    '''Spawn to click on buttons and input/submit data on webpage'''
    def __init__(self) -> None:
        '''conf with parameters'''
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

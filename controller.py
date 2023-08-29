from typing import List
import datetime as DT
'''
This should be able to take user input and add it to the list that the resbot checks
'''

def get_rest_from_user(usrStr: str) -> str:
    '''ask user for restaurant name and convert to url string'''
    return usrStr.replace(' ','-').lower()


def adjust_date(time_delta):
    '''adjust date '''
    today = DT.date.today()
    nextweek: DT.date = today + DT.timedelta(days=7)
    adjusted_date: DT.date = nextweek + DT.timedelta(time_delta)
    return adjusted_date.strftime('%Y-%m-%d') # '2023-08-22'

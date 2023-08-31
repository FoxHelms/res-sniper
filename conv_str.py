from typing import List

def get_rest_from_user(usrStr: str) -> str:
    '''Convert user input string to url string'''
    return usrStr.replace(' ','-').lower()



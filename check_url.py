from typing import List
import sockets

s = 'https://resy.com/cities/ny/mischa?date=2023-09-14&seats=2'

def conf_host(usrStr):
    if usrStr[:16] == 'https://resy.com' or usrStr[:20] == 'https://www.resy.com':
        return True
    return False




def get_rest_from_user(usrStr: str) -> str:
    '''Convert user input string to url string'''
    return usrStr.replace(' ','-').lower()


print(sockets.gethostbyname(s))
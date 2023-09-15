from typing import List
import re
from urllib.parse import urlparse

s = 'https://resy.com/cities/ny/mischa?date=2023-09-14&seats=21'


def conf_valid_url(usrStr):
    result = urlparse(usrStr)
    if result.scheme and result.netloc:
        return True
    return False


def conf_host(usrStr):
    if usrStr[:16] == 'https://resy.com' or usrStr[:20] == 'https://www.resy.com':
        return True
    return False

def conf_only_two_query(usrStr):
    try:
        s_queries = re.search('?(.*)', usrStr)
        len_queries = len(s_queries.group(1))
    except:
        return False
    if len_queries <= 24:
        return True
    return False

def conf_link_rest_page(usrStr):
    '''This checks if the link is a restuarant page'''
    if 'cities' in usrStr:
        return True
    else:
        return False

def conf_good_url(usrStr: str) -> str:
    '''Check to make user input is indeed a resy link to a restaurant'''
    if conf_valid_url(usrStr):
        if conf_host(usrStr) and conf_only_two_query(usrStr) and conf_link_rest_page(usrStr):
            return True
    return False

print(conf_good_url(s))
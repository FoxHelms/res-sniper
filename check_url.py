import re
from urllib.parse import urlparse


def conf_valid_url(usrStr) -> bool:
    '''
    To confirm that user input string is a valid internet url and not some form of injection or file'''
    result = urlparse(usrStr)
    if result.scheme and result.netloc:
        return True
    return False


def conf_host(usrStr) -> bool:
    '''
    This confirms that the url host is resy and the schema is https'''
    if usrStr[:16] == 'https://resy.com' or usrStr[:20] == 'https://www.resy.com':
        return True
    return False

def conf_only_two_query(usrStr) -> bool:
    '''This confirms that the user is only submitting the two default query parameters, date and number of seats
    Should protect against submitting malicious queries'''
    try:
        s_queries = re.search('\?(.*)', usrStr)
        len_queries = len(s_queries.group(1))
    except:
        return False
    if len_queries <= 24:
        return True
    return False

def conf_link_rest_page(usrStr) -> bool:
    '''All resy restaurant pages include the 'cities' directory.'''
    if 'cities' in usrStr:
        return True
    else:
        return False

def conf_good_url(usrStr) -> bool:
    '''Check to make user input is indeed a resy link to a restaurant'''
    if conf_valid_url(usrStr):
        if conf_host(usrStr) and conf_only_two_query(usrStr) and conf_link_rest_page(usrStr):
            return True
    return False
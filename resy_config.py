from logincred import login_data
from cryptic import *

'''
Config file for resbot
contains encrypted email, pw, and headers for requests
'''

email = decrypt_message(login_data.get('email'))
pw = decrypt_message(login_data.get('password'))

'''

test_email = 'r6174126@gmail.com'
test_password = '7uEWA%r34#z5'

email = 'foxhelms@gmail.com',
pw = '_9mKxuSu2Wr8&Vx'

        '''

headers = {
    'Authority': 'api.resy.com',
    'Scheme': 'https',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'Cache-Control': 'no-cache',
    'Origin': 'https://resy.com',
    'Referer': 'https://resy.com/',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': 'macOS',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-origin': 'https://resy.com'
}
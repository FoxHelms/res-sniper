from logincred import login_data
from encryption import *

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
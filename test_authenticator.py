import pytest
from resbot import Authenticator
import resy_config as rc


def test_get_auth_token():
    '''Check the auth token'''
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9'
    tokenGen, extra  = Authenticator.get_auth_and_payment(rc.email, rc.pw)
    assert tokenGen[:36] == tokenStr

def test_get_auth_fails_with_bad_creds():
    '''tokenGen, extra  = Authenticator.get_auth_and_payment('curious@george.com', 'manwiththeyellowHat')
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9'
    assert tokenGen[:36] != tokenStr'''

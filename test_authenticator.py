import pytest
from resbot import Authenticator
import resy_config as rc

@pytest.fixture
def auth():
    '''init a resy session'''
    # self.test_id: str = '59679'  '59679' = el coco '8579' = shukette
    return Authenticator(rc.email,rc.pw)

def test_get_auth_token(auth):
    '''Check the auth token'''
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9'
    tokenGen, extra = auth.get_auth_and_payment()
    assert tokenGen[:36] == tokenStr

def test_get_auth_fails_with_bad_creds():
    bad_a = Authenticator('curious@george.com', 'manwiththeyellowHat')
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9'
    tokenGen, extra = bad_a.get_auth_and_payment()
    assert tokenGen[:36] != tokenStr

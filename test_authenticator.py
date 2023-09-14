import pytest
from unittest.mock import patch, Mock
import resbot



@patch('resbot.requester')
def test_get_auth_token(mock_req):
    '''Passing correct login data should return a token and id number'''
    fake_auth = {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9', 'payment_method_id':69}
    mock_req.return_value = fake_auth
    get_token, pmid = resbot.Authenticator.get_auth_and_payment('curious@george.com', 'manwiththeyellowHat')
    assert get_token == fake_auth['token']
    assert pmid == '{"id":69}'

@patch('resbot.r.post')
def test_resy_being_mean_throws_excep(mock_post):
    '''Passing correct login data should raise bad login exception if resy is being unreasonable'''
    mock_response = Mock()
    mock_post.return_value = mock_response
    mock_post.return_value.status_code = 500
    with pytest.raises(resbot.BadLogin):
        resbot.Authenticator.get_auth_and_payment('curious@george.com', 'manwiththeyellowHat')


def test_get_auth_w_no_creds():
    '''Passing blank login info should result in an error'''
    with pytest.raises(resbot.BadLogin):
        resbot.Authenticator.get_auth_and_payment('', '')

def test_get_auth_w_bad_creds():
    '''Passing incorect login info should result in an error'''
    with pytest.raises(resbot.BadLogin):
        resbot.Authenticator.get_auth_and_payment('bad_username', 'bad_password')
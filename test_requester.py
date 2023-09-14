from unittest.mock import patch, Mock
import pytest
import resbot
from resbot import InvalidMethod

hdrs: dict = {
            'accept-language': 'en-US,en;q=0.9',
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

def test_bad_method_raises_exception():
    '''a method other than what I've defined should raise exception'''
    bad_method = 'give'
    good_url = 'https://www.google.com'
    with pytest.raises(InvalidMethod):
        resbot.requester(bad_method, good_url)


@patch('resbot.r.get')
def test_get_method(mock_get):
    '''Calling the requester with get should call  requests.get with headers arg'''
    mock_response = Mock()
    mock_get.return_value = mock_response
    resbot.requester('get', 'https://api.website.com')
    mock_get.assert_called_with('https://api.website.com', headers=hdrs)


@patch('resbot.requester')
def test_get_returns_json(mock_get):
    fake_json = {'name':'Scooby'}
    mock_get.return_value = fake_json
    assert resbot.requester('get', 'https://www.google.com') == fake_json

@patch('resbot.r.post')
def test_post_method(mock_get):
    '''Calling the requester with post should call requests.post with headers and data (not json!!) arg'''
    fake_data = {'name':'Scooby'}
    mock_response = Mock()
    mock_get.return_value = mock_response
    resbot.requester(m='post', upath='https://api.website.com', name='Scooby')
    mock_get.assert_called_with('https://api.website.com', headers=hdrs, data=fake_data)
    

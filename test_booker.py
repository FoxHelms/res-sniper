import pytest
from unittest.mock import patch, Mock
from resbot import Booker


hdrs: dict = {
            'accept-language': 'en-US,en;q=0.9',
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }



@patch('resbot.requester')
def test_create_valid_book_token(mock_get_tables): 
    '''Should return list of available dates'''
    # t['search']['hits'][0]['inventory_reservation']
    token_value = "t8iuqLd8saEfP66Nd2HlVfLBfcVe0x2f1|7p9dSg3|ZD03egn6BqtW9DwsvdnlJ42UNRZw|NjPsns58pb4p7DP21xbcMBr9qyinhnT|05rfqWM_Ar6saEY|02g|Un4fQvm44dSYGv1BKfh6dGpEABirXenIqRvDWhV73Tpz0GoPONoazjugPnFNMu|TKDi|lD5ifBIwWBRcBIwn0PhL5qYzialE|nWsx_CpxHLo7Fnlo5ro0moYeiBGzanxeIs|kNWC5Vi1pHgLTrhsSFJB8K|111hGXXe6zR9b1uc9LTL4EDcT0mP42TQEdicvcrMQ|ZDlufI8Ge_BHygNDQpuNVRdXUa|o0jv7uwlcr2_8pfD4JGGuVTO9nmCJBIcNMAwlTNkx6GcgJ|sSMmjgM7vBgVQhso1E7TJ9|6pH7SI1MYYjsh_W29rnUlsTGmX7jTyuNXns9tAiTUSgfOr6qBmDpl7DQkpVLuFXThTw_LVa|2lD9sdrDuLDqTTBIeI6327BGv5AVA9|2ZMNrDxyEdc7ruQqAwaQQABcchFwYEEVDYctg9PHRgTDPRPpYPyYEXeivLNfRP2xAz_aGWBRB669n3Q7tjX4Gcyz_hBs|VLZMTTtN00f9wheKhGEHqagZG|qoVBQYN_WaMxBCxaC8BWuxsOyCJ9jOoZyty96pmhK5InwKq9OzY0BK"
    fake_book_token = {'book_token':{'value': token_value}}
    mock_get_tables.return_value = fake_book_token
    get_token = Booker.create_book_token('auth', 'res time', 'conf token') # cls, auth, all_time_confs_key, all_time_confs_value
    assert get_token == token_value
    assert len(token_value) > 600
    assert '|' in token_value

@patch('resbot.requester')
def test_make_reservation(mock_post_res): # bot arg
    '''Make res should result in status code 201'''
    token_value = "t8iuqLd8saEfP66Nd2HlVfLBfcVe0x2f1|7p9dSg3|ZD03egn6BqtW9DwsvdnlJ42UNRZw|NjPsns58pb4p7DP21xbcMBr9qyinhnT|05rfqWM_Ar6saEY|02g|Un4fQvm44dSYGv1BKfh6dGpEABirXenIqRvDWhV73Tpz0GoPONoazjugPnFNMu|TKDi|lD5ifBIwWBRcBIwn0PhL5qYzialE|nWsx_CpxHLo7Fnlo5ro0moYeiBGzanxeIs|kNWC5Vi1pHgLTrhsSFJB8K|111hGXXe6zR9b1uc9LTL4EDcT0mP42TQEdicvcrMQ|ZDlufI8Ge_BHygNDQpuNVRdXUa|o0jv7uwlcr2_8pfD4JGGuVTO9nmCJBIcNMAwlTNkx6GcgJ|sSMmjgM7vBgVQhso1E7TJ9|6pH7SI1MYYjsh_W29rnUlsTGmX7jTyuNXns9tAiTUSgfOr6qBmDpl7DQkpVLuFXThTw_LVa|2lD9sdrDuLDqTTBIeI6327BGv5AVA9|2ZMNrDxyEdc7ruQqAwaQQABcchFwYEEVDYctg9PHRgTDPRPpYPyYEXeivLNfRP2xAz_aGWBRB669n3Q7tjX4Gcyz_hBs|VLZMTTtN00f9wheKhGEHqagZG|qoVBQYN_WaMxBCxaC8BWuxsOyCJ9jOoZyty96pmhK5InwKq9OzY0BK"
    fake_data = {
        'book_token': token_value,
        'struct_payment_method': '',
        'source_id': 'resy.com-venue-details'
        }
    mock_response = Mock()
    mock_post_res.return_value = mock_response
    Booker.make_reservation(token_value, '', '') # book_token: str, auth, p_id
    mock_post_res.assert_called_with('post','https://api.resy.com/3/book', '', **fake_data)
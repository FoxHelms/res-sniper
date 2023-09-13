import pytest
from resbot import InvalidMethod, requester




def test_bad_method_raises_exception():
    '''a method other than what I've defined should raise exception'''
    bad_method = 'give'
    good_url = 'https://www.google.com'
    with pytest.raises(InvalidMethod):
        requester(bad_method, good_url)

def test_get_method_returns_correct_page():
    '''requester returns json of a page, so find a page with good json, i guess. or add a check to requester for json or not...'''

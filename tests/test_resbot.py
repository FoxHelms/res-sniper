import pytest
import requests
from resbot import BookingError, NoSlotsError, ResBot


@pytest.fixture
def bot():
    '''init a resy session'''
    return ResBot()

def test_get_auth_token(bot):
    '''Check the auth token'''
    tokenStr = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJleHAiOjE2OTYyMTczMTcsInVpZCI6MzY0NTA2NTIsImd0IjoiY29uc3VtZXIiLCJncyI6W10sImxhbmciOiJlbi11cyIsImV4dHJhIjp7Imd1ZXN0X2lkIjoxMjM0NDM3MjJ9fQ.AOF-LCJqoBmEjEfAuP1GjoZ6cfe9PzdZsP96X0g1rLaDTVAiulKJt2Qsso-fQiD5BKrj_hhKMlt7vwaa1Vx77pA-AOuRc5As0iYqQFdLhNMUjeTtFC6SwFtxslFiCYd5n4bdMJEc55_VgCY66fVvYMvgiD7jhhw2IsOuvhWCE7ZrJhMB'
    tokenGen = bot.auth
    assert tokenGen[:36] == tokenStr[:36]

def test_get_venue_id_with_known_value(bot):
    '''the query 'shukette' should return 8579'''
    venue_id = bot.get_venue_id('shukette')
    assert venue_id == 8579

def test_find_table_at_el_coco(bot):
    '''el coco should return 38'''
    open_tables = bot.get_avail_times_for_date(bot.test_day,bot.test_id)
    assert len(open_tables) == 38


def test_don_angie_raises_error(bot):
    venue_id = bot.get_venue_id('don-angie')
    with pytest.raises(NoSlotsError):
        open_tables = bot.get_avail_times_for_date(bot.test_day,venue_id)

def test_create_conf_id(bot):
    open_tables = bot.get_avail_times_for_date(bot.test_day,bot.test_id)
    open_table = [open_tables[0]]
    id = bot.create_config_id(open_table)
    assert id == 'rgs://resy/59705/1657851/3/2023-08-21/2023-08-21/12:00:00/2/Indoor'

def test_create_book_token(bot):
    open_tables = bot.get_avail_times_for_date(bot.test_day,bot.test_id)
    open_table = [open_tables[0]]
    id = bot.create_config_id(open_table)
    book_token = bot.create_book_token(id)
    assert len(book_token) == 761

def test_make_reservation(bot):
    open_tables = bot.get_avail_times_for_date(bot.test_day,bot.test_id)
    open_table = [open_tables[-6]]
    id = bot.create_config_id(open_table)
    book_token = bot.create_book_token(id)
    success = bot.make_reservation(book_token)
    assert success.status_code == 200 or 201 or 202

def test_make_reservation_raises_error(bot):
    open_tables = bot.get_avail_times_for_date(bot.test_day,bot.test_id)
    open_table = [open_tables[-6]]
    id = bot.create_config_id(open_table)
    book_token = bot.create_book_token(id)
    book_token = book_token + 'string to fail booking'
    with pytest.raises(BookingError):
        bot.make_reservation(book_token)

def test_check_length_check_list(bot):
    assert bot.size() == 2


import pytest
from resbot import ResBot


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
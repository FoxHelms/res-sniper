import pytest
import requests
from resbot import BookingError, NoSlotsError, ResBot


@pytest.fixture
def bot():
    '''init a resy session'''
    # self.test_id: str = '59679'  '59679' = el coco '8579' = shukette
    return ResBot()





import pytest
import resbot
from unittest.mock import patch

def test_url_to_name_and_city_ny():
    '''should be able to get thing for anywhere in world'''
    test_url_1 = 'https://resy.com/cities/ny/shukette?date=2023-09-12&seats=2'
    test_name_1 = 'shukette'
    test_city_1 = 'ny'
    gen_city_1, gen_name_1 = resbot.RestaurantIdentifier.convert_url(test_url_1)
    assert gen_city_1 == test_city_1
    assert gen_name_1 == test_name_1

def test_url_to_name_and_city_rmi():
    '''should be able to get thing for anywhere in world'''
    # test_url_1 = 'https://resy.com/cities/ny/shukette?date=2023-09-12&seats=2'
    test_name_2 = 'kruse-and-muer-on-main'
    test_city_2 = 'rmi'
    test_url_2 = 'https://resy.com/cities/rmi/kruse-and-muer-on-main?date=2023-09-14&seats=2'
    gen_city_2, gen_name_2 = resbot.RestaurantIdentifier.convert_url(test_url_2)
    assert gen_city_2 == test_city_2
    assert gen_name_2 == test_name_2

def test_url_to_name_and_city_tky():
    '''should be able to get thing for anywhere in world'''
    test_url_3 = 'https://resy.com/cities/tky/ginza-yoshoku-mikasa-kaikan-ikebukuro-parco?date=2023-09-14&seats=2'
    test_name_3 = 'ginza-yoshoku-mikasa-kaikan-ikebukuro-parco'
    test_city_3 = 'tky'
    gen_city_3, gen_name_3 = resbot.RestaurantIdentifier.convert_url(test_url_3)
    assert gen_city_3 == test_city_3
    assert gen_name_3 == test_name_3

@patch('resbot.RestaurantIdentifier.convert_url')
def test_shukette_id(mock_convert_url):
    '''Shukette (NY) should return known venue ID'''
    shukette_package = ('ny','shukette')
    shukette_id = 8579
    mock_convert_url.return_value = shukette_package
    assert resbot.RestaurantIdentifier.get_venue_id('url_for_shukette') == shukette_id

@patch('resbot.RestaurantIdentifier.convert_url')
def test_shikara_id(mock_convert_url):
    '''Shikara (Navi Mumbai) should return known venue ID'''
    shikara_package = ('nvmm','shikara-5371')
    shikara_id = 61640
    mock_convert_url.return_value = shikara_package
    assert resbot.RestaurantIdentifier.get_venue_id('url_for_shukette') == shikara_id




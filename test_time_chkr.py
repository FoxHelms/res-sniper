from unittest.mock import patch, Mock
import resbot

@patch('resbot.requester')
def test_for_open_tables_at_restaurant(mock_get_tables):
    '''Should return list of available dates'''
    # t['search']['hits'][0]['inventory_reservation']
    fake_list_dates = ['2023-09-11', '2023-09-12', '2023-09-13']
    fake_page = {'search':{'hits':[{'inventory_reservation':fake_list_dates}]}}
    mock_get_tables.return_value = fake_page
    get_list = resbot.TimeChecker.check_if_slots('rest name')
    assert get_list == fake_list_dates

@patch('resbot.requester')
def test_no_empty_tables_returns_false(mock_get_tables):
    '''An empty list should return false'''
    # t['search']['hits'][0]['inventory_reservation']
    fake_list_dates = []
    fake_page = {'search':{'hits':[{'inventory_reservation':fake_list_dates}]}}
    mock_get_tables.return_value = fake_page
    get_list = resbot.TimeChecker.check_if_slots('rest name')
    assert get_list == False

@patch('resbot.requester')
def test_status_error_returns_false(mock_get_tables):
    '''An status error should return false'''
    # t['search']['hits'][0]['inventory_reservation']
    mock_response = Mock()
    mock_get_tables.return_value = mock_response
    mock_get_tables.return_value.status_code = 500
    get_list = resbot.TimeChecker.check_if_slots('rest name')
    assert get_list == False


@patch('resbot.requester')
def test_get_confs_and_times(mock_requester):
    '''Should get conf codes and such for available dates'''
    # ['results']['venues'][0]['slots']
    fake_ven_id = 'ven_id'
    fake_avail_dates = ['2023-09-11']
    fake_time_1 = '2023-09-11 17:15:00'
    fake_time_2 = '2023-09-11 20:00:00'
    fake_token_1 = 'peanut butter'
    fake_token_2 = 'jelly'
    mock_requester.return_value = {'results':{'venues':[{'slots':[
        {'date':{'start':fake_time_1},'config':{'token':fake_token_1}},
        {'date':{'start':fake_time_2},'config':{'token':fake_token_2}},
        ]}]}}
    get_dict = resbot.TimeChecker.get_times_confs_for_ven(fake_ven_id,fake_avail_dates)
    assert get_dict[fake_time_1] == fake_token_1
    assert get_dict[fake_time_2] == fake_token_2

@patch('resbot.requester')
def test_get_ct_returns_empty_dict_for_no_slots(mock_requester):
    '''If there are no slots then should return empty dictionary'''
    # ['results']['venues'][0]['slots']
    fake_ven_id = 'ven_id'
    fake_avail_dates = ['2023-09-11']
    empty_list = []
    mock_requester.return_value = {'results':{'venues':[{'slots':empty_list}]}}
    get_dict = resbot.TimeChecker.get_times_confs_for_ven(fake_ven_id,fake_avail_dates)
    assert len(get_dict) == 0


def test_select_time_after_threshold():
    '''Of time options, best time should be the one that is at or later than 8pm'''
    fake_times = {'2023-09-11 17:15:00': 'peanut butter', '2023-09-11 20:00:00':'jelly'}
    later_time = resbot.TimeChecker.select_time(fake_times)
    assert fake_times[later_time] == 'jelly'

def test_select_earliest_time():
    '''Of time options, if no time is after 8pm, then first option is returned'''
    fake_times = {'2023-09-11 17:15:00': 'peanut butter', '2023-09-11 19:00:00':'jelly'}
    later_time = resbot.TimeChecker.select_time(fake_times)
    assert fake_times[later_time] == 'peanut butter'


def test_find_table(): # bot arg
    '''el coco should return at least one table
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    assert len(open_tables) > 0
    '''


def test_select_slot(): # bot arg
    '''should return dictionary where date:start is greater than 20
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    best_table = bot.select_slot(open_tables)
    date_dict = best_table.get('date')
    start_time = date_dict.get('start')
    assert type(best_table) == dict
    assert (int(start_time[-8:-6]) >= 20) or (best_table == open_tables[0])
    '''

def test_create_conf_id(): # bot
    '''Should create config id of reliable format
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    open_table = open_tables[0]
    id = bot.create_config_id(open_table)
    assert 'rgs://resy' in id
    '''
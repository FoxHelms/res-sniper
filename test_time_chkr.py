
def test_find_table(bot):
    '''el coco should return at least one table'''
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    assert len(open_tables) > 0


def test_select_slot(bot):
    '''should return dictionary where date:start is greater than 20'''
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    best_table = bot.select_slot(open_tables)
    date_dict = best_table.get('date')
    start_time = date_dict.get('start')
    assert type(best_table) == dict
    assert (int(start_time[-8:-6]) >= 20) or (best_table == open_tables[0])

def test_create_conf_id(bot):
    '''Should create config id of reliable format'''
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    open_table = open_tables[0]
    id = bot.create_config_id(open_table)
    assert 'rgs://resy' in id
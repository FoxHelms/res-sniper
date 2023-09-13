
def test_create_book_token(): # bot arg
    '''Should create book token of reliable length
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    open_table = open_tables[0]
    id = bot.create_config_id(open_table)
    book_token = bot.create_book_token(id)
    assert len(book_token) == 761
    '''

def test_make_reservation(): # bot arg
    '''Should make reservation
    open_tables = bot.get_avail_times_for_venue(bot.test_id)
    best_table = bot.select_slot(open_tables)
    id = bot.create_config_id(best_table)
    book_token = bot.create_book_token(id)
    success = bot.make_reservation(book_token)
    assert success == 201
    '''

def test_make_reservation_raises_error(): # bot arg
    '''Unrecognizable book token should result in booking failure
    open_tables = bot.get_avail_times_for_venue(int(bot.test_id))
    open_table = open_tables[0]
    id = bot.create_config_id(open_table)
    book_token = bot.create_book_token(id)
    bad_book_token = book_token + 'string to fail booking'
    with pytest.raises(BookingError):
        bot.make_reservation(bad_book_token)
    '''
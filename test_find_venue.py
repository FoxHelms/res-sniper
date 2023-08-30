from find_venue_id import get_venue_id

def test_get_venue_id_with_known_value():
    '''the query 'shukette' should return 8579'''
    venue_id = get_venue_id('shukette')
    assert venue_id == 8579

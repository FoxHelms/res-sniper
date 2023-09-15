from check_url import conf_good_url, conf_valid_url 


def test_invalid_url():
    s = 'ftp.sketchy.com'
    assert conf_good_url(s) == False

def test_wrong_host_returns_false():
    s1 = 'https://resty.com'
    s2 = 'https://google.com'
    assert conf_good_url(s1) == False
    assert conf_good_url(s2) == False

def test_too_many_queries_returns_false():
    s = 'https://resy.com/cities/ny/mischa?date=2023-09-14&seats=2&virus=Trojan'
    assert conf_good_url(s) == False

def test_not_rest_page_returns_false():
    s = 'https://resy.com/?date=2023-09-14&seats=2'
    assert conf_good_url(s) == False
    





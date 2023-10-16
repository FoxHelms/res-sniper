from app import app


def test_post_good_link():
    '''Good link submission'''
    with app.test_client() as c:
        s = 'https://resy.com/cities/ny/mischa?date=2023-09-14&seats=21'
        t_data = {'userRest':s}
        d_post = c.post('/', data=t_data, follow_redirects=True)
        assert d_post.status_code == 200

def test_error_page_loads():
    '''Load error page!'''
    with app.test_client() as c:
        t_data = {'ResyEmail':'gibberish', 'ResyPW': 'gibberish'}
        d_post = c.post('/login', data=t_data, follow_redirects=True)
        assert b'<a href="/">Try Again</a>' in d_post.data





from app import app
from logincred import login_data
from encryption import encrypt_message

def test_home_page_redirect():
    '''Test that you are redirected to login page if no logindata is provided'''
    response = app.test_client().get('/')
    assert response.status_code == 200
    if login_data:
        assert b'<h1>Reservation Sniper</h1>' in response.data
    else:
        assert b'<h1>Login</h1>' in response.data

def test_encryption():
    '''Test that a password provided is not the same as the password stored'''
    human_readable = 'ThisIsAHumanReadablePassword'
    encrypted = encrypt_message(human_readable)
    assert human_readable != encrypted


def test_post_good_link():
    '''Good link submission'''
    with app.test_client() as c:
        s = 'https://resy.com/cities/ny/mischa?date=2023-09-14&seats=21'
        t_data = {'userRest':s}
        d_post = c.post('/', data=t_data, follow_redirects=True)
        assert d_post.status_code == 200

def test_post_bad_link():
    '''Good link submission'''
    with app.test_client() as c:
        s = 'https://resy.com'
        t_data = {'userRest':s}
        d_post = c.post('/', data=t_data, follow_redirects=True)
        assert b'<a href="/">Try Again</a>' in d_post.data

def test_error_page_loads():
    '''Load error page!'''
    with app.test_client() as c:
        t_data = {'ResyEmail':'gibberish', 'ResyPW': 'gibberish'}
        d_post = c.post('/login', data=t_data, follow_redirects=True)
        assert b'<a href="/">Try Again</a>' in d_post.data





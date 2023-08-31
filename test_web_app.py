from app import app
from logincred import login_data
from cryptic import encrypt_message

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
    assert human_readable not in str(encrypted)

def test_post_name():
    with app.test_client() as c:
        t_data = {'userRest':'Mischa'}
        d_post = c.post('/', data=t_data)
        updated_page = app.test_client().get('/')
        assert d_post.status_code == 302
        assert updated_page.status_code == 200
        assert b'<td>Mischa</td>' in updated_page.data

def test_error_page_loads():
    '''Load error page!'''
    with app.test_client() as c:
        t_data = {'ResyEmail':'gibberish', 'ResyPW': 'gibberish'}
        d_post = c.post('/login', data=t_data, follow_redirects=True)
        assert b'<a href="/">Try Again</a>' in d_post.data

def test_login_to_account():
    '''Should log into test account'''
    with app.test_client() as c:
        t_data = {'ResyEmail':'r6174126@gmail.com', 'ResyPW': '7uEWA%r34#z5'}
        d_post = c.post('/login', data=t_data)
        updated_page = app.test_client().get('/')
        assert d_post.status_code == 302
        assert updated_page.status_code == 200




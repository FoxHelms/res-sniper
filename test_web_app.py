from app import app
from logincred import login_data
from cryptic import encrypt_message

def test_home_page():
    '''Test that you can successfully get to the homepage IF logindata is provided'''
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

def test_post_name_should_fail():
    with app.test_client() as c:
        t_data = {'userRest':'sushi den'}
        d_post = c.post('/', data=t_data)
        assert d_post.status_code == 500
        assert b'<h1>KeyError</h1>' or b'<h1>Internal Server Error</h1>' in d_post.data




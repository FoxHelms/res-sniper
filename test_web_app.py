from app import app

def test_home_page():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'<h1>Reservation Sniper</h1>' in response.data
    
'''
def test_post_name():
    with app.test_client() as c:
        response = c.post('/', 'userRest=Mischa')
        assert response.status_code == 302
        assert b'<td>Mischa</td>' in response.data'''
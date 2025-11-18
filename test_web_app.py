from app import app


def test_post_good_link():
    '''Good link submission'''
    with app.test_client() as c:
        with c.session_transaction() as sess:
            sess['user'] = 'r6174126@gmail.com'
        
        hdrs = {
        'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
        'Origin': 'https://resy.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        s = 'https://resy.com/cities/new-york-ny/venues/shukette?seats=2&date=2025-11-18'
        t_data = {'userRest':s}
        d_post = c.post('/api/restaurants', json=t_data, headers=hdrs, follow_redirects=True)
        print(d_post.data)
        assert d_post.status_code == 201

def test_error_page_loads():
    '''Load error page!'''
    with app.test_client() as c:
        t_data = {'ResyEmail':'gibberish', 'ResyPW': 'gibberish'}
        d_post = c.post('/api/login', json=t_data, follow_redirects=True)
        print(d_post.data)
        assert b'<a href="/">Try Again</a>' in d_post.data





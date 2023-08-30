import requests as r
import urllib

hdrs = {
    'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'Origin': 'https://resy.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}



data = {
            'email': 'foxhelms@gmail.com',
            'password': '_9mKxuSu2Wr8&Vx'
            }

s = r.Session()
s.headers.update(hdrs)

s.proxies = {
   'https': 'http://144.49.99.190:8080',
   'https': 'http://144.49.99.190:8080',
}

s.cookies.clear()

post_path = 'https://api.resy.com/3/auth/password'
get_path = 'https://api.resy.com/3/venue?url_slug=shukette&location=ny'
base_path = 'https://api.resy.com'


try:
    response = s.post(post_path, data=data, verify=False)
except r.exceptions.Timeout as e:

    # Maybe set up for a retry
    print(e)

except r.exceptions.RequestException as e:
    print(e)

print(response.status_code)
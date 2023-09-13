import requests as r

def requester(m,upath,*params, **data): # (optional data)
    hdrs: dict = {
            'accept-language': 'en-US,en;q=0.9',
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
    if m == 'postj':
        response: r.models.Response = r.post(upath, headers=hdrs, json=data)
    if m == 'post':
        response: r.models.Response = r.post(upath, headers=hdrs, data=data)
    if m == 'get':
        if params:
            response: r.models.Response = r.get(upath, headers=hdrs, params=params)
        response: r.models.Response = r.get(upath, headers=hdrs)
    response.raise_for_status()  # raises exception when not a 2xx response
    if response.status_code != 204:
        return response.json()


s = 'https://resy.com/cities/rmi/kruse-and-muer-on-main?date=2023-09-12&seats=2'

t = r.get(s)

print(t.text)
'''

We have a way of checking if there are any open tables 

We don't need to adjust dates at all, we can just choose from the dates on the list. 


'''


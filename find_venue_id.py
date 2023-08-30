import requests as r

def get_venue_id(resQuery: str) -> int:
        '''return resy venue ID based on query'''
        url_path = f'https://api.resy.com/3/venue?url_slug={resQuery}&location=ny'
        hdrs = {
            'Authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
            'Origin': 'https://resy.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }
        response = r.get(url_path, headers=hdrs)
        dat = response.json()
        resyID = dat['id']['resy']
        return resyID

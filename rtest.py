import requests

headers = {
    'authority': 'api.resy.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://resy.com',
    'referer': 'https://resy.com/',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'x-origin': 'https://resy.com',
}

json_data = {
    'geo': {
        'latitude': 40.712941,
        'longitude': -74.006393,
    },
    'highlight': {
        'pre_tag': '<b>',
        'post_tag': '</b>',
    },
    'per_page': 5,
    'query': 'shukett',
    'slot_filter': {
        'day': '2023-09-13',
        'party_size': 2,
    },
    'types': [
        'venue',
        'cuisine',
    ],
}

response = requests.post('https://api.resy.com/3/venuesearch/search', headers=headers, json=json_data)

print(response.status_code)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"geo":{"latitude":40.712941,"longitude":-74.006393},"highlight":{"pre_tag":"<b>","post_tag":"</b>"},"per_page":5,"query":"shukett","slot_filter":{"day":"2023-09-13","party_size":2},"types":["venue","cuisine"]}'
#response = requests.post('https://api.resy.com/3/venuesearch/search', headers=headers, data=data)
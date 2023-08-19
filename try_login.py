import requests


'''
This works and header is updated to my macbook
'''


headers = {
	 'origin': 'https://resy.com',
	 'accept-encoding': 'gzip, deflate, br',
	 'x-origin': 'https://resy.com',
	 'accept-language': 'en-US,en;q=0.9',
	 'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"',
	 'content-type': 'application/x-www-form-urlencoded',
	 'accept': 'application/json, text/plain, */*',
	 'referer': 'https://resy.com/',
	 'authority': 'api.resy.com',
	 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}




def login(username,password):
	data = {
	  'email': username,
	  'password': password
	}

	response = requests.post('https://api.resy.com/3/auth/password', headers=headers, data=data)
	res_data = response.json()
	auth_token = res_data['token']
	payment_method_string = '{"id":' + str(res_data['payment_method_id']) + '}'
	return auth_token,payment_method_string

pee, poop = login('foxhelms@gmail.com', '_9mKxuSu2Wr8&Vx')

print(f'Token: {pee}')

print(f'Payment: {poop}')

import requests as r

url = 'https://www.bne.com.au/passenger/flights/arrivals-departures'

resp = r.get(url)

print(type(resp))
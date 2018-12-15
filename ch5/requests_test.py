import requests
url_1 = 'https://en.wikipedia.org/wiki/Nobel_Prize'
url_2 = 'https://data.ct.gov/resource/y6p2-px98.json?category=Fruit&item=Peaches'

response = requests.get(url_1)
dir(response)
response.status_code
response.headers
response.text

response = requests.get(url_2)
response.status_code
data = response.json()
data[0].keys()
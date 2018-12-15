import requests
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from tools.mongodb import get_mongo_db

REST_EU_ROOT_URL = "https://restcountries.eu/rest/v1"

def REST_country_request(field='all', name=None, params=None):

    headers = {'User-Agent': 'Mozilla/5:0'}

    if not params:
        params = {}
    
    if field == 'all':
        return requests.get(REST_EU_ROOT_URL + '/all')

    url = f"{REST_EU_ROOT_URL}/{field}/{name}"
    print('Requesting URL: ' + url)
    response = requests.get(url, params=params, headers=headers)

    if not response.status_code == 200:
        raise Exception('Request failed with status code ' \
        + str(response.status_code))

    return response

# response = REST_country_request('currency', 'usd')
# print(response.json())

db_nobel = get_mongo_db('nobel_prize')
col = db_nobel['country_data']

response = REST_country_request()

col.insert(response.json())

res = col.find({'currencies': {'$in': ['USD']}})
print(list(res))

# or use mongo shell to check the content:
# use nobel_prize
# db.country_data.find({}).pretty()
# db.country_data.find({'currencies': {'$in': ['USD']}}).pretty()
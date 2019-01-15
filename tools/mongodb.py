from pymongo import MongoClient
import pandas as pd
import json

def get_mongo_db(db_name, host='localhost', port=27017, username=None, password=None):
    """ Get named database from MongoDB with/out authentication """

    if username and password:
        mongo_uri = f'mongodb://{username}:{password}@{host}/{db_name}'
        conn = MongoClient(mongo_uri)
    
    else:
        conn = MongoClient(host, port)

    return conn[db_name]

def mongo_to_df(db_name, collection, query={}, host='localhost', port=27017, username=None, password=None, no_id=True):
    """ create a dataframe from mongodb collection """
    db = get_mongo_db(db_name, host, port, username, password)
    records = db[collection].find(query)

    df = pd.DataFrame(list(records))

    if no_id:
        del df['_id']

    return df

def df_to_mongo(df, db_name, collection, host='localhost', port=27017, username=None, password=None):
    """ save a dataframe to mongodb collection """
    db = get_mongo_db(db_name, host, port, username, password)
    db[collection].drop()
    db[collection].insert_many(json.loads(df.to_json(orient='records', date_format='iso')))
    
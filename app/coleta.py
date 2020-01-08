# Import the Twython class
from twython import Twython
import json
import pandas as pd
from pymongo import MongoClient


# Create connection to MongoDB
client = MongoClient('localhost', 27017)
db = client['db_teste_itau1']
collection = db['teste4']

# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

# Instantiate an object
python_tweets = Twython(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])

# Create our query
query = {"q": "#devops",
        #'result_type': 'popular',
        "count": 5,
        #'lang': 'en',
        "include_entities": "true",
        }

print(query)

dict_ = {'user': [], 'date': [], 'text': [], 'favorite_count': [], 'followers': []}
for status in python_tweets.search(**query)['statuses']:
    dict_['user'].append(status['user']['screen_name'])
    dict_['date'].append(status['created_at'])
    dict_['text'].append(status['text'])
    dict_['favorite_count'].append(status['favorite_count'])
    dict_['followers'].append(status['user']['followers_count'])

print(dict_)
# Structure data in a pandas DataFrame for easier manipulation
df = pd.DataFrame(dict_)
df.sort_values(by='favorite_count', inplace=True, ascending=False)
#df.to_csv('hash_cloudfirst.csv')
print(df)
records = json.loads(df.T.to_json()).values()
db.teste4.insert_many(records)
#collection.insert(dict_)
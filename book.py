# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 12:07:21 2016

@author: Su
"""

import twitter
def login():
    CONSUMER_KEY = 'O3d2eaHxKqqncsQ2FO9AoEzoD'
    CONSUMER_SECRET ='SEVuO0x4l1ljzE5O73wSKSxZKL9ToR7GVTqVUmdnd8gy5TnKmy'
    OAUTH_TOKEN = '3319954537-sy0AkxZKVpHPpjRy5OzHzMcr2fm2FXPRe1ngebG'
    OAUTH_TOKEN_SECRET = '3MJVHdQL0UELGCXFXdDzbracSacbhH5qWQBa0uiC4UDBZ'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN,OAUTH_TOKEN_SECRET,CONSUMER_KEY,CONSUMER_SECRET)
    twitter_api = twitter.Twitter(auth = auth)
    return twitter_api
twitter_api = login()

q = ['Trump2016', 'Hillary2016','#imwithher','#makeamericagreatagain','election2016','Donald Trump','Hillary Clinton','presidentialelections2016','donald trump','hillary clinton']
print(twitter_api)
twitter_stream = twitter.TwitterStream(auth = twitter_api.auth)
stream = twitter_stream.statuses.filter(track = q, language = 'en')

statuses =[]
no_tweets = 100000
for tweet in stream:
    statuses.append(tweet)
    if len(statuses) == no_tweets:
        break

import nltk
from nltk.corpus import stopwords
# Extracting text, screen names, and hashtags from tweets
status_texts = [ status['text'] 
                 for status in statuses ]
# most mentioned names
screen_names = [ user_mention['screen_name'] 
                 for status in statuses
                     for user_mention in status['entities']['user_mentions'] ]

hashtags = [ hashtag['text'] 
             for status in statuses
                 for hashtag in status['entities']['hashtags'] ]

# Compute a collection of all words from all tweets

words = []
for t in status_texts:
    for w in t.split():
        w = nltk.word_tokenize(w)
        w = nltk.pos_tag(w)
        #get the noun and adj.
        if w[0][1] in ['NN','ADJ'] and w[0][0] not in stopwords.words("english") and w[0][0]not in ['RT','@','http','https']:               
            words.append(w[0][0])

popu_tweets = sorted(statuses, key = lambda s:s['retweet_count'], reverse = True)

from collections import Counter
for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print (c.most_common()[:30]) # top 10
#Using prettytable to display tuples in a nice tabular format
from prettytable import PrettyTable

for label, data in (('Word', words), 
                    ('Screen Name', screen_names), 
                    ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count']) 
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()[:30] ]
    pt.align[label], pt.align['Count'] = 'l', 'r' # Set column alignment
    print (pt)
#the below codes are searching method

"""
WORLD_WOE_ID = 1
US_WOE_ID = 23424977
# Named place to set up a ID
#retrieve the place by using ID

world_trends = twitter_api.trends.place(_id = WORLD_WOE_ID)
us_trends= twitter_api.trends.place(_id = US_WOE_ID)
# Displaying API responses as pretty-printed JSON
import json

print (json.dumps(world_trends, indent=1))
print
print (json.dumps(us_trends, indent=1))
# Example 4. Computing the intersection of two sets of trends
world_trends_set = set([trend['name'] 
                        for trend in world_trends[0]['trends']])

us_trends_set = set([trend['name'] 
                     for trend in us_trends[0]['trends']]) 

common_trends = world_trends_set.intersection(us_trends_set)

print (common_trends)

q = 'trump2016'    # query 

count = 20

# See https://dev.twitter.com/docs/api/1.1/get/search/tweets

search_results = twitter_api.search.tweets(q=q, count=count)

statuses = search_results['statuses']


# Iterate through 5 more batches of results by following the cursor

for _ in range(5):
    print ("Length of statuses", len(statuses))
    try:
        next_results = search_results['search_metadata']['next_results']
    except KeyError as k: # No more results when next_results doesn't exist
        break
        
    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
    
    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

# Show one sample search result by slicing the list...
from nltk.corpus import stopwords
"""


"""
words = [w for t in status_texts
            for w in t.split()
                if len(w) >2 and w not in stopwords.words("english") or w in brown_tags # get the adj
             ]
"""            

# Explore the first 5 items for each...
"""
print (json.dumps(status_texts[0:5], indent=1))
print (json.dumps(screen_names[0:5], indent=1)) 
print (json.dumps(hashtags[0:5], indent=1))
print (json.dumps(words[0:5], indent=1))
"""
"""
from collections import Counter
# Creating a basic frequency distribution from the words in tweets
for item in [words, screen_names, hashtags]:
    c = Counter(item)
    print (c.most_common()[:30]) # top 10
#Using prettytable to display tuples in a nice tabular format
from prettytable import PrettyTable

for label, data in (('Word', words), 
                    ('Screen Name', screen_names), 
                    ('Hashtag', hashtags)):
    pt = PrettyTable(field_names=[label, 'Count']) 
    c = Counter(data)
    [ pt.add_row(kv) for kv in c.most_common()[:30] ]
    pt.align[label], pt.align['Count'] = 'l', 'r' # Set column alignment
    print (pt)
#Calculating lexical diversity for tweets
# A function for computing lexical diversity
def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens) 

# A function for computing the average number of words per tweet
def average_words(statuses):
    total_words = sum([ len(s.split()) for s in statuses ]) 
    return 1.0*total_words/len(statuses)

print (lexical_diversity(words))
print (lexical_diversity(screen_names))
print (lexical_diversity(hashtags))
print (average_words(status_texts))


import json
import pymongo # pip install pymongo

def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    
    # Connects to the MongoDB server running on 
    # localhost:27017 by default
    
    client = pymongo.MongoClient(**mongo_conn_kw)
    
    # Get a reference to a particular database
    
    db = client[mongo_db]
    
    # Reference a particular collection in the database
    
    coll = db[mongo_db_coll]
    
    # Perform a bulk insert and  return the IDs
    
    return coll.insert(data)

def load_from_mongo(mongo_db, mongo_db_coll, return_cursor=True,
                    criteria=None, projection=None, **mongo_conn_kw):
    
    # Optionally, use criteria and projection to limit the data that is 
    # returned as documented in 
    # http://docs.mongodb.org/manual/reference/method/db.collection.find/
    
    # Consider leveraging MongoDB's aggregations framework for more 
    # sophisticated queries.
    
    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]
    
    if criteria is None:
        criteria = {}
    
    if projection is None:
        cursor = coll.find(criteria)
    else:
        cursor = coll.find(criteria, projection)

    # Returning a cursor is recommended for large amounts of data
    
    if return_cursor:
        return cursor
    else:
        return [ item for item in cursor ]

# Sample usage


save_to_mongo(statuses, 'search_results', q)
myCursor = load_from_mongo('search_results',q)
for document in myCursor:
    print(document)
"""
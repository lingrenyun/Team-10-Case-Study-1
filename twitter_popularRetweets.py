import json
from collections import Counter
from prettytable import PrettyTable

with open('tweets.json','r') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        terms_all = [tweet['text']]
        #print(terms_all)
        count_all.update(terms_all)
        #print (word_tokenize(text))
        #do_something_else(tokens)
    print(count_all.most_common(30))
    pt = PrettyTable(count_all.most_common(30))

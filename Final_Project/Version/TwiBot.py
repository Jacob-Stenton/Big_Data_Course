
from twikit import Client
import pandas as pd
import nltk
import re
import nltk.corpus
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import datetime
import time
import random

nltk.download('stopwords')
nltk.download('vader_lexicon')

client = Client('en-US')
# client.login(auth_info_1='Siftr0', password='10@SiftPass')
# client.save_cookies('cookies.json') #run once saved cookies - stops from hitting rate limits
client.load_cookies(path='cookies.json')

def get_current_trends():
    trends = client.get_trends('Trending') #rate limit 20000 every 15m
    trend_list = []
    for trend in trends:
            trend_list.append(trend.name)
    return trend_list

def get_tweets_from_query(query):
    tweets = client.search_tweet(query, 'Top') #rate limit 50 every 15m
    tweet_list = []
    for tweet in tweets:
        _tweet = tweet.text.lower()
        _tweet = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", _tweet) #regex to remove unicode chatacters taken from monkeylearn link above
        _tweet = " ".join([word for word in _tweet.split() if word not in (stopwords.words('english'))]) #removes stopwords
        tweet_list.append(_tweet)
    return tweet_list

sentiment = SentimentIntensityAnalyzer()

def get_avg_sentiment(tweets):
    tweet_sentiment = 0
    length = 0
    for tweet in tweets:
        pol_score = sentiment.polarity_scores(tweet)["compound"] 
        if pol_score > 0.0:
            tweet_sentiment += pol_score
            length += 1
    if length == 0:
        length = 1
    return (tweet_sentiment / length)

current_trends = get_current_trends()
print(f"{len(current_trends)} trends found\n")
trends_tweets = []

for trend in current_trends:
    tweets = get_tweets_from_query(trend)
    time.sleep(random.randint(5,10))
    trends_tweets.append([trend,tweets])
    print(f"{len(tweets)} taken from {trend}")

trend_data = {
    "Trend" : [],
    "Sentiment" : [],
    "Last Seen" : []
}

for trend in trends_tweets:
    trend_data["Trend"].append(trend[0])
    trend_data["Sentiment"].append(get_avg_sentiment(trend[1]))
    trend_data["Last Seen"].append(datetime.datetime.now())
        

trend_words_fdist = []
tweet_string = ''
for trend in trends_tweets:
    for tweet in trend[1]:
        tweet_string += tweet
    tweet_tokens = nltk.word_tokenize(tweet_string)
    fdist = nltk.FreqDist(word for word in tweet_tokens)
    trend_words_fdist.append((trend[0], fdist))
    tweet_string = ''


trend_common_nouns = {
    'Trend': [],
    'Words': []
}
for trend in trend_words_fdist:
    _trend = trend[0]
    _fdist = trend[1]
    common_nouns = []
    for word in nltk.pos_tag(list(_fdist)):
        _word = word[0]
        _tag = word[1]
        if _fdist[_word] > 2: # Word appears more than twice sample tweets
            common_nouns.append(_word)
    trend_common_nouns['Trend'].append(_trend)
    trend_common_nouns['Words'].append(', '.join(common_nouns))

old_trend_nouns = pd.read_csv('Common_Words.csv').to_dict(orient="list")
#update csv
for trend in enumerate(trend_common_nouns['Trend']):
    if trend[1] not in old_trend_nouns['Trend']:
        old_trend_nouns['Trend'].append(trend[1])
        old_trend_nouns['Words'].append(trend_common_nouns['Words'][trend[0]])
    else:
        index = old_trend_nouns['Trend'].index(trend[1])
        words = old_trend_nouns['Words'][index].split(", ")
        _words = trend_common_nouns['Words'][trend[0]].split(", ")
        for word in _words:
            if word not in words:
                old_trend_nouns['Words'][index] += f", {word}"

pd.DataFrame.from_dict(old_trend_nouns).to_csv("Common_Words.csv", index=0,)

grouped_trends = {
    'Trend' : [],
    'Matches' : []
}

for words in enumerate(trend_common_nouns['Words']):
    matches = []
    for _words in enumerate(old_trend_nouns['Words']):
        for word in words[1].split(', '):
            if type(_words[1]) == str:
                if word in _words[1].split(', ') and trend_common_nouns['Trend'][words[0]] != old_trend_nouns['Trend'][_words[0]]:
                    matches.append(old_trend_nouns['Trend'][_words[0]])
                    break
    if len(matches) != 0:
        grouped_trends['Trend'].append(trend_common_nouns['Trend'][words[0]])
        grouped_trends['Matches'].append(', '.join(matches))

#read historical trends
history = pd.read_csv("trends.csv").to_dict(orient="list")


returning_trends = []


#update trends csv file

calc_trend_data = trend_data

for trend in enumerate(history["Trend"]):
    if trend[1] in calc_trend_data["Trend"]: #seen trend before
        new_trend_index = 0
        for _trend in calc_trend_data["Trend"]:
            if _trend == trend[1]:
                break
            else:
                new_trend_index += 1
                
        if history["Last Seen"][trend[0]][:10] != str(calc_trend_data["Last Seen"][new_trend_index].date()):#if not same day
            returning_trends.append((history['Trend'][trend[0]],history["Last Seen"][new_trend_index][:10]))
            history["Last Seen"][trend[0]] = calc_trend_data["Last Seen"][new_trend_index] #overwrite date

        history["Sentiment"][trend[0]] = (history["Sentiment"][trend[0]] + calc_trend_data["Sentiment"][new_trend_index]) / 2 # create better sentiment avg

        calc_trend_data["Trend"].pop(new_trend_index)
        calc_trend_data["Sentiment"].pop(new_trend_index)
        calc_trend_data["Last Seen"].pop(new_trend_index)


for i in range(len(calc_trend_data["Trend"])):
    history["Trend"].append(calc_trend_data["Trend"][i])
    history["Sentiment"].append(calc_trend_data["Sentiment"][i])
    history["Last Seen"].append(calc_trend_data["Last Seen"][i])



#new data to put in trends.csv
new_df = pd.DataFrame.from_dict(history)
new_df.to_csv("trends.csv", index=0,)


date = datetime.datetime.now()


def sentiment_to_words(score):
    score = int(score * 100) 
    string = ''
    if score in range(-5, 5):
        string = 'neutral'
    elif score in range(-20, -5) or score in range(5, 20):
        string += 'slightly'
    elif score in range(-40, -20) or score in range(20, 40):
        string += 'somewhat'
    elif score in range(-60, -40) or score in range(40, 60):
        string += 'mostly'
    elif score in range(-80, -60) or score in range(60, 80):
        string += 'highly'
    elif score in range(-100, -80) or score in range(80, 100):
        string += 'extremely'

    if string != 'neutral':
        if score > 0:
            string += ' positive'
        else:
            string += ' negative'

    return string


#Posting results on twitter
date = datetime.datetime.now()
cycle = int(date.strftime("%H")) # So posts can be made at different times

def post_opposite_trends(): #Top and bottom trend sentiment
    df = pd.DataFrame.from_dict(trend_data)
    top = df.sort_values("Sentiment").tail(1)
    top = pd.DataFrame.to_dict(top, orient="list")
    bottom = df.sort_values("Sentiment").head(1)
    bottom = pd.DataFrame.to_dict(bottom, orient="list")

    template = random.randint(1,3)
    if template == 1:
        tweet = f"A lot of {sentiment_to_words(bottom['Sentiment'][0])} views radiating from the people talking about {bottom['Trend'][0]}. Perhaps the people yapping about {top['Trend'][0]} can chime in?"
    elif template == 2:
        tweet = f"Honestly, the fact everyones views are {sentiment_to_words(top['Sentiment'][0])} about {top['Trend'][0]} is quite interesting if you think about it."
    elif template == 3:
        tweet = f"I did some analysis on {top['Trend'][0]} and {bottom['Trend'][0]}\n\nOn average people are {sentiment_to_words(top['Sentiment'][0])} in their tweets towards {top['Trend'][0]} and {sentiment_to_words(bottom['Sentiment'][0])} towards {bottom['Trend'][0]}"
        
    client.create_tweet(tweet)


#post any trends that have returned

def post_returned_trends():
    tweet = ''
    if len(returning_trends) > 1:
        tweet = f"Hey! I've seen all this before...\n"
        for trend in returning_trends: #trend = ("trend","last seen")
            if len(tweet) < 90:
                tweet += f"{trend[0]} on {trend[1]}\n"
            else:
                break
        tweet += "I suppose they're all important topics."
    elif len(returning_trends) == 1:
        tweet = f"Looks like we're talking about {returning_trends[0][0]} again."

    if tweet != '':
        client.create_tweet(tweet)


def post_all_time_ranks():
    all_bottom = new_df.sort_values("Sentiment").head(3)
    all_bottom = pd.DataFrame.to_dict(all_bottom, orient="list")
    all_top = new_df.sort_values("Sentiment").tail(3)
    all_top = pd.DataFrame.to_dict(all_top, orient="list")

    template = random.randint(1,3)
    if template == 1:
        tweet = f"Isn't it fascinating that {all_top['Trend'][0]}, {all_top['Trend'][1]} and {all_top['Trend'][2]} get the most positve views! I could talk about it all day!"
    elif template == 2:
        tweet = f"It appears {all_bottom['Trend'][0]}, {all_bottom['Trend'][1]} and {all_bottom['Trend'][2]} are the lowest of the low in terms of sentiment. I wonder why?"
    elif template == 3:
        tweet = f"People talk highly of {all_top['Trend'][0]}, {all_top['Trend'][1]} and {all_top['Trend'][2]} but so lowly of {all_bottom['Trend'][0]}, {all_bottom['Trend'][1]} and {all_bottom['Trend'][2]}. Anyone have any thoughts on this?"
        
    client.create_tweet(tweet)

def post_linked_trends():
    index = random.randint(0,len(grouped_trends['Trend'])-1)
    links = grouped_trends['Matches'][index].split(", ")

    template = random.randint(1,3)
    if template == 1:
        tweet = f"For anyone interested in {grouped_trends['Trend'][index]}, you might also be interested in {links[random.randint(0,len(links))-1]}"
    elif template == 2:
        if len(links) != 1:
            tweet = f"0_0\n\n {grouped_trends['Trend'][index] }"
            for trend in enumerate(links):
                if trend[0] == len(links)-1:
                    tweet += f"and {trend[1]} are all connected..."
                else:
                    tweet += f"{trend[1]}, "
        else:
            tweet = f"0_0\n\n{grouped_trends['Trend'][index]} and {links[0]} are connected..."
    elif template == 3:
        tweet = f"Ever think about how {grouped_trends['Trend'][index]} and {links[random.randint(0,len(links))-1]} are linked?"
        
    client.create_tweet(tweet)


# if date.day % 7 == 0 and date.hour == 18:
#     post_all_time_ranks()
#     time.sleep(10)
    
# print(date.hour)
# print(date.hour % 4)
# if date.hour % 4 == 0:
#     if random.randint(1,2) == 2:
#         post_opposite_trends()
#     else:
#         post_linked_trends()

# time.sleep(10)
# post_returned_trends()



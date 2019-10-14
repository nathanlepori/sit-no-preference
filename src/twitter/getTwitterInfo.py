import csv

import tweepy

# defining token keys
access_token = '1174467219629076480-KtAYQaIyf8xI6XiBcNOwdnDxgVIxJZ'
access_token_secret = 'NR4Gh8LdGyLznEQ1Q4D5rXaez4iApUVAJixojxFkC1fNH'
consumer_key = 'j6HqL176aZmPCdcOEzoQgFkOy'
consumer_secret = 'tJ20feJRMfD1S7DakSU6FzUKQC57urOZOw2P29ojGiTTTeUitX'

# Function to extract tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_token, access_token_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 200
    tweets = api.user_timeline(screen_name=username)

    # Empty Array
    tmp = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    for j in tweets_for_csv:
        # Appending tweets to the empty array tmp
        tmp.append(j)

        # Printing the tweets
    print(tmp)


# Driver code
if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("amazonIN")
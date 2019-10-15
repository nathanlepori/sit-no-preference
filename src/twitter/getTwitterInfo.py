import unicodecsv as csv
import tweepy

# Defining token keys
access_token = '1174467219629076480-KtAYQaIyf8xI6XiBcNOwdnDxgVIxJZ'
access_token_secret = 'NR4Gh8LdGyLznEQ1Q4D5rXaez4iApUVAJixojxFkC1fNH'
consumer_key = 'j6HqL176aZmPCdcOEzoQgFkOy'
consumer_secret = 'tJ20feJRMfD1S7DakSU6FzUKQC57urOZOw2P29ojGiTTTeUitX'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Defining file for storing information
output_file_path = 'tweets_information.csv'

with open(output_file_path, 'wb') as output_file:
    csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
    headers = ['Timestamp', 'Tweets', 'Status']
    csv_writer.writerow(headers)

    for tweet in tweepy.Cursor(api.user_timeline, screen_name='realDonaldTrump', tweet_mode='extended').items():
        # Check if the tweet is a retweet or tweet made by the user
        if tweet.full_text.startswith("RT @"):
            csv_writer.writerow([tweet.created_at, tweet.retweeted_status.full_text.encode('UTF-8-sig'), 'RT'])
            # print tweet.created_at, tweet.retweeted_status.full_text.encode('UTF-8-sig'), 'RT'
        else: # Tweet made by user without 'RT @'
            csv_writer.writerow([tweet.created_at, tweet.full_text.encode('UTF-8-sig'), 'Tweet'])
            # print tweet.created_at, tweet.full_text.encode('UTF-8-sig')
csv_writer.close()
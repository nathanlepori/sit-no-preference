import tweepy
from pandas import DataFrame

# Defining token keys
# TODO: allow keys configuration?
_ACCESS_TOKEN = '1174467219629076480-KtAYQaIyf8xI6XiBcNOwdnDxgVIxJZ'
_ACCESS_TOKEN_SECRET = 'NR4Gh8LdGyLznEQ1Q4D5rXaez4iApUVAJixojxFkC1fNH'
_CONSUMER_KEY = 'j6HqL176aZmPCdcOEzoQgFkOy'
_CONSUMER_SECRET = 'tJ20feJRMfD1S7DakSU6FzUKQC57urOZOw2P29ojGiTTTeUitX'

_TIMELINE_COLUMNS = ['text', 'created_at', 'lang', 'is_retweet']


def get_twitter_api():
    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(_CONSUMER_KEY, _CONSUMER_SECRET)
    auth.set_access_token(_ACCESS_TOKEN, _ACCESS_TOKEN_SECRET)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
    return api


def get_twitter_timeline(screen_name: str, include_retweets=True) -> DataFrame:
    api = get_twitter_api()

    timeline = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items():
        # Check if the tweet is a retweet or tweet made by the user
        if include_retweets and hasattr(tweet, 'retweeted_status'):
            timeline.append(
                [tweet.retweeted_status.full_text, tweet.created_at, tweet.retweeted_status.lang, True])
        else:
            timeline.append([tweet.full_text, tweet.created_at, tweet.lang, False])

    df = DataFrame(timeline, columns=_TIMELINE_COLUMNS)
    return df


if __name__ == '__main__':
    timeline = get_twitter_timeline('NathixSsb')
    timeline.to_csv('../../datasets/twitter_timeline_nathan.csv', index=False)

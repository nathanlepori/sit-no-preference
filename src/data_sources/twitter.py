from typing import List

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


api = get_twitter_api()


def get_timeline(screen_name: str, include_retweets=True) -> DataFrame:
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


def get_following(screen_name: str) -> List[str]:
    """
    Returns a list of users' screen names followed by the provided user.
    :param screen_name:
    :return:
    """
    following = []
    for user in tweepy.Cursor(api.friends, screen_name=screen_name).items():
        # Get the screen name from the ID
        following.append(user.screen_name)
    return following


def get_tweets_for_training(screen_names: List[str], include_retweets=True, items_per_user=0) -> List[str]:
    """
    Returns a list of tweet texts from given screen names, suitable for annotation tools.
    :param screen_names:
    :param include_retweets:
    :return:
    """
    tweets: List[str] = []
    for screen_name in screen_names:
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(items_per_user):
            # Check if the tweet is a retweet or tweet made by the user
            if include_retweets and hasattr(tweet, 'retweeted_status'):
                tweets.append(tweet.retweeted_status.full_text)
            else:
                tweets.append(tweet.full_text)
    return tweets


if __name__ == '__main__':
    # screen_name = 'NathixSsb'
    # timeline = get_timeline(screen_name)
    # timeline.to_csv('../../datasets/twitter_timeline_nathan.csv', index=False)
    # print(get_following(screen_name))
    tweets = get_tweets_for_training(['9lives_Salem', 'MVG_Mew2King', 'MVD731'], items_per_user=30)
    open('../../datasets/tweets_for_training_2.txt', 'w', encoding='utf-8').writelines(map(lambda t: f'{t}\n', tweets))

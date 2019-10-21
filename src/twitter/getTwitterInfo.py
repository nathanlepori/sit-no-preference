from datetime import datetime
import pytz

import unicodecsv as csv
import tweepy


# Defining function to convert timezone to Asia/Singapore
def changeTime(something):
    sing = pytz.timezone("Asia/Singapore")
    utc = pytz.timezone("UTC")
    utc_created_at = utc.localize(something)
    sing_created_at = utc_created_at.astimezone(sing)
    return datetime.strftime(sing_created_at, '%d/%m/%Y %H:%M:%S')


# Defining function to retrieve Twitter user information
def retrieveUserInformation(userName):
    try:
        # Defining file for storing user information
        userInformation = 'userInformation.csv'
        # Open file to write twitter user information
        with open(userInformation, 'wb') as userInfoOutput:
            csv_writer = csv.writer(userInfoOutput, quoting=csv.QUOTE_ALL)

            print "\nStarting job at " + str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")) + \
                  "\nGetting user information..."

            # Defining header to store the respective fields
            profileHeader = ['Profile ID', 'Profile User Name', 'Profile Screen Name', 'Profile Description',
                             'Profile Location', 'Profile Description URL', 'Profile Creation', 'Following Count',
                             'Followers Count']
            # Write header to csv file
            csv_writer.writerow(profileHeader)

            # Getting the twitter username and store it into a variable
            user = api.get_user(userName)

            # Get the necessary fields and write to csv file
            csv_writer.writerow([user.id_str, user.screen_name, user.name, user.description, user.location, user.url,
                                 user.created_at, user.friends_count, user.followers_count])
            # Close csv file
            userInfoOutput.close()

            print "Finished writing user information to file at " + \
                  str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S") + '\n')

    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


# Defining function to retrieve tweets information
def retrieveTwitterInformation(userName):
    try:
        # Defining file for storing tweets information
        tweetsInformation = 'tweetsInformation.csv'
        # Open file to write tweets information
        with open(tweetsInformation, 'wb') as tweetsInfoOutput:
            csv_writer = csv.writer(tweetsInfoOutput, quoting=csv.QUOTE_ALL)

            print "Starting job at " + str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")) + \
                  "\nGetting tweets information..."

            # Defining header for the respective fields
            tweetsHeader = ['Timestamp', 'Tweets', 'Retweet Counts', 'Liked Counts', 'Status']
            csv_writer.writerow(tweetsHeader)  # Write header to csv file
            # Get tweets with user specified screen_name
            # Extended is used because twitter only allow retrieving of 280 characters max, the rest will be truncated
            # Extended is used alongside with full_text
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=userName, tweet_mode='extended').items():
                # Check if the tweet is a retweet or tweet made by the user, all retweets will start with 'RT @'
                if tweet.full_text.startswith("RT @"):
                    csv_writer.writerow([changeTime(tweet.created_at),
                                         tweet.retweeted_status.full_text.encode('ascii', 'ignore'),
                                         tweet.retweeted_status.retweet_count,
                                         tweet.retweeted_status.favorite_count, 'RT'])
                else:  # Tweet made by user
                    csv_writer.writerow([changeTime(tweet.created_at), tweet.full_text.encode('ascii', 'ignore'),
                                         tweet.retweet_count, tweet.favorite_count, 'Tweet'])

            # Close csv file
            tweetsInfoOutput.close()
            print "Finished writing tweets information to file at " + \
                  str(datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S"))
    except Exception as ex:
        print 'An error occurred. Please contact the administrator!'


try:
    # Defining token keys
    access_token = '1174467219629076480-KtAYQaIyf8xI6XiBcNOwdnDxgVIxJZ'
    access_token_secret = 'NR4Gh8LdGyLznEQ1Q4D5rXaez4iApUVAJixojxFkC1fNH'
    consumer_key = 'j6HqL176aZmPCdcOEzoQgFkOy'
    consumer_secret = 'tJ20feJRMfD1S7DakSU6FzUKQC57urOZOw2P29ojGiTTTeUitX'

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Creation of the actual interface, using authentication
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Prompt user to key in Twitter username
    userInput = raw_input("Enter Twitter username: ")

    # Calling the functions that take in userInput as arguments
    retrieveUserInformation(userInput)
    retrieveTwitterInformation(userInput)

except Exception as ex:
    print "An error has occurred. Please contact the administrator!"

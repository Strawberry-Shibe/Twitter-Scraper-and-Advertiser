import tweepy
from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler

# import twitter_credentials
from creds import creds

twitter_credentials = creds.twitter


def authenticator():
    auth = OAuthHandler(
        twitter_credentials.CONSUMER_KEY,
        twitter_credentials.CONSUMER_SECRET
        )
    auth.set_access_token(
        twitter_credentials.ACCESS_TOKEN,
        twitter_credentials.ACCESS_TOKEN_SECRET
        )
    api = API(auth)
    return api


def server_authenticator(creds):
    auth = OAuthHandler(
        creds.CONSUMER_KEY,
        creds.CONSUMER_SECRET
        )
    auth.set_access_token(
        creds.ACCESS_TOKEN,
        creds.ACCESS_TOKEN_SECRET
        )
    api = API(auth)

    return api


def get_tweets_server(search, api, since_id):

    # Search for tweets matching the query and append them to tweets
    lang = 'en'
    tweets = []
    try:
        for status in Cursor(api.search, q=search, since_id=since_id, tweet_mode="extended").items(100):
            if (status._json["lang"] == lang) and ("retweeted_status" not in status._json.keys()):
                tweets.append(status._json)
                # id_to_file(status._json['id'])
    except tweepy.error.TweepError:
        print(429)

    if len(tweets) > 0:
        new_last_tweet = tweets[0]['id']
    else:
        new_last_tweet = since_id

    return tweets, new_last_tweet


def get_tweets(search):
    api = authenticator()

    since_id = id_from_file("most_recent_tweet.txt")

    # Search for tweets matching the query and append them to tweets
    lang = 'en'
    tweets = []
    print("test0")
    for status in Cursor(api.search, q=search, since_id=since_id,
                         ).items():
        print("test1")
        if status._json["lang"] == lang:
            tweets.append(status._json)
            if len(tweets) == 10:
                print(tweets[9]["id"])
            # id_to_file(status._json['id'])

    if len(tweets) > 0:
        id_to_file(tweets[0]['id'])
    else:
        id_to_file(since_id)

    return tweets


# Loads the most recent tweet id from text file
def id_from_file(file):
    try:
        with open(file, 'r') as f:
            since_id = f.read()
            if since_id == "" or since_id is None:
                print("An id was not supplied.\nGoing back as far as I can.")
                return 0
            else:
                return int(since_id)
        f.close()
    except FileNotFoundError:
        print(f"The file '{file}' was not found.\nGoing back as far as I can.")
        return 0


# Stores id of the most recent tweet in the text file
def id_to_file(id):
    with open("most_recent_tweet.txt", 'w+') as f:
        f.write(str(id))
    f.close()


# Get n most recent tweets made by the user
def get_recent_tweets(user_id, n, api=authenticator()):
    if n > 20:
        n = 20
    tweets = []
    for status in api.user_timeline(user_id=user_id, count=n):
        tweets.append(status._json)
    return tweets


# Runs if not called from another file
if __name__ == "__main__":
    get_tweets("samsung")
    # print("This is not the main script!")
    #
    # test_terms = ["penis"]
    # print(f"Using test data: {test_terms}")
    # tweets = get_tweets(test_terms)
    #
    # if len(tweets) == 0:
    #     print("No tweets were found.")
    # else:
    #     print(f"""The first tweet, out of {len(tweets)} tweets found,
    #               in the tweet list fetched is:""")
    #     print(tweets[0])

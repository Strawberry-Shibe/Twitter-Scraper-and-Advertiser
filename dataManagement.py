#Imports
#mysql?
#datetime?
#numpy?
#flask?

from textblob import TextBlob
import re
import datetime

import test_tweet

"""
1 : tweets in

2: clean data

3: upload to db

4: download entire db/query it for answers

5: package as list of dicts

6: hand to output team
"""


class User:

    username = ""
    userID = ""
    verified = False
    accountCreationDate = 1/1/2000
    postFrequency = 1  # avergae number of posts per day for 20 recent tweets
    accountWeight = 0  # multiplier for between 0 and 1
    confirmedBot = False
    manager = ""

    def __init__(self, username="", userID="", verified=False, accountCreationDate=1/1/2000,
                    postFrequency=1, accountWeight=0, confirmedBot=False, manager=""):

        self.username = username
        self.userID = userID
        self.verified = verified
        self.accountCreationDate = accountCreationDate
        self.postFrequency = postFrequency
        self.accountWeight = accountWeight
        self.confirmedBot = confirmedBot
        self.manager = manager

    def calculatePostFrequency(self):

        # code that finds num tweets on timeline and calculates postFrequency
        dates = self.manager.userPosts  # some list of the most recent 20 post dates

        try:

            postFrequency = len(dates) / int((max(dates) - min(dates)).days)

            self.postFrequency = postFrequency

        except ZeroDivisionError:

            print("legnth of the dates array: " + len(dates) +
                    " , day difference: " + str((max(dates) - min(dates)).days) +
                    " the latter caused a division by zero error. Operation Ignored.")

    def calculateAccountWeight(self):

        # missing post frequency

        if self.confirmedBot is True:
            self.accountWeight = 0
            return  # could even delete the user from memory instead

        elif self.verified is True:
            self.accountWeight = 1
            return

        elif self.accountCreationDate - self.date.today() >= 30:
            self.accountWeight = 1
            return

        else:
            self.accountWeight = (((2/9 - 0.2) * ((self.accountCreationDate - date.today)**2)) / 20)


class DatasetManager:

    def __init__(self):
        self.postsToWrite = {}
        self.postsRetrieved = {}
        self.userPosts = {}
        self.users = {}
        self.recentOperationResult = ""

    def userTimeline(self, post):
        # takes in a post object

        # depending on platform, do the thing:

        if post.dataDict["platform"] == "twitter":
            posts = []  # post list
            for post in posts:
                self.generateTweet(post, "user")
                self.user[post["user"]["id"]] = self.user(
                        post["user"]["screen_name"],
                        post["user"]["id"], post["user"]["verified"],
                        post["user"]["created_at"], post["user"]["created_at"], 1, 1
                )
            pass

            # call sams func to get tweets from user id with post.dataDict["posterID"]

        if post.dataDict["platform"] == "flickr":
            # posts = []
            pass

            # call joe's func to get flicks from user id with post.dataDict["posterID"]

        return posts  # instantiate posts instead and add to userPosts

    def findPosts(self, sortBy):

        """
        Takes a dict of sort criteria, returns list of posts meeting criteria
        """

        foundPosts = []

        for post in self.postsToWrite:
            postCheck = True
            for criterion in sortBy.keys():
                if post.criterion != sortBy[criterion]:
                    postCheck = False
                    break

            if postCheck is True:
                foundPosts.append(post)

        self.recentOperationResult = foundPosts
        return foundPosts

    def generateTweet(self, tweetList, address):

        tweets = tweetList
        # what if tweets is empty?
        for tweet in tweets:
            # what if coords arent present?

            try:
                coords = tweet["coordinates"]
                long = coords["coordinates"][0]
                lat = coords["coordinates"][1]

            except TypeError as e:
                # work out coordinates from location or just say fail on finding coords
                long = 0
                lat = 0

            # what if any info is missing?
            tweetDateTime = tweet["created_at"]
            datetimeOfTweet = datetime.datetime.strptime(tweetDateTime, "%a %b %d %H:%M:%S %z %Y")

            if address == "write":
                self.postsToWrite["twitter"+str(tweet["id"])] = CleanedData(
                    "twitter", tweet["user"]["id"], tweet["id"], tweet["full_text"], datetimeOfTweet, long, lat, self)
                self.postsToWrite["twitter"+str(tweet["id"])].setSentiment()

            elif address == "retrieve":
                self.postsRetrieved["twitter"+str(tweet["id"])] = self.CleanedData(
                    "twitter", tweet["user"]["id"], tweet["id"], tweet["full_text"], datetimeOfTweet, long, lat, self)
                self.postsRetrieved["twitter"+str(tweet["id"])].setSentiment()

            elif address == "user":
                self.userPosts["twitter"+str(tweet["id"])] = self.CleanedData(
                    "twitter", tweet["user"]["id"], tweet["id"], tweet["text"], datetimeOfTweet, long, lat, self)
                self.userPosts["twitter"+str(tweet["id"])].setSentiment()

            else:
                print("Address for tweet generation not given! Where does this belong? " + "twitter",
                        tweet["user"]["id"], tweet["id"], tweet["text"], datetimeOfTweet, long, lat, self)


    def generateFlick(self):

        flicks = fs.get_flicks()
        for flick in flicks:
            postsToWrite["flickr"+str(postID)] = cleanedData(
                "flickr", flick.user["id"], flick["id"], postContent, postTime, postDate, longitude, latitude, self)


class CleanedData:
    """
    This class will be used to store, clean, analyse data as well as write it to a database.

    This may be subclassed in future for a larger class that does mass management of data
    """
    platform = "n/a"
    posterID = -1
    postID = -1
    postContent = ""
    postDateTime = ""
    longitude = 0
    latitude = 0
    sentiment = 0
    manager = ""

    def __init__(self, platform="n/a", posterID=-1, postID=-1, postContent="",
                    postDateTime="", longitude=None, latitude=None, sentiment=0, manager=""):

        """
        Instanciates a new set of collected data with preset features that can be modified on creation
        """

        self.platform = platform
        self.posterID = posterID
        self.postID = postID
        self.postContent = postContent
        self.postDateTime = postDateTime
        self.longitude = longitude
        self.latitude = latitude
        self.sentiment = sentiment
        self.manager = manager

    def cleanTweet(self, postContent):

        """
        This code removes any reoccuring characters, links and cleans the whole tweet.
        """

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", postContent).split())

    def setSentiment(self):

        """
        This piece of code finds the sentiment of the postContent, saves it as a self var, and returns it
        """

        testimonial = TextBlob(self.postContent)
        self.sentiment = testimonial.sentiment.polarity

    def getAttribute(self):

        """
        Simple getter to get any attr of the dataDict
        """
        return self.postContent


    def getDict(self):

        return {
            # "post_id": self.postID,
            "poster_id": self.posterID,
            "post_content": self.postContent,
            "post_date_time": self.postDateTime,
            "platform": self.platform,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "sentiment": self.sentiment
        }


if __name__ == '__main__':

    manager = DatasetManager()
    tweets = test_tweet.tweets
    manager.generateTweet(tweets, "write")
    for tweet in manager.postsToWrite:
        print(manager.postsToWrite[tweet].getAttribute())

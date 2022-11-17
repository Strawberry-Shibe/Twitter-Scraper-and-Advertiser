import psycopg2
import sqlalchemy
from webapp import scheduler, db, socketio, app, twitter_api
from webapp.helpers import string_rounding, avg
from webapp.models import PersistentStorage as PS, post_collection as posts
import datetime
from twitter_searcher import server_authenticator, get_tweets_server
from dataManagement import DatasetManager
from flask_socketio import join_room, leave_room, send, emit


# scheduler task for running the twitter scraper function based on interval set in database
@scheduler.task('interval', id='twitter_scraper', seconds=int(app.ps_cache["twitter_scrape_interval"]), misfire_grace_time=900)
def twitter_scraper():

	current_datetime = datetime.datetime.utcnow()

	# get current iso timestamp
	timestamp = current_datetime.isoformat()

	# debug statement for job execution time
	print('Job 1 executed - ', current_datetime.strftime("%H:%M:%S"))

	# store current iso timestamp in database and persistent cache
	app.ps_cache["last_tweet_scrape_time"] = timestamp
	PS.query.filter_by(id="last_tweet_scrape_time").first().content = timestamp
	db.session.commit()

	last_tweet_samsung = int(app.ps_cache["last_tweet_samsung"])

	tweets_list, last_tweet_samsung = get_tweets_server("samsung", twitter_api, last_tweet_samsung)

	manager = DatasetManager()
	manager.generateTweet(tweets_list, "write")

	for id, post in manager.postsToWrite.items():
		post_dict = post.getDict()
		try:
			new_tweet = posts(post_id=id, **post_dict, keyword="samsung")
			db.session.add(new_tweet)
			db.session.commit()
		except sqlalchemy.exc.IntegrityError:
			pass
		except psycopg2.errors.UniqueViolation:
			pass
		except sqlalchemy.exc.PendingRollbackError:
			db.session.rollback()

	del manager

	print("samsung done")

	last_tweet_iphone = int(app.ps_cache["last_tweet_iphone"])

	tweets_list, last_tweet_iphone = get_tweets_server("iphone", twitter_api, last_tweet_iphone)

	manager = DatasetManager()
	manager.generateTweet(tweets_list, "write")

	for id, post in manager.postsToWrite.items():
		post_dict = post.getDict()
		try:
			new_tweet = posts(post_id=id, **post_dict, keyword="iphone")
			db.session.add(new_tweet)
			db.session.commit()
		except sqlalchemy.exc.IntegrityError:
			pass
		except psycopg2.errors.UniqueViolation:
			pass
		except sqlalchemy.exc.PendingRollbackError:
			db.session.rollback()

	# db.session.commit()

	del manager

	print("iphone done")

	app.ps_cache["last_tweet_iphone"] = last_tweet_iphone
	PS.query.filter_by(id="last_tweet_iphone").first().content = last_tweet_iphone

	app.ps_cache["last_tweet_samsung"] = last_tweet_samsung
	PS.query.filter_by(id="last_tweet_samsung").first().content = last_tweet_samsung
	db.session.commit()

	# notify dashboard of executed job and update with new info
	# socketio.emit('twitter_scraper_update', {
	# 		"last_time": current_datetime.timestamp(),
	# 		"next_time": current_datetime.timestamp() + int(app.ps_cache["twitter_scrape_interval"]),
	# 		"interval": int(app.ps_cache["twitter_scrape_interval"])
	# 	}, broadcast=True, namespace="/dashboard")

	socketio.emit('data_update', {
			"Twitter": {
				"type": "int",
				"value": string_rounding(len(posts.query.filter_by(platform="twitter").all()))
			},
			"Flickr": {
				"type": "int",
				"value": string_rounding(len(posts.query.filter_by(platform="flickr").all()))
			},
			"Samsung": {
				"type": "scale",
				"value": round(2.5*(avg([value[0] for value in posts.query.with_entities(posts.sentiment).filter_by(keyword="samsung").all()])+1), 2),
				"max": 5
			},
			"iPhone": {
				"type": "scale",
				"value": round(2.5 * (avg([value[0] for value in posts.query.with_entities(posts.sentiment).filter_by(keyword="iphone").all()]) + 1), 2),
				"max": 5
			},
			"tweet_scrape_cd": {
				"type": "countdown",
				"length": int(app.ps_cache["twitter_scrape_interval"]),
				"last": "last_twitter_scrape_timestamp-text"
			}
		}, broadcast=True, namespace="/dashboard")

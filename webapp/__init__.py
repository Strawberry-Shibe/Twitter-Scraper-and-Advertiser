from dotmap import DotMap
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_navigation import Navigation
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
import os
import math as maths
from datetime import datetime, timedelta
import json
from typing import Tuple, Union
import webapp.helpers as olf
from twitter_searcher import server_authenticator
import pandas as pd

app = Flask(__name__)

with open((os.getcwd() + "/webapp/.env").replace("\\", "/"), "r") as file:
	envs = json.load(file)

# set secret key for webserver
app.config['SECRET_KEY'] = envs["flask"]["secret_key"]
# save current working directory as root folder for webapp
app.config['ROOT_FOLDER'] = os.getcwd().replace("\\", "/")
# set database url
app.config['SQLALCHEMY_DATABASE_URI'] = envs["flask"]["db_url"]
# load twitter credentials
app.config['tweet_creds'] = DotMap(envs["twitter"])

app.static_folder = 'static'

# initialise database connection

db = SQLAlchemy(app)

# LEAVE THIS COMMENTED OUT FOR THE LOVE OF GOD, THIS MIGHT OVERWRITE THE ENTIRE DATABASE
# from webapp import models
# db.create_all()

from webapp.models import PersistentStorage as PS

# initialise flask login manager
login_manager = LoginManager()
login_manager.init_app(app)

# api
twitter_api = server_authenticator(app.config["tweet_creds"])

# initialise navigation plugin for navbar
nav = Navigation()
nav.init_app(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)

# initialise socketio plugin
socketio = SocketIO(app)

# load persistent storage values from database into cache
app.ps_cache = olf.load_ps_cache(PS)

# import any circular imports
# TODO check for a cleaner way to import these functions (PEP8)
from webapp import jobs
from webapp import routes

app.data = pd.read_csv(app.config['ROOT_FOLDER'] + "/webapp/static/locations.csv")

# get current iso timestamp
current_datetime = datetime.utcnow()
timestamp = current_datetime.isoformat()

# store current iso timestamp in database and persistent cache
app.ps_cache["last_tweet_scrape_time"] = timestamp
PS.query.filter_by(id="last_tweet_scrape_time").first().content = timestamp
db.session.commit()


# start all scheduled jobs
# scheduler.start()


def polar_to_cartesian(center_x: float, center_y: float, radius: float, angle_in_degrees: float):
	"""
	converts a polar coordinate with center point to a cartesian coordinate

	:authors:
		- Matt
	:param center_x: center coordinate x
	:param center_y: center coordinate y
	:param radius: radius
	:param angle_in_degrees: angle from the polar axis going anti-clockwise, measured in degrees
	:return: dictionary listing the resultant cartesian point
	"""
	angle_in_radians = maths.radians(angle_in_degrees)
	return {
		"x": center_x + (radius * maths.cos(angle_in_radians)),
		"y": center_y + (radius * maths.sin(angle_in_radians))
	}


def describe_arc(x: float, y: float, radius: float, start_angle: float, end_angle: float) -> str:
	"""
	takes a handful of parameters for defining an arc using an svg path element

	:authors:
		- Matt
	:param x: center coordinate x
	:param y: center coordinate y
	:param radius: radius of the arc
	:param start_angle: starting angle of the arc in degrees
	:param end_angle: ending angle of the arc in degrees
	:return: the path d string described by the input parameters
	"""
	start = polar_to_cartesian(x, y, radius, end_angle)
	end = polar_to_cartesian(x, y, radius, start_angle)

	large_arc_flag = str(int((end_angle - start_angle >= 180)))
	sweep_flag = str(int((end_angle - start_angle >= 360)))

	return " ".join(
		["M", str(start["x"]), str(start["y"]), "A", str(radius), str(radius), "0", large_arc_flag, sweep_flag,
		 str(end["x"]), str(end["y"])])


def font_size_calc(value: dict) -> Tuple[str, int]:
	"""
	calculates the font size based on length of input.

	:authors:
		- Matt
	:param value: str or int
	:returns: Tuple: fontsize percentage (str), number of digits (int)
	"""
	# get number of characters in the provided string or integer
	values = [str(x[0]) for x in value.values()]
	digits = len(max(values, key=len))

	# old approximation:
	# decimal = 1.24194 - 0.231619*maths.log((15.2666*digits)-6.20299)

	# new approximation:
	decimal = 0.04889127 + 0.42963403 / (1 + (digits / 3.496243) ** 3.158169) ** 0.518323

	# conversion from decimal to truncated percentage
	percentage = "{:.2%}".format(decimal)
	return percentage, digits


def svg(filename):
	"""
	function for loading basic svg icons as paths in html template
	without needing an extra http request

	:authors:
		- Matt
	:param filename: string
	:return: string containing html path element
	"""
	try:
		path = {
			"home.svg": '<path d="M4 0l-4 3h1v4h2v-2h2v2h2v-4.03l1 .03-4-3z" />',
			"logout.svg": '<path d="M3 0v1h4v5h-4v1h5v-7h-5zm-1 2l-2 1.5 2 1.5v-1h4v-1h-4v-1z" />',
			"double-chevrons.svg": '<path d="M 1 1 l 6.5 7 l -6.5 7" class="dc"/> \n\t <path d="M 7 1 l 6.5 7 l -6.5 7" class="dc"/>',
			"map.svg": '<path d="M0 0v8h8v-2.38a.5.5 0 0 0 0-.22v-5.41h-8zm1 1h6v4h-1.5a.5.5 0 0 0-.09 0 .5.5 0 1 0 .09 1h1.5v1h-6v-6zm2.5 1c-.83 0-1.5.67-1.5 1.5 0 1 1.5 2.5 1.5 2.5s1.5-1.5 1.5-2.5c0-.83-.67-1.5-1.5-1.5zm0 1c.28 0 .5.22.5.5s-.22.5-.5.5-.5-.22-.5-.5.22-.5.5-.5z"/>',
			"globe.svg": '<path d="M4 0c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 1c.33 0 .64.09.94.19-.21.2-.45.38-.41.56.04.18.69.13.69.5 0 .27-.42.35-.13.66.35.35-.64.98-.66 1.44-.03.83.84.97 1.53.97.42 0 .53.2.5.44-.54.77-1.46 1.25-2.47 1.25-.38 0-.73-.09-1.06-.22.22-.44-.28-1.31-.75-1.59-.23-.23-.72-.14-1-.25-.09-.27-.18-.54-.19-.84.03-.05.08-.09.16-.09.19 0 .45.38.59.34.18-.04-.74-1.31-.31-1.56.2-.12.6.39.47-.16-.12-.51.36-.28.66-.41.26-.11.45-.41.13-.59-.06-.03-.13-.1-.22-.19.45-.27.97-.44 1.53-.44zm2.31 1.09c.18.22.32.46.44.72 0 .01 0 .02 0 .03-.04.07-.11.11-.22.22-.28.28-.32-.21-.44-.31-.13-.12-.6.02-.66-.13-.07-.18.5-.42.88-.53z"/>',
			"graph.svg": '<path d="M.97 0l3.03 3 1-1 3 3.03-1 1-2-2.03-1 1-4-4 .97-1zm7.03 7v1h-8v-1h8z"/>'
		}[filename]
	except KeyError:
		path = '<path d="M4 0l-4 3h1v4h2v-2h2v2h2v-4.03l1 .03-4-3z" />'
	return path


def format_td(td: timedelta) -> str:
	"""
	function to deal with the horrendous lack of support for any
	nice string formatting of the the timedelta object.
	outputs in HH:MM:SS format unless HH is 00 in which case, outputs MM:SS format

	:authors:
		- Matt
	:param td: timedelta object from datetime module
	:return: str: formatting string consisting of hours, minutes and seconds
	"""
	# function for formatting a timedelta as hours (only if required), minutes and seconds
	output = ""
	if td.seconds // 3600:
		output += "{:02d}:".format(td.seconds // 3600)
	output += "{:02d}:{:02d}".format((td.seconds // 60) % 60, td.seconds % 60)
	return output


def dt_diff(ts1: float, ts2: float) -> str:
	"""
	function for calculating the difference in time between 2 unix timestamps and formatting the output

	:authors:
		- Matt
	:param ts1: posix timestamp as float
	:param ts2: posix timestamp as float
	:return: string
	"""

	dt1 = datetime.fromtimestamp(ts1)
	dt2 = datetime.fromtimestamp(ts2)
	diff = dt1 - dt2
	output = format_td(diff)
	return output


# function call to pass some functions into the jinja template engine
app.jinja_env.globals.update(describeArc=describe_arc, len=len, font_size_lookup=font_size_calc, svg=svg,
								dt=datetime, dt_diff=dt_diff)

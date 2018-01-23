#Author: Morgan Simmons
#Description: This is a twitter bot designed to follow, like, and retweet to automatically enter
#twitter "giveaways". I made this to familiarize myself with the Tweepy twitter api, and for fun.
#I may augment this or build a companion bot to collect data to visualize after some time.

# -*- coding: utf-8 -*-
import time, sys, tweepy, random, logging
from subprocess import call

#Twitter bot oauth information
#----------------------------------------------------------------------
#
consumer_key = 'consumerkeygoeshere'
consumer_secret = 'consumersecretgoeshere'
access_key = 'accesskeygoeshere'
access_secret = 'accesssecretgoeshere'
#
#----------------------------------------------------------------------

#logging configuration
#----------------------------------------------------------------------
#
logging.basicConfig(level=logging.DEBUG, filename = "tblogfile", filemode = "a+",
					format = "%(asctime)-15s %(levelname)-8s %(message)s")
#
#----------------------------------------------------------------------


#oauth dance
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

#create api object
api = tweepy.API(auth)


query_list = ['retweet giveaway', 'retweet sweepstakes', 'retweet raffle', 'RT giveaway', 'RT sweepstakes', 'RT raffle']
max_tweets = 45 #maximum number of follows = 20/hour = 480 follows per day
	

bot_active = True
while bot_active == True:
	#search 20 tweets for the phrase "retweet giveaway"
	#i found this block on stackoverflow --  interestingly tweepy does not list api.search in its api reference
	searched_tweets = []
	last_id = -1
	query = random.choice(query_list)
	logging.info("search criteria: " + query)
	while len(searched_tweets) < max_tweets:
		count = max_tweets - len(searched_tweets)
		try:
			new_tweets = api.search(q=query, count = count, max_id = str(last_id - 1))#search
			if not new_tweets:
				break
			searched_tweets.extend(new_tweets)
			last_id = new_tweets[-1].id
		except tweepy.TweepError as e:
			break

	#retweet the giveaway tweets
	try:
		for i in searched_tweets:
			if i.retweeted == False and hasattr(i, 'retweeted_status') == False: #making sure the bot has not already retweeted and the tweet in question is the original, not a retweet
				if ('follow' in i.text or 'FOLLOW' in i.text or 'Follow' in i.text) and i.user.following == False: #if the tweets contain these extra steps, do them
					api.create_friendship(i.user.id_str)
					logging.info("followed " + i.user.screen_name)
				if ('like' in i.text or 'LIKE' in i.text or 'Like' in i.text or 'Fav' in i.text or 'FAV' in i.text or 'fav' in i.text) and i.favorited == False: #if the tweets contain these extra steps, do them
					api.create_favorite(i.id)
					logging.info("favorited tweet by " + i.user.screen_name)
				api.retweet(i.id)
				logging.info("retweeted tweet by " + i.user.screen_name)

		#clean up follower list to stay under follow limit
		#follower limit is 5000 for twitter accounts that have fewer than 100 followers
		#don't expect this bot to get any followers, so rate must keep follower count below 5000
		follower_count = len(api.friends_ids(api.me().id))
		if follower_count >= 4500:
			for i in range(1000):
				api.destroy_friendship(api.friends_ids(api.me().id)[-1].id) #if follower count ever gets above 4500, unfollow the oldest 1000
				#cannot unfollow all of them because giveaways have variable durations -- need to catch the sweetspot
	except tweepy.TweepError as e:
		logging.warning("Error occured interacting with tweet by " + i.user.screen_name)
		logging.warning(e)

	#go to sleep for an hour
	logging.info("Finished searching. Going to sleep for 1 hour.")
	time.sleep(3600)
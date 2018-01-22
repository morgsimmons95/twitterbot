# twitterbot
### You can find my twitterbot at @webbybo
## Description
This is a very simple twitter bot that searches twitter for a giveaway query (default is "retweet giveaway"). Once it finds a tweet containing these words, it checks if it must favorite and/or follow in order to enter the contest. If necessary, it does those things before retweeting. **The bot is very simple so it does not distinguish parameters like "tag your friends" or "follow this link to enter the giveaway".** I made this bot to familiarize myself with the tweepy api. S/o to tweepy!

## Complying with Twitter's ToS
Twitter requires that accounts with fewer than 100 followers cannot follow more than 5000 other accounts. To get around this, the bot deletes its oldest 1000 followers when it has 4500 or more followers. This generally allows for each contest to have 10 days to run before being removed from the bot's follow list. 

Twitter also has a limit for the number of api requests that an application can make in an hour. **As far as I know,** this number is 100 requests per hour. The bot satisfies this by making only up to 80 requests per hour (1 request for search, 1 for retweet, 1 for favorite, 1 for follow -- across 20 tweets per hour makes 80 max requests).

## Planned Features
I'd like to build a companion bot for this one that collects data about the giveaways and performs statistical analysis (e.g. what percentage of entered contests does an instance of the twitterbot win). I'd also like to improve the bot's comprehension of giveaway tweet parameters.

## Instructions
If you'd like to run a twitter bot, you first must obtain twitter application credentials. Go to http://apps.twitter.com and create a new app. Fill in all of the necessary fields and generate your consumer key, consumer secret key, access key, and access secret. Just plug these into the twitter bot's parameters and run it. 

## Notes
There is a line in the code that prints the user name of tweets that generate exceptions for the bot -- I left this in for troubleshooting as the tweepy api is very sensitive.

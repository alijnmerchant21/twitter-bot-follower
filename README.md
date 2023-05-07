# Twitter-Bot-Follower

A twitter bot to facilitate followers and following

## How to use bot for your account

**If you'd like to use this bot to run your own Twitter Bot, follow these steps:**

1. Clone this repository to your local machine.
2. Create a Twitter developer account and obtain API keys and access tokens. You can do this by following the instructions in Twitter's [developer documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api)
3. Create a config.ini file and add your credentials to it.

```bash
[twitter]
consumer_key = xxxxxxxxxxxxxxxxxxxx
consumer_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
access_token = xxxxxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxx
access_secret = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

4. You can simply run the bot through your local computer. If you are feeling brave, you can run it through services like - Digital Occean, AnywherePython, etc.

## Flow

1. Follow people based on certain keywords in bio.
2. Repeat process for 15 mins.
3. Sleep for 1 hour.
4. Repeat.

## To do

- [ ] Create content calendar
- [ ] Auto schedule and tweet

### Engagement

- [ ] Like tweet with certain keyword
- [ ] Retweet tweet with certain keyword
- [ ] Comment tweet with certain keyword

## Process to create your own bot

1. Create a Twitter developer account and obtain API keys and access tokens. You can do this by following the instructions in Twitter's [developer documentation](https://developer.twitter.com/en/docs/twitter-api/getting-started/about-twitter-api)

2. Once you have your API keys and access tokens, you can use the Tweepy library to interact with Twitter's API in Python. You can install Tweepy by running `pip install tweepy` in your terminal.

3. Create a new Python file called bot.py and import the necessary libraries.

4. Load your API keys and access tokens from the config.ini file. You can use the configparser library to do this.

5. Use the Tweepy library to authenticate your Twitter API credentials.

6. Define a list of keywords to search for and a list of users to follow.

7. Set up a loop to run for 48 hours, following users based on the specified keywords.

8. Run the script by calling python bot.py in your terminal.

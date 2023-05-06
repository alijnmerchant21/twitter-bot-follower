import tweepy
import time
import configparser

# Load the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Authenticate with the Twitter API
auth = tweepy.OAuthHandler(config['twitter']['consumer_key'], config['twitter']['consumer_secret'])
auth.set_access_token(config['twitter']['access_token'], config['twitter']['access_secret'])
api = tweepy.API(auth)

# Define the keywords to search for in a user's bio
keywords = ['web3', 'blockchain']

# Define the amount of time to sleep between runs
sleep_time = 60 * 60  # 1 hour

# Define the file to store the people we follow
followers_file = 'followers.txt'

# Define the time to wait before unfollowing a user (48 hours)
unfollow_time = 48 * 60 * 60

# Load the list of people we're already following
with open(followers_file, 'r') as f:
    followers = set(line.strip() for line in f)

# Define a function to check if a user matches our criteria
def should_follow(user):
    print("Bot in should follow")
    if user.friends_count < 100:
        return False
    for keyword in keywords:
        if keyword in user.description.lower():
            return True
    return False

# Define a function to follow a user
def follow_user(user, follow_count):
    if follow_count >= 400:
        print("Bot has reached the daily follow limit.")
        return
    print("Bot in follow user")
    api.create_friendship(user_id=user.id)
    followers.add(str(user.id))
    with open(followers_file, 'a') as f:
        f.write(str(user.id) + '\n')
    follow_count += 1
    return follow_count


# Define the amount of time to run the bot
bot_runtime = 15 * 60  # 15 minutes

# Keep track of the start time of the bot
start_time = time.time()

# Define the follow count and the last reset time
follow_count = 0
last_reset_time = start_time

# Run the bot for 15 minutes when it starts
while time.time() - start_time < bot_runtime:
    elapsed_time = time.time() - start_time
    print(f"Bot is running for {elapsed_time} seconds.")
    # Follow users based on our criteria
    for user in tweepy.Cursor(api.search_users, q=' '.join(keywords)).items():
        if should_follow(user) and str(user.id) not in followers:
            follow_count = follow_user(user, follow_count)
            if time.time() - last_reset_time > 24 * 60 * 60:
                # Reset the follow count and last reset time
                follow_count = 0
                last_reset_time = time.time()

    # Unfollow users we followed more than 'unfollow_time' ago
    current_time = time.time()
    with open(followers_file, 'r') as f:
        for line in f:
            user_id = line.strip()
            user = api.get_user(user_id)
            if current_time - user.created_at.timestamp() > unfollow_time:
                api.destroy_friendship(user_id)
                followers.remove(user_id)
                with open(followers_file, 'w') as f:
                    f.write('\n'.join(followers))

    # Sleep for a specified amount of time before running the bot again
    print("Bot is sleeping")
    time.sleep(sleep_time)


# Run the bot indefinitely
while True:
    elapsed_time = time.time() - start_time
    print(f"Bot is running for {elapsed_time} seconds.")
    # Follow users based on our criteria
    for user in tweepy.Cursor(api.search_users, q=' '.join(keywords)).items():
        if should_follow(user) and str(user.id) not in followers:
            follow_user(user)

    # Unfollow users we followed more than 'unfollow_time' ago
    current_time = time.time()
    with open(followers_file, 'r') as f:
        for line in f:
            user_id = line.strip()
            user = api.get_user(user_id)
            if current_time - user.created_at.timestamp() > unfollow_time:
                api.destroy_friendship(user_id)
                followers.remove(user_id)
                with open(followers_file, 'w') as f:
                    f.write('\n'.join(followers))

    # Sleep for a specified amount of time before running the bot again
    print("Bot is sleeping")
    time.sleep(sleep_time)


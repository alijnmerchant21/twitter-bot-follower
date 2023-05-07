import tweepy
import datetime
import time
import csv
import configparser

# Load the API keys and access tokens from the config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

consumer_key = config.get("twitter", "consumer_key")
consumer_secret = config.get("twitter", "consumer_secret")
access_token = config.get("twitter", "access_token")
access_secret = config.get("twitter", "access_secret")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# Create API object
api = tweepy.API(auth)

# Set the minimum number of followers required to follow an account
MIN_FOLLOWERS = 100

# Set the keywords to search for in the user's bio
KEYWORDS = ["blockchain", "web3"]

# Set the number of accounts to follow in a day
MAX_FOLLOW_PER_DAY = 400
FOLLOW_PER_HOUR = 15

# Set the number of hours after which to unfollow an account
UNFOLLOW_AFTER_HOURS = 36

# Set the name of the CSV file
CSV_FILE_NAME = "followed_accounts.csv"

# Get the current date
today = datetime.datetime.now().strftime("%Y-%m-%d")

# Check if the CSV file exists, and create it if it doesn't
try:
    with open(CSV_FILE_NAME, "x", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["id", "display_name", "followed_at"])
except FileExistsError:
    pass

# Load the list of followed accounts from the CSV file
followed_accounts = []
with open(CSV_FILE_NAME, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header row
    for row in csvreader:
        followed_accounts.append({
            "id": row[0],
            "display_name": row[1],
            "followed_at": datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        })

# Follow new accounts
follow_count = 0
for follower_id in tweepy.Cursor(api.get_follower_ids).items():
    try:
        # Check if the follower has a minimum number of followers
        user = api.get_user(user_id=follower_id)
        if user.followers_count < MIN_FOLLOWERS:
            continue

        # Check if the follower has already been followed
        if any(account["id"] == str(user.id) for account in followed_accounts):
            continue

        # Check if the user's bio contains any of the keywords
        if not any(keyword in user.description.lower() for keyword in KEYWORDS):
            continue

        # Follow the user
        api.create_friendship(user_id=user.id)
        followed_accounts.append({
            "id": str(user.id),
            "display_name": user.name,
            "followed_at": datetime.datetime.now()
        })
        follow_count += 1
        print(f"Followed user {user.id}")

        # Save the newly followed account to the CSV file
        with open(CSV_FILE_NAME, "a", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([str(user.id), user.name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        # Check if the daily follow limit has been reached
        if follow_count >= MAX_FOLLOW_PER_DAY:
            break

         # Check if the hourly follow limit has been reached
        if follow_count % FOLLOW_PER_HOUR == 0:
            print("Hourly follow limit reached, bot is going to sleep.")
            time.sleep(3600)  # Sleep for 1 hour

    except tweepy.errors.NotFound:
        print(f"User with ID {follower_id} not found.")

    # Check if the daily follow limit has been reached
    if follow_count >= MAX_FOLLOW_PER_DAY:
        break

# Save the updated list of followed accounts to the CSV file
with open(CSV_FILE_NAME, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["id", "display_name", "followed_at"])
    for account in followed_accounts:
        csvwriter.writerow([account["id"], account["display_name"], account["followed_at"].strftime("%Y-%m-%d %H:%M:%S")])

# Check if the daily follow limit was reached
if follow_count >= MAX_FOLLOW_PER_DAY:
    print("Daily follow limit reached, bot is going to sleep.")
    time.sleep(3600)  # Sleep for 1 hour
else:
    # Followed less than the daily limit, wait for 1 hour before following more accounts
    print(f"Followed {follow_count} accounts today, waiting for 1 hour before following more.")
    time.sleep(3600)

# Unfollow accounts that were followed more than UNFOLLOW_AFTER_HOURS ago
accounts_to_remove = []
for account in followed_accounts:
    if (datetime.datetime.now() - account["followed_at"]).total_seconds() >= UNFOLLOW_AFTER_HOURS * 3600:
        api.destroy_friendship(account["id"])
        accounts_to_remove.append(account)
        print(f"Unfollowed user {account['id']}")

# Remove the unfollowed accounts from the list of followed accounts
for account in accounts_to_remove:
    followed_accounts.remove(account)

# Save the updated list of followed accounts to the CSV file
with open(CSV_FILE_NAME, "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["id", "display_name", "followed_at"])
    for account in followed_accounts:
        csvwriter.writerow([account["id"], account["display_name"], account["followed_at"].strftime("%Y-%m-%d %H:%M:%S")])
        
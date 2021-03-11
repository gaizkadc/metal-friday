import utils
import twitter_utils
import media_utils
import datetime

# create a logger
logger = utils.get_logger()
logger.info('metal-friday started')

# today
now = datetime.datetime.now()  # + datetime.timedelta(days=1)
today = now.strftime("%Y%m%d")

output_folder_path = utils.create_mf_output_folder(logger, today)
tweet_text = twitter_utils.create_tweet_text(logger)

# Create title image
mf_video_path = media_utils.create_mf_video(logger, output_folder_path, today)

# Tweet
consumer_key, consumer_secret, access_token, access_token_secret = twitter_utils.get_twitter_credentials(logger)
api = twitter_utils.get_twitter_api(logger, consumer_key, consumer_secret, access_token, access_token_secret)
twitter_utils.tweet(logger, api, mf_video_path, tweet_text)

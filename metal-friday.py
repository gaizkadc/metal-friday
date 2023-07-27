import utils
import twitter_utils
import instagram_utils
import media_utils
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

import tweepy

# create a logger
logger = utils.get_logger()
logger.info(os.getenv('APP_NAME') + ' started')

# today
now = datetime.datetime.now()  # + datetime.timedelta(days=1)
today = now.strftime("%Y%m%d")

output_folder_path = utils.create_mf_output_folder(logger, today)
caption = twitter_utils.create_tweet_text(logger)

# Create title image
# mf_video_path = media_utils.create_mf_video(logger, output_folder_path, today)

# Tweet
if os.getenv('TWITTER_POST') == '1':
    # credentials, client = twitter_utils.get_twitter_credentials_and_client(logger)
    # api = twitter_utils.get_twitter_api(logger, credentials)
    # twitter_utils.tweet(logger, api, client, mf_video_path, caption)
    client = twitter_utils.get_twitter_client(logger)
    twitter_utils.tweet_text(logger, client, caption)

# Instagram
# if os.getenv('INSTAGRAM_POST') == '1':
#     instagram_utils.instagram_collage(logger, mf_video_path, caption)

# done
logger.info('done ✅')
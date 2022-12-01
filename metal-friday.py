import tumblr_utils
import utils
import twitter_utils
import instagram_utils
import media_utils
import datetime
import os

from dotenv import load_dotenv
load_dotenv()

# create a logger
logger = utils.get_logger()
logger.info('metal-friday started')

# today
now = datetime.datetime.now()  # + datetime.timedelta(days=1)
today = now.strftime("%Y%m%d")

output_folder_path = utils.create_mf_output_folder(logger, today)
caption = twitter_utils.create_tweet_text(logger)
tumblr_tags = utils.create_tumblr_tags(logger)

# Create title image
mf_video_path = media_utils.create_mf_video(logger, output_folder_path, today)

# Tweet
if os.getenv('TWITTER_POST') == '1':
    credentials = twitter_utils.get_twitter_credentials(logger)
    api = twitter_utils.get_twitter_api(logger, credentials)
    twitter_utils.tweet(logger, api, mf_video_path, caption)

# Instagram
if os.getenv('INSTAGRAM_POST') == '1':
    instagram_utils.instagram_collage(logger, mf_video_path, caption)

# post video to tumblr
if os.getenv('TUMBLR_POST') == '1':
    tumblr_utils.tumblr_video(logger, mf_video_path, caption, tumblr_tags)

# done
logger.info('done ✅')

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

logger.debug(tweet_text)

# Create title image
media_utils.create_mf_video(logger, output_folder_path, today)
import os
import pytumblr


def get_tumblr_credentials(logger):
    logger.info('getting tumblr credentials')

    consumer_key = os.getenv('TUMBLR_CONSUMER_KEY')
    consumer_secret = os.getenv('TUMBLR_CONSUMER_SECRET')
    oauth_token = os.getenv('TUMBLR_OAUTH_TOKEN')
    oauth_secret = os.getenv('TUMBLR_OAUTH_SECRET')

    credentials = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': oauth_token,
        'oauth_secret': oauth_secret
    }

    logger.info('twitter credentials retrieved')

    return credentials


def tumblr_login(logger, credentials):
    logger.info('logging in tumblr')

    client = pytumblr.TumblrRestClient(
        credentials['consumer_key'],
        credentials['consumer_secret'],
        credentials['oauth_token'],
        credentials['oauth_secret'],
    )

    client.info()

    return client


def tumblr_video(logger, video_path, caption, tags):
    logger.info('posting collage to tumblr')

    credentials = get_tumblr_credentials(logger)
    client = tumblr_login(logger, credentials)

    tags.append('metal collector')
    tags.append('metal')

    client.create_photo("fohoma", tags=tags, state="published", caption=caption, data=video_path)

    logger.info('collage posted to tumblr')

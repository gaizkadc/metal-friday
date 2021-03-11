import os
import datetime

import twitter

import settings


def get_twitter_credentials(logger):
    try:
        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        access_token = settings.ACCESS_TOKEN
        access_token_secret = settings.ACCESS_TOKEN_SECRET

    except ImportError as error:
        logger.info(error)
        logger.info('settings module not found, retrieving env variables')
        consumer_key = os.getenv('CONSUMER_KEY')
        consumer_secret = os.getenv('CONSUMER_SECRET')
        access_token = os.getenv('ACCESS_TOKEN')
        access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    return consumer_key, consumer_secret, access_token, access_token_secret


def get_twitter_api(consumer_key, consumer_secret, access_token, access_token_secret, logger):
    logger.info('getting twitter api')
    return twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, access_token_secret=access_token_secret, sleep_on_rate_limit=True)


def create_tweet_text(logger):
    logger.info('creating tweet text')
    tweet_text = 'Hostia puta, #ViernesdeMetal:\n'

    now = datetime.datetime.now() # + datetime.timedelta(days=1)
    today = now.strftime("%Y%m%d")

    try:
        input_folder_path = settings.INPUT_FOLDER_PATH
    except ImportError as error:
        logger.info(error)
        logger.info('settings module not found, retrieving env variables')
        input_folder_path = os.getenv('INPUT_FOLDER_PATH')

    with open(input_folder_path + '/' + today + '/' + today + '.list') as album_list_file:
        mf_lines = album_list_file.readlines()

    mf_items = []

    for mf_line in mf_lines:
        twitter_user, artist, album = mf_line.split('|')
        if twitter_user.strip() != '':
            mf_twitter_user = '@' + twitter_user.strip()
        else:
            mf_twitter_user = ''
        mf_artist = artist.replace(' ', '').replace('&', 'and')
        mf_album = album.replace('\n', '').strip()
        mf_item = {
            'twitter_user': mf_twitter_user,
            'artist': mf_artist,
            'album': mf_album
        }
        mf_items.append(mf_item)

    i = 0
    while len(tweet_text) < 280 and i < len(mf_items):
        if mf_items[i]['twitter_user'] != '':
            tweet_text += mf_items[i]['twitter_user'] + ' | ' + mf_items[i]['album'] + '\n'
        else:
            tweet_text += '#' + mf_items[i]['artist'] + ' | ' + mf_items[i]['album'] + '\n'
        i += 1
        
    logger.info('tweet text created')

    return tweet_text, mf_items

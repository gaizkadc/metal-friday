import os
import datetime
import random
import time

import twitter


def get_twitter_credentials(logger):
    logger.info('getting twitter credentials')

    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    credentials = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret
    }

    logger.info('twitter credentials retrieved')

    return credentials


def get_twitter_api(logger, credentials):
    logger.info('getting twitter api')

    return twitter.Api(consumer_key=credentials['consumer_key'], consumer_secret=credentials['consumer_secret'], access_token_key=credentials['access_token'], access_token_secret=credentials['access_token_secret'], sleep_on_rate_limit=True)


def create_tweet_text(logger):
    logger.info('creating tweet text')
    
    adornment_noun_list = ['Hostia ', 'Mierda ']
    adornment_adjective_list = ['jodida', 'puta']
    tweet_text = random.choice(adornment_noun_list) + random.choice(adornment_adjective_list) + ', #ViernesdeMetal:\n'

    now = datetime.datetime.now() # + datetime.timedelta(days=1)
    today = now.strftime("%Y%m%d")

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
        mf_artist = artist.replace(' ', '').replace('&', 'and').replace("'", "")
        mf_album = album.replace('\n', '').strip()
        mf_item = {
            'twitter_user': mf_twitter_user,
            'artist': mf_artist,
            'album': mf_album
        }
        mf_items.append(mf_item)

    tweet_text = check_tweet_text_length(logger, mf_items, tweet_text)
    logger.info('tweet text created')

    return tweet_text


def check_tweet_text_length(logger, mf_items, tweet_text):
    logger.info('checking tweet length')
    for mf_item in mf_items:
        if mf_item['twitter_user'] != '':
            almost_tweet_text = tweet_text + mf_item['twitter_user'] + ' | ' + mf_item['album'] + '\n'
        else:
            almost_tweet_text = tweet_text + '#' + mf_item['artist'] + ' | ' + mf_item['album'] + '\n'

        if len(almost_tweet_text) > 280 and len(tweet_text) < (280 - len('Y más.')):
            tweet_text += 'Y más.'
            break
        if len(almost_tweet_text) > 280 and len(tweet_text) >= (280 - len('Y más.')):
            tweet_text = almost_tweet_text
            break
        else:
            tweet_text = almost_tweet_text

    logger.info('tweet text:\n' + tweet_text)
    return tweet_text


def tweet(logger, api, video_path, tweet_text):
    logger.info('tweeting mf video')
    mf_video_id = api.UploadMediaChunked(video_path)
    time.sleep(20)
    api.PostUpdate(status=tweet_text, media=mf_video_id)

    logger.info('mf video tweeted')

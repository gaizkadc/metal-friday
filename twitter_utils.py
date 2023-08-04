import os
import datetime
import random
import time

# import twitter
import tweepy


# def get_twitter_credentials_and_client(logger):
#     logger.info('getting twitter credentials')
#
#     consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
#     consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
#     access_token = os.getenv('TWITTER_ACCESS_TOKEN')
#     access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
#
#     credentials = {
#         'consumer_key': consumer_key,
#         'consumer_secret': consumer_secret,
#         'access_token': access_token,
#         'access_token_secret': access_token_secret
#     }
#
#     logger.info('twitter credentials retrieved')
#
#     client = tweepy.Client(
#         consumer_key=consumer_key, consumer_secret=consumer_secret,
#         access_token=access_token, access_token_secret=access_token_secret
#     )
#
#     logger.info('twitter client retrieved')
#
#     return credentials, client


def get_twitter_client(logger):
    logger.info('getting twitter client')
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    logger.info('twitter client retrieved')

    return client


def create_tweet_text(logger):
    logger.info('creating tweet text')

    adornment_noun_list = ['Hostia ', 'Mierda ']
    adornment_adjective_list = ['jodida', 'puta']
    caption = random.choice(adornment_noun_list) + random.choice(adornment_adjective_list) + ', #ViernesdeMetal:\n'

    now = datetime.datetime.now()  # + datetime.timedelta(days=1)
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
        mf_artist = artist.replace(" ", "").replace('&', 'and').replace("'", "").replace(",", "")
        mf_album = album.replace('\n', '').strip()
        mf_item = {
            'twitter_user': mf_twitter_user,
            'artist': mf_artist,
            'album': mf_album
        }
        mf_items.append(mf_item)

    caption = check_tweet_text_length(logger, mf_items, caption)
    logger.info('tweet text created')

    return caption


def check_tweet_text_length(logger, mf_items, caption):
    logger.info('checking tweet length')
    for mf_item in mf_items:
        if mf_item['twitter_user'] != '':
            almost_tweet_text = caption + mf_item['twitter_user'] + ' | ' + mf_item['album'] + '\n'
        else:
            almost_tweet_text = caption + '#' + mf_item['artist'] + ' | ' + mf_item['album'] + '\n'

        if len(almost_tweet_text) >= 280 and len(caption) <= (280 - len('Y más.')):
            caption += 'Y más.'
            break
        if len(almost_tweet_text) >= 280 and len(caption) >= (280 - len('Y más.')):
            break
        else:
            caption = almost_tweet_text

    logger.info('tweet text:\n' + caption)
    logger.info('tweet length: ' + str(len(caption)))
    return caption


def tweet(logger, api, client, video_path, caption):
    logger.info('tweeting mf video')
    mf_video_id = api.UploadMediaChunked(video_path)
    time.sleep(20)

    response = client.create_tweet(
        text=caption,
        media_media_ids=mf_video_id
    )

    tweet_id = response.data['id']
    logger.info('mf video tweeted: https://twitter.com/user/status/' + tweet_id)


def tweet_text(logger, client, caption):
    logger.info('tweeting text')

    response = client.create_tweet(
        text=caption
    )

    tweet_id = response.data['id']
    logger.info('text tweeted: https://twitter.com/user/status/' + tweet_id)

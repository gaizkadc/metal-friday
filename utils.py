import os
import sys
import logging
import datetime
from logging.handlers import RotatingFileHandler


def get_logger():
    logs_folder_path = os.getenv('LOGS_FOLDER_PATH')
    app_name = os.getenv('APP_NAME')

    if not os.path.isdir(logs_folder_path):
        os.mkdir(logs_folder_path)
    log_file_path = logs_folder_path + '/' + app_name + '.log'
    if not os.path.isfile(log_file_path):
        log_file = open(log_file_path, "a")
        log_file.close()

    logger = logging.getLogger(app_name)
    logger.setLevel('DEBUG')

    log_format = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(log_file_path, maxBytes=(1048576 * 5), backupCount=5)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    logger.info('logger created')

    return logger


# Get filename
def create_mf_output_folder(logger, today):
    logger.info('creating metal friday output folder')

    output_folder_path = os.getenv('OUTPUT_FOLDER_PATH')

    mf_folder_path = output_folder_path + '/' + today

    if not os.path.exists(mf_folder_path):
        os.makedirs(mf_folder_path)

    return output_folder_path


def create_tumblr_tags(logger):
    logger.info('creating tumbler tags')

    tags = []

    input_folder_path = os.getenv('INPUT_FOLDER_PATH')

    now = datetime.datetime.now()  # + datetime.timedelta(days=1)
    today = now.strftime("%Y%m%d")

    with open(input_folder_path + '/' + today + '/' + today + '.list') as album_list_file:
        mf_lines = album_list_file.readlines()

    for mf_line in mf_lines:
        twitter_user, artist, album = mf_line.split('|')
        if twitter_user.strip() != '':
            mf_twitter_user = '@' + twitter_user.strip()
        else:
            mf_twitter_user = ''
        mf_artist = artist.replace(' ', '').replace('&', 'and').replace("'", "")
        mf_album = album.replace('\n', '').strip()

        tags.append(mf_artist)

    return tags

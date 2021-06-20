import os

from instabot import Bot


def instagram_collage(logger, video_path, caption):
    logger.info('instagramming collage')

    ig_bot = instagram_login(logger)

    ig_bot.upload_video(video_path, caption=caption)

    logger.info('mf video instagrammed')


def instagram_login(logger):
    logger.info('logging in instagram')

    ig_username = os.getenv('IG_USERNAME')
    ig_password = os.getenv('IG_PASSWORD')

    cookie_path = 'config/Fohoma_uuid_and_cookie.json'
    if os.path.exists(cookie_path):
        os.remove(cookie_path)

    bot = Bot()
    bot.login(username=ig_username, password=ig_password)

    return bot

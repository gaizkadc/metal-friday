from PIL import ImageFont, ImageDraw, Image
import moviepy.editor as editor
from pydub import AudioSegment
import os
import cv2

import settings


def create_title_img(logger, today, output_path):
    logger.info('creating title img')
    size = (500, 500)
    fonts_path = 'fonts'
    font = ImageFont.truetype(fonts_path + '/ImpactLabel.ttf', 40)
    text_color = (240, 240, 240)
    text_a_position = (50, 200)
    text_b_position = (250, 290)

    resulting_img_path = output_path + '/000MF.jpg'
    mf_title_img = Image.new('RGB', size)
    draw = ImageDraw.Draw(mf_title_img)
    draw.text(text_a_position, '#VIERNESDEMETAL', fill=text_color, font=font)
    draw.text(text_b_position, today, fill=text_color, font=font)
    mf_title_img.save(resulting_img_path)

    logger.info('mf title image created as {}'.format(resulting_img_path))
    return resulting_img_path


def create_mf_video(logger, output_folder_path, today):
    logger.info('creating mf video')

    # gc as in generated content
    gc_path = output_folder_path + '/' + today

    try:
        input_folder_path = settings.INPUT_FOLDER_PATH
    except ImportError as error:
        logger.info(error)
        logger.info('settings module not found, retrieving env variables')
        input_folder_path = os.getenv('INPUT_FOLDER_PATH')

    covers_folder_path = input_folder_path + '/' + today + '/covers'

    images = [img for img in os.listdir(covers_folder_path) if (img.lower().endswith('.jpg') or img.lower().endswith('.png') or img.lower().endswith('.webp'))]
    images = sorted(images)

    size = (500, 500)

    resized_covers_folder_path = gc_path + '/resized_covers'
    if not os.path.exists(resized_covers_folder_path):
        os.makedirs(resized_covers_folder_path)

    resized_covers = []
    title_img = create_title_img(logger, today, resized_covers_folder_path)
    resized_covers.append(title_img)

    for img in images:
        img_path = covers_folder_path + '/' + img
        final_image_path = resized_covers_folder_path + '/' + img
        cover = Image.open(img_path)
        cover = cover.resize(size, Image.ANTIALIAS)
        cover.save(final_image_path)
        resized_covers.append(final_image_path)

    clips_folder_path = gc_path + '/clips'
    if not os.path.exists(clips_folder_path):
        os.makedirs(clips_folder_path)

    mf_video_prefix = clips_folder_path + '/mf_clip_'
    mf_clips = []

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 1  # 1s every cover

    for i, img in enumerate(resized_covers):
        mf_video_name = mf_video_prefix + '0' + str(i) + '.avi'
        mf_video = cv2.VideoWriter(mf_video_name, fourcc, fps, size)
        mf_video.write(cv2.imread(img))
        mf_video.release()

        mf_clip = editor.VideoFileClip(mf_video_name)
        mf_clip_in = mf_clip.fadein(1)
        mf_clip_out = mf_clip.fadeout(1)
        mf_clips.append(mf_clip_in)
        mf_clips.append(mf_clip)
        mf_clips.append(mf_clip_out)

    audio_file_path = create_audio(logger, len(resized_covers), today, output_folder_path)
    audio = editor.AudioFileClip(audio_file_path)

    video_extension = 'mp4'
    video_codec = 'libx264'
    audio_codec = 'aac'
    final_fps = 30

    mf_final_video_path = gc_path + '/MF' + today + '.' + video_extension

    final_mf_video = editor.concatenate_videoclips(mf_clips)
    final_mf_video = final_mf_video.set_audio(audio)
    final_mf_video.write_videofile(filename=mf_final_video_path, fps=final_fps, codec=video_codec, audio_codec=audio_codec)

    logger.info('final mf video created at {}'.format(mf_final_video_path))

    return mf_final_video_path


def create_audio(logger, img_number, today, output_folder_path):
    logger.info('creating audio')

    sound = AudioSegment.from_file('audio/acrasia.mp3')

    audio_folder_path = output_folder_path + '/' + today + '/audio'
    if not os.path.exists(audio_folder_path):
        os.makedirs(audio_folder_path)

    audio_length = 3000 * img_number + 800     # 3s each img in ms plus some ms extra for good measure
    trimmed_audio = sound[:audio_length]
    faded_audio = trimmed_audio.fade_in(2000).fade_out(2000)

    final_audio_path = output_folder_path + '/' + today + '/audio/mf_audio.mp3'
    faded_audio.export(final_audio_path, format='mp3')

    logger.info('audio created')

    return final_audio_path

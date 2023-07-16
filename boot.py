#!/usr/bin/python3
from random import randint
from mfrc522 import SimpleMFRC522
from vlc import Instance
from pathlib import Path
import os
import logging
import random   
import glob
import RPi.GPIO as GPIO
import time

def playmovie(video, directory, player):
    """Plays a video."""
    VIDEO_PATH = Path(directory + video)
    isPlay = isplaying(player)

    if not isPlay:
        logging.info('playmovie: No videos playing, so play video.')
    else:
        if player.is_playing():
            logging.info('playmovie: Video already playing, so quit current video, then play')
            player.stop()

    try:
        player = Instance().media_player_new()
        player.set_mrl(str(VIDEO_PATH))
        player.play()
    except SystemError:
        logging.info('$Error: Cannot Find Video.')
    logging.info('playmovie: vlc %s' % video)
    return player

def isplaying(player):
    """Check if player is playing a video"""
    return player.is_playing()

def main():
    # Program start
    directory = '/media/usb/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()    # Setup reader
    logging.info('\n\n\n***** %s Begin Player****\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    current_movie_id = 111111222222
    playerOB = Instance().media_player_new()
    isMoviePlaying = False
    # Play boot.mkv at start
    playerOB = playmovie("boot.mkv", directory, playerOB)
    isMoviePlaying = True

    try:
        while True:
            isPlay = isplaying(playerOB)
            logging.debug("Movie Playing: %s" % isPlay)

            if not isPlay:
                current_movie_id = 555555555555
                time.sleep(0.5)  # Ajout du délai de 500 ms entre chaque scan

            idd, movie_name = reader.read()

            logging.debug("+ ID: %s" % idd)
            logging.debug("+ Movie Name: %s" % movie_name)
            movie_name = movie_name.rstrip()
            if current_movie_id != idd:
                logging.info('New Movie')
                logging.info("- ID: %s" % idd)
                logging.info("- Name: %s" % movie_name)
                if movie_name.endswith(('.mp4', '.avi', '.m4v','.mkv')):
                    current_movie_id = idd
                    logging.info("playing: vlc %s" % movie_name)
                    playerOB = playmovie(movie_name, directory, playerOB)
                    isMoviePlaying = True
                elif 'folder' in movie_name:
                    current_movie_id = idd
                    movie_directory = movie_name.replace('folder', '')
                    try:
                        movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
                        movie_name = movie_name.replace(directory, "")
                        direc = directory
                    except IndexError:
                        movie_name = 'videonotfound.mp4'
                        direc = 'media/usb/'
                    logging.info("randomly selected: vlc %s" % movie_name)
                    playerOB = playmovie(movie_name, direc, playerOB)
                    isMoviePlaying = True

            else:
                isPlay = isplaying(playerOB)

                if isPlay:
                    if playerOB.is_playing():
                        playerOB.pause()
                    else:
                        playerOB.play()
                time.sleep(0.5)  # Ajout du délai de 500 ms après la lecture du RFID
                # Vérifier si la lecture du film est terminée
                if isMoviePlaying and not playerOB.is_playing():
                    isMoviePlaying = False
                    current_movie_id = 0
                    logging.info("Movie playback finished")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nAll Done")

if __name__ == '__main__':
    main()

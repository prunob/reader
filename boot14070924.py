#!/usr/bin/python3
from random import randint	# Import randint function from random module
from mfrc522 import SimpleMFRC522
from vlc import Instance
from pathlib import Path
import os
import logging
import random	
import glob
import RPi.GPIO as GPIO


def playmovie(video, directory, player):
    """Plays a video."""
    VIDEO_PATH = Path(directory + video)
    isPlay = isplaying()

    if not isPlay:
        logging.info('playmovie: No videos playing, so play video.')
    else:
        logging.info('playmovie: Video already playing, so quit current video, then play')
        player.stop()

    try:	# Try to play video
        player = Instance().media_player_new()
        player.set_mrl(str(VIDEO_PATH))
        player.play()
    except SystemError:
        logging.info('$Error: Cannot Find Video.')

    logging.info('playmovie: vlc %s' % video)
    return player


def isplaying():
    """Check if vlc is running
    If the value returned is 1 or 0, vlc is NOT playing a video
    If the value returned is 2, vlc is playing a video"""
    processname = 'vlc'	# Name of the process you want to check
    tmp = os.popen("ps -Af").read()
    proccount = tmp.count(processname)

    if proccount == 1 or proccount == 0:
        proccount = False
    else:
        proccount = True

    return proccount


def main():
    # Program start
    directory = '/media/pi/BILLYUSB1/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()	# Setup reader
    current_movie_id = 111111222222
    playerOB = ""

    try:
        while True:
            isPlay = isplaying()
            logging.debug("Movie Playing: %s" % isPlay)

            if not isPlay:
                current_movie_id = 555555555555

            logging.info("Waiting for ID to be scanned")

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
                    
                elif 'folder' in movie_name:
                    current_movie_id = idd
                    movie_directory = movie_name.replace('folder', '')
                    
                    try:
                        movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
                        movie_name = movie_name.replace(directory, "")
                        direc = directory
                    except IndexError:
                        movie_name = 'videonotfound.mp4'
                        direc = 'home/bruno/'

                    logging.info("randomly selected: vlc %s" % movie_name)
                    playerOB = playmovie(movie_name, direc, playerOB)

            else:
                isPlay = isplaying()

                if isPlay:
                    if playerOB.is_playing():
                        playerOB.pause()
                    else:
                        playerOB.play()

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nAll Done")


if __name__ == '__main__':
    main()

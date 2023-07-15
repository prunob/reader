#!/usr/bin/python3
import os
import subprocess
from random import randint
from mfrc522 import SimpleMFRC522
from pathlib import Path
import logging
import random   
import glob
import RPi.GPIO as GPIO
import time

def playmovie(video, directory):
    """Plays a video."""
    VIDEO_PATH = Path(directory + video)

    # Stop any existing VLC processes
    subprocess.run(['killall', 'vlc'])

    try:
        # Launch VLC with desired options
        subprocess.Popen(['vlc', '--aout=pulse', str(VIDEO_PATH)])
    except Exception as e:
        logging.info('$Error: Cannot Find Video.')

def main():
    # Program start
    directory = '/media/usb/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()   # Setup reader
    logging.info('\n\n\n***** %s Begin Player****\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    current_movie_id = 111111222222
    isMoviePlaying = False

    # Play boot.mkv at start
    playmovie("boot.mkv", directory)
    isMoviePlaying = True

    try:
        while True:
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
                    playmovie(movie_name, directory)
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
                    playmovie(movie_name, direc)
                    isMoviePlaying = True

            time.sleep(0.5)  # Ajout du délai de 500 ms après la lecture du RFID

    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nAll Done")


if __name__ == '__main__':
    main()

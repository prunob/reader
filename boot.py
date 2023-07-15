#!/usr/bin/python3
from random import randint
from mfrc522 import SimpleMFRC522
from pathlib import Path
import os
import logging
import random	
import random   
import glob
import RPi.GPIO as GPIO
import time
import subprocess

def playmovie(video, directory):
    """Plays a video."""
    VIDEO_PATH = directory + video
    player = subprocess.Popen(["omxplayer", VIDEO_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return player

def is_playing(player):
    """Check if player is playing a video"""
    # Returns False if the process has terminated, True otherwise
    return player.poll() is None

def main():
    # Program start
    directory = '/media/usb/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()   # Setup reader
    logging.info('\n\n\n***** %s Begin Player****\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    current_movie_id = 111111222222
    player = playmovie("boot.mkv", directory)  # Play boot.mkv at start
    try:
        while True:
            isPlay = is_playing(player)
            logging.debug("Movie Playing: %s" % isPlay)
            if not isPlay:
                current_movie_id = 555555555555
                time.sleep(0.5)  # Delay of 500 ms between each scan
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
                    logging.info("playing: omxplayer %s" % movie_name)
                    player = playmovie(movie_name, directory)
                elif 'folder' in movie_name:
                    current_movie_id = idd
                    movie_directory = movie_name.replace('folder', '')
                    try:
                        movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
                        movie_name = movie_name.replace(directory, "")
                    except IndexError:
                        movie_name = 'videonotfound.mp4'
                    logging.info("randomly selected: omxplayer %s" % movie_name)
                    player = playmovie(movie_name, directory)
            else:
                isPlay = is_playing(player)
                if isPlay:
                    player.stdin.write(b'p')  # pause
                    player.stdin.flush()
                    time.sleep(0.5)
                    player.stdin.write(b'p')  # play
                    player.stdin.flush()
                time.sleep(0.5)  # Delay of 500 ms after RFID read
                # Check if movie playback is finished
                if isPlay and not is_playing(player):
                    current_movie_id = 0
                    logging.info("Movie playback finished")
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nAll Done")


if __name__ == '__main__':
    main()

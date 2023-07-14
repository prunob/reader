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
import pygame  # Import the pygame library

# The path to the image you want to display
IMAGE_PATH = "/media/usb/boot.jpg"

def playmovie(video, directory, player):
    """Plays a video."""
    pygame.quit()  # Close the image
    VIDEO_PATH = Path(directory + video)
    isPlay = isplaying()

    if not isPlay:
        logging.info('playmovie: No videos playing, so play video.')
    else:
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

def isplaying():
    """Check if vlc is running."""
    processname = 'vlc'
    tmp = os.popen("ps -Af").read()
    proccount = tmp.count(processname)

    if proccount == 1 or proccount == 0:
        proccount = False
    else:
        proccount = True

    return proccount

def display_image_pygame(image_path):
    """Displays an image fullscreen using pygame."""
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    img = pygame.image.load(image_path)
    screen.blit(img, (0, 0))
    pygame.display.flip()

def main():
    directory = '/media/usb/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()
    logging.info('\n\n\n***** %s Begin Player****\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    current_movie_id = 111111222222
    playerOB = ""
    isMoviePlaying = False

    display_image_pygame(IMAGE_PATH)  # Display the image

    try:
        while True:
            isPlay = isplaying()
            logging.debug("Movie Playing: %s" % isPlay)

            if not isPlay:
                current_movie_id = 555555555555
                time.sleep(0.5)  # Ajout du délai de 500 ms entre chaque scan

            idd, movie_name = reader.read()

            logging.debug("+ ID: %s" % idd)
            logging.debug("+ Movie Name: %s" % movie_name)

            movie_name = movie_name.rstrip()

            if current_movie_id != idd:
                current_movie_id = idd
                if movie_name.endswith(('.mp4', '.avi', '.m4v','.mkv')):
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
                isPlay = isplaying()

                if isPlay:
                    if playerOB.is_playing():
                        playerOB.pause()
                    else:
                        playerOB.play()

                time.sleep(0.5)  # Ajout du délai de 500 ms après la lecture du RFID

                if isMoviePlaying and not playerOB.is_playing():
                    isMoviePlaying = False
                    current_movie_id = 0
                    logging.info("Movie playback finished")

    except KeyboardInterrupt:
        pygame.quit()  # Make sure Pygame quits when the script is stopped
        GPIO.cleanup()
        print("\nAll Done")


if __name__ == '__main__':
    main()

#!/usr/bin/python3
from random import randint
from mfrc522 import SimpleMFRC522
from vlc import Instance
from pathlib import Path
import time
import os
import logging
import random
import random	
import random   
import glob
import RPi.GPIO as GPIO
import time
def playmovie(video, directory, player):
    """Plays a video."""
    VIDEO_PATH = Path(directory + video)
    if player.is_playing():
        logging.info('playmovie: Video already playing, so quit current video, then play')
        player.stop()

    try:
        player = Instance().media_player_new()
        player = Instance('--aout=pulse').media_player_new() # Change here
        player.set_mrl(str(VIDEO_PATH))
        player.play()
    except SystemError:
        logging.info('$Error: Cannot Find Video.')
    logging.info('playmovie: vlc %s' % video)
    return player

def playmovie(video,directory,player):

	"""plays a video."""

	VIDEO_PATH = Path(directory + video)

	isPlay = isplaying()

	if not isPlay:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + 'playmovie: No videos playing, so play video.')

	else:

		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+ 'playmovie: Video already playing, so quit current video, then play')
		player.stop()

	try:
		player = Instance().media_player_new()
		player.set_mrl(str(VIDEO_PATH))
		player.play()
	except SystemError:
		logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' $Error: Cannot Find Video.')

	logging.info('playmovie: vlc %s' % video)

	time.sleep(2)

	return player

def isplaying():

		"""check if vlc is running
		if the value returned is a 1 or 0, vlc is NOT playing a video
		if the value returned is a 2, vlc is playing a video"""

		processname = 'vlc'
		tmp = os.popen("ps -Af").read()
		proccount = tmp.count(processname)

		if proccount == 1 or proccount == 0:
			proccount = False
		else:
			proccount = True

		return proccount
def isplaying(player):
    """Check if player is playing a video"""
    return player.is_playing()


def main():
    # Program start
    directory = '/media/usb/'
    logging.basicConfig(level=logging.DEBUG)
    reader = SimpleMFRC522()	# Setup reader
    reader = SimpleMFRC522()   # Setup reader
    logging.info('\n\n\n***** %s Begin Player****\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    current_movie_id = 111111222222
    playerOB = Instance().media_player_new()
    playerOB = Instance('--aout=pulse').media_player_new()  # Change here
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

	#program start

	directory = '/media/pi/BILLYUSB1/'

	LOG_FILENAME = '/tmp/bplay_%s.log' %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).replace(" ","_").replace(":","")
	logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
	#logging.basicConfig(level=logging.DEBUG)

	reader = SimpleMFRC522()

	logging.info("\n\n\n***** %s Begin Player****\n\n\n" %time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

	current_movie_id = 111111222222

	playerOB = ""

	try:
		while True: 

			isPlay = isplaying()
			logging.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " Movie Playing: %s" % isPlay)

			if not isPlay:

				current_movie_id = 555555555555

			start_time = time.time()
			logging.debug('start_time0: %s' %start_time)

			logging.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " Waiting for ID to be scanned")

			temp_time = time.time()
			logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " #READER BEFORE %s" %temp_time)
			idd, movie_name = reader.read()

			temp_time = time.time() - temp_time
			logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " #READER AFTER - ELAPSED TIME %s" %temp_time)

logging.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " + ID: %s" % idd)
			logging.debug(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " + Movie Name: %s" % movie_name)

			movie_name = movie_name.rstrip()

			if current_movie_id != idd:

				logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' New Movie')
				logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " - ID: %s" % idd)
				logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " - Name: %s" % movie_name)
				#this is a check in place to prevent vlc from restarting video if ID is left over the reader.
				#better to use id than movie_name as there can be a problem reading movie_name occasionally


				if movie_name.endswith(('.mp4', '.avi', '.m4v','.mkv')):
					current_movie_id = idd 	#we set this here instead of above bc it may mess up on first read
					logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " playing: vlc %s" % movie_name)

					playerOB = playmovie(movie_name,directory,playerOB)


				elif 'folder' in movie_name:
					current_movie_id = idd
					movie_directory = movie_name.replace('folder',"") 

					try:

						movie_name = random.choice(glob.glob(os.path.join(directory + movie_directory, '*')))
						movie_name = movie_name.replace(directory,"")
						direc = directory
					except IndexError:
						movie_name = 'videonotfound.mp4'
						direc = 'home/bruno/'

					logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " randomly selected: vlc %s" % movie_name)
					playerOB = playmovie(movie_name,direc,playerOB)


			else:

				end_time = time.time()
				elapsed_time = end_time - start_time

				logging.debug('end_time: %s' %end_time)
				logging.debug('start_time1: %s' %start_time)

				isPlay = isplaying()

				if isPlay:

					if elapsed_time > 0.6 and elapsed_time < 8:
						#pause, unpause movie
						logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " PLAY/PAUSE %s" %elapsed_time)
						if playerOB.is_playing():
							playerOB.pause()
						else:
							playerOB.play()


	except KeyboardInterrupt:
		GPIO.cleanup()
		print("\nAll Done")

if __name__ == '__main__':

	main()
    main()

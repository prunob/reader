#!/usr/bin/python3
from random import randint
from mfrc522 import SimpleMFRC522
from vlc import Instance
from pathlib import Path
import time
import os
import logging
import random
import glob
import RPi.GPIO as GPIO


def playmovie(video, directory, player):

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


def main():

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
			logging.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + " #READER

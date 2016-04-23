''' Videoplay.py is a script for playing videos using GPIO pins on a Raspberry Pi SBC. 
	Adapted from https://www.hackster.io/ThothLoki/play-video-with-python-and-gpio-a30c7a .
    Copyright (C) 2016  Peter Svedman

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

'''	Import relevant libraries '''
import Rpi.GPIO as GPIO
import sysimport os
from subprocess import Popen

'''	Setup GPIO pins on the Raspberry Pi '''
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

'''	Set up movie locations and names '''	
movie1 = ("/home/pi/Videos/movie1.mp4")
movie2 = ("/home/pi/Videos/movie2.mp4")

'''	Set up state variables for the videos and GPIO pins '''
last_state1 = True
last_state2 = True

input_state1 = True
input_state2 = True

quit_video = True

''' Main loop '''
while True:
	'''Read states of inputs'''
	input_state1 = GPIO.input(17)
	input_state2 = GPIO.input(18)
	quite_video = GPIO.input(24)

	'''If GPIO(17) is shorted to ground'''
	if input_state1 != last_state1:
		if (player and not input_state1):
			os.system('killall omxplayer.bin')
			omxc = Popen(['omxplayer', '-b', movie1])
			player = True
		elif not input_state1:
			omxc = Popen(['omxplayer', '-b', movie1])
			player = True
	
	'''If GPIO(18) is shorted to ground'''
	elif input_state2 != last_state2:
		if (player and not input_state2):
			os.system('killall omxplayer.bin')
			omxc = Popen(['omxplayer', '-b', movie2])
			player = True
		elif not input_state2:
			omxc = Popen(['omxplayer', '-b', movie2])
			player = True

	'''If omxplayer is running and GPIO(17) and GPIO(18) are NOT shorted to ground'''
	elif (player and input_state1 and input_state2):
		os.system('killall omxplayer.bin')
		player = False

	'''GPIO(24) to close omxplayer manually - used during debug'''
	if quit_video == False:
		os.system('killall omxplayer.bin')
		player = False

	'''Set last_input states'''
	last_state1 = input_state1
	last_state2 = input_state2 
	
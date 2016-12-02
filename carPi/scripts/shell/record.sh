#!/bin/sh
 
file_name=/home/pi/carPi/video/webcam_
resolution=320x240
fps=30


for i in `seq 1 1 100` 
do
   	echo "Welcome $i times..."

	current_time=$(date "+%Y-%m-%d_%H.%M.%S")
	echo "Current Time : $current_time"
	 
	new_fileName=$file_name$current_time.mp4
	echo "New FileName: " "$new_fileName"
	
	#This was the toughest part of the whole project to find the optimal settings for recording.
	avconv -f video4linux2 -r $fps -s $resolution -i /dev/video0 -c:v mpeg4 -r $fps -s $resolution -b 1024k -an -t 00:05:00 -y $new_fileName
	#avconv -f video4linux2 -r 25 -i /dev/video0 -f alsa -i plughw:VX2000,0 -ar 11025 -ab 32k -strict experimental -acodec aac -vcodec mpeg4 -y $new_fileName	

	echo "Done with recording..."

done
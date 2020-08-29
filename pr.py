import numpy as np
import os
import cv2
from datetime import date

todaydate=date.today()

print(todaydate)

filename = 'video'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

def video_file_name(filename, num, et):
    file_num = str(num)
    return filename + file_num + et

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

def get_file_size_in_bytes(file_path):
   """ Get size of file at given path in bytes"""
   size = os.path.getsize(file_path)
   return size

video_num=1
video_et = '.avi'
fullfilename = video_file_name(filename, video_num, video_et)

cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(fullfilename, get_video_type(filename), 25, get_dims(cap, res))

while True:
    ret, frame = cap.read()

    if get_file_size_in_bytes(fullfilename) > (1024 * 1024 * 100):
        print(get_file_size_in_bytes(fullfilename))
        video_num = video_num + 1
        fullfilename = video_file_name(filename, video_num, video_et)
        out = cv2.VideoWriter(fullfilename, get_video_type(filename), 25, get_dims(cap, res))
    else:
        out.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
out.release()
cv2.destroyAllWindows()

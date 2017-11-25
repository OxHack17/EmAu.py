# Deprecated because avprobe not found. Using ffmpeg instead. 

import cv2
import numpy as np

import sys
import skvideo.io

print(cv2.__version__)
vidcap = cv2.VideoCapture("../data/IMG_1734.mp4")
#vidcap = skvideo.io.VideoCapture("../data/IMG_1734.mp4")

success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1

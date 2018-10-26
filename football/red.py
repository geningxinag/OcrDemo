# encoding:utf-8
import math
import os
import cv2
import numpy as np
from math import *


img = cv2.imread('images/IMG_4272.JPG')
cv2.imwrite("temp/2/img.jpg", img)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imwrite("temp/2/hsv.jpg", hsv)

lower_red = np.array([0, 40, 150])  # red
upper_red = np.array([7, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

cv2.imwrite("temp/2/red.jpg", red)
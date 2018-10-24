# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *


img = cv2.imread('images/IMG_4273.JPG')
#cv2.imshow("orginImg", img)

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 50, 50])  # red
upper_red = np.array([10, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

#cv2.imshow("red", red)
cv2.imwrite("temp/1.jpg", red)
# 腐蚀
element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

#腐蚀
erosion = cv2.erode(red, element0, iterations=3)
cv2.imwrite("temp/2.jpg", erosion)

# 膨胀
dilation = cv2.dilate(erosion, element1, iterations=3)
cv2.imwrite("temp/3.jpg", dilation)


image, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#找最长的轮廓
maxCnt = []

for i in range(len(cnts)):
    # 只关注轮廓点数量超过10 的轮廓
    if len(cnts[i]) > 10 and len(cnts[i]) > len(maxCnt):
        maxCnt = cnts[i]

cv2.drawContours(img, [maxCnt], -1, (0, 255, 0), 2)


cv2.imwrite("temp/4.jpg", img)

#cv2.waitKey()
#cv2.destroyAllWindows()
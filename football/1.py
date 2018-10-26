
# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *


img = cv2.imread('images/IMG_4275.JPG')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("temp1/main-1.jpg", img)

# 直方图均衡化 增加对比度
img = cv2.equalizeHist(img)
cv2.imwrite("temp1/main-2.jpg", img)

# 高斯平滑
img = cv2.GaussianBlur(img, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
cv2.imwrite("temp1/main-3.jpg", img)

img = cv2.equalizeHist(img)
cv2.imwrite("temp1/main-4.jpg", img)

# 中值滤波
median = cv2.medianBlur(img, 5)
cv2.imwrite("temp1/main-5.jpg", img)

# Sobel算子，X方向求梯度
sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
cv2.imwrite("temp1/main-6.jpg", sobel)

# Sobel算子，X方向求梯度
sobely = cv2.Sobel(median, cv2.CV_8U, 0, 1, ksize=3)
cv2.imwrite("temp1/main-6y.jpg", sobely)

# 二值化
ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
cv2.imwrite("temp1/main-7.jpg", binary)

#cv2.waitKey()
#cv2.destroyAllWindows()
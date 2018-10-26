# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *

# https://www.cnblogs.com/interdrp/p/5818770.html

tempImg = cv2.imread("temp/1/59.jpg")

cv2.imshow('tempImg', tempImg)

text = pytesseract.image_to_string(tempImg, lang='chi_sim')
# 空格没有什么好方法，  或者先定位每个数字？
print('OCR识别结果：', text)


cv2.waitKey()
cv2.destroyAllWindows()
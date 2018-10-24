# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *


# 定位票信息内容区域     img 图片  红色条带的区域x, y, h
def getTicketContentImg(img, x, y, w, h):
    x1 = int(x - h * 370 / 1000)
    y1 = int(y - h / 2 + h * 30 / 1000)
    w1 = int(h * 370 / 1000 - w / 2 - 2)
    h1 = int(h - h * 60 / 1000)
    return img[y1: y1 + h1, x1: x1 + w1]

img = cv2.imread('images/IMG_4273.JPG')

# 查找红色条带区域
[x, y], [w, h], rate = Util.findRedArea(img)

# 长宽是否有反转
if w > h:
    rate += 90

# 是否需要旋转
if abs(rate) > 0.1:
    img = Util.warpAffine(img, rate)
    # 查找红色条带区域
    [x, y], [w, h], rate = Util.findRedArea(img)

# 找到的区域 长宽 反了
if abs(rate) > 80:
    a = h
    h = w
    w = a

cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)

cv2.imshow('img', img)
# cv2.imwrite("temp/4.jpg", img)

# 截取 票内容区域
contentImg = getTicketContentImg(img, x, y, w, h)
cv2.imshow('contentImg', contentImg)

# 灰度
gray = cv2.cvtColor(contentImg, cv2.COLOR_BGR2GRAY)
# 二值化
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('binary', binary)

element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
# 膨胀  为了找文字区域
dilation = cv2.dilate(binary, element0, iterations=5)
cv2.imshow("dilation", dilation)

# 查找边框  RETR_EXTERNAL外轮廓
image, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

contentImg2 = contentImg.copy()
cv2.drawContours(contentImg2, cnts, -1, (0, 255, 0), 2)

cv2.imshow("image", contentImg2)

cv2.imshow("gray", gray)
# histImg = cv2.equalizeHist(gray)
# cv2.imshow("histImg", histImg)
ret, bitImg = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

for i in range(len(cnts)):
    # 只关注轮廓点数量超过5 的轮廓
    if len(cnts[i]) > 5:
        rect = cv2.minAreaRect(cnts[i])
        print(rect)
        [x, y], [w, h], rate = rect

        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print("#######   " + str(i) + "   ######")

        if h < 5 or w < 5:
            continue
        # 长、宽 反转    按轮廓切图
        if w < h:
            tempImg = Util.rotate(bitImg, box[1], box[2], box[3], box[0])
        else:
            tempImg = Util.rotate(bitImg, box[0], box[1], box[2], box[3])


        cv2.imwrite("temp/1/" + str(i) + ".jpg", tempImg)

        # try:
        #     text = pytesseract.image_to_string(tempImg, lang='num')
        #     # 空格没有什么好方法，  或者先定位每个数字？
        #     print('OCR识别结果：', text)
        # except Exception as e:
        #     print(e)

cv2.waitKey()
cv2.destroyAllWindows()

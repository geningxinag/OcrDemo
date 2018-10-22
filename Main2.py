# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *


def handle(dir, filename):
    img = cv2.imread(dir + filename)

    # 查找红色条带区域
    [x, y], [w, h], rate = Util.findRedArea(img)

    if w > h:
        rate += 90

    if abs(rate) > 1:
        img = Util.warpAffine(img, rate)
        # 查找红色条带区域
        [x, y], [w, h], rate = Util.findRedArea(img)

    # 找到的区域 长宽 反了
    if abs(rate) > 80:
        a = h
        h = w
        w = a

    print('找到的红色条带轮廓：', filename, x, y, w, h, rate)

    # 红色条带
    # cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
    width, height, pixels = img.shape
    # 定位号码区域
    x1 = int(x - h * 480 / 680)
    y1 = int(y - h / 2 + h * 50 / 680)
    w1 = int(h * 463 / 680)
    h1 = int(h - h * 80 / 680)

    if x1 > 0 and y1 > 0 and x1 + w1 < width and y1 + h1 < width:
        img = img[y1: y1 + h1, x1: x1 + w1]
        # cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)

    cv2.imshow('img3', img)

    cv2.imwrite('1/101.jpg', img)

    cv2.waitKey()
    cv2.destroyAllWindows()


rootdir = 'D:/PycharmProjects/OcrDemo/1/'

# list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
# for i in range(0, len(list)):
#     print('#################')
#     print(rootdir, list[i])
#     handle(rootdir, list[i])


handle(rootdir, '102.jpg')

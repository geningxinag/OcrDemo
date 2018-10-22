# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *


def handle(dir, filename):
    img = cv2.imread(dir + filename)

    width, height, pixels = img.shape

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
    cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)

    # 定位号码区域
    x1 = int(x - h * 445 / 681)
    y1 = int(y - h / 2 + h * 248 / 681)
    w1 = int(h * 400 / 681)
    h1 = int(h * 143 / 681 / 5)

    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 增加对比度
    gray = cv2.equalizeHist(gray)
    # 高斯平滑 应该不需要
    # gray = cv2.GaussianBlur(gray, (1, 1), 0, 0, cv2.BORDER_DEFAULT)
    # 二值化
    ret, binary = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    for i in range(5):
        # print('号码区域：', i)
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
        if x1 > 0 and y1 > 0 and x1 + w1 < width and y1 + h1 < width:
            tempImg = binary[y1: y1 + h1, x1: x1 + w1]
            cv2.imwrite('2/' + filename + '_number_' + str(i) + '.tif', tempImg)
            # cv2.imwrite('step/4_' + str(i) + '.tif', tempImg)
            try:
                text = pytesseract.image_to_string(tempImg, lang='num')
                # 空格没有什么好方法，  或者先定位每个数字？
                print('OCR识别结果：', text.replace(' ', ''))
            except Exception as e:
                print('出错啦')

        y1 += h1

    # cv2.imshow('img3', img)
    cv2.imwrite('D:/PycharmProjects/OcrDemo/2/' + filename, img)


rootdir = 'D:/PycharmProjects/OcrDemo/1/'

# list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
# for i in range(0, len(list)):
#     print('#################')
#     print(rootdir, list[i])
#     handle(rootdir, list[i])


handle(rootdir, '104.jpg')

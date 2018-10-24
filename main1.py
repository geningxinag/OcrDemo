# encoding:utf-8

import os
import cv2
import numpy as np
import pytesseract
import Util
from math import *

global isDebug


# 定位票信息内容区域     img 图片  红色条带的区域x, y, h
def getTicketContentImg(img, x, y, h):
    x1 = int(x - h * 470 / 680)
    y1 = int(y - h / 2 + h * 50 / 680)
    w1 = int(h * 450 / 680)
    h1 = int(h - h * 80 / 680)
    return img[y1: y1 + h1, x1: x1 + w1];


def handle(dir, filename):
    # 读取图片
    img = cv2.imread(dir + filename)
    cv2.imshow("orginImg", img)

    if isDebug:
        cv2.imwrite('temp1/1.jpg', img)

    width, height, pixels = img.shape

    # 查找红色条带区域
    [x, y], [w, h], rate = Util.findRedArea(img)

    # 长宽是否有反转
    if w > h:
        rate += 90

    # 是否需要旋转
    if abs(rate) > 1:
        img = Util.warpAffine(img, rate)
        # 查找红色条带区域
        [x, y], [w, h], rate = Util.findRedArea(img)

    # 找到的区域 长宽 反了
    if abs(rate) > 80:
        a = h
        h = w
        w = a
    if isDebug:
        cv2.imwrite('temp1/2.jpg', img)
    print('找到的红色条带轮廓：', filename, x, y, w, h, rate)

    # 截取 票内容区域
    contentImg = getTicketContentImg(img, x, y, h)
    cv2.imshow('contentImg', contentImg)
    if isDebug:
        cv2.imwrite('temp1/3.jpg', contentImg)

    return handerContent(contentImg)


# 处理票区域
def handerContent(contentImg):
    # 灰度
    gray = cv2.cvtColor(contentImg, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 1))
    # 膨胀  为了找文字区域
    dilation = cv2.dilate(binary, element0, iterations=5)
    # cv2.imshow("dilation", dilation)
    if isDebug:
        cv2.imwrite('temp1/4.jpg', dilation)

    # 查找边框  RETR_EXTERNAL外轮廓
    image, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 直方图均衡化 增加对比度
    temp1Img = cv2.equalizeHist(gray)
    # 二值化
    ret, bitImg = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    if isDebug:
        cv2.imwrite("temp1/5.jpg", bitImg)

    for i in range(len(cnts)):
        # 只关注轮廓点数量超过5 的轮廓
        if len(cnts[i]) > 5:
            rect = cv2.minAreaRect(cnts[i])
            print(rect)
            [x, y], [w, h], rate = rect



            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # TODO 怎么实现 根据轮廓 抠图

            print("#######   " + str(i) + "   ######")

            if h < 5 or w < 5:
                continue
            # 长、宽 反转    按轮廓切图
            if w < h:
                tempImg = Util.rotate(bitImg, box[1], box[2], box[3], box[0])
            else:
                tempImg = Util.rotate(bitImg, box[0], box[1], box[2], box[3])

            if isDebug:
                cv2.imwrite("temp1/9_" + str(i) + ".jpg", tempImg)

            try:
                text = pytesseract.image_to_string(tempImg, lang='num')
                # 空格没有什么好方法，  或者先定位每个数字？
                print('OCR识别结果：', text)
            except Exception as e:
                print(e)


    cv2.imshow("img2", contentImg)
    if isDebug:
        cv2.imwrite("temp1/6.jpg", contentImg)
    return 0


isDebug = True

rootdir = '1/'

# list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
# for i in range(0, len(list)):
#     print('#################')
#     print(rootdir, list[i])
#     handle(rootdir, list[i])


handle(rootdir, 'IMG_4264.JPG')

cv2.waitKey()
cv2.destroyAllWindows()

# encoding:utf-8

import os
import cv2
import numpy as np
from math import *


def findRedArea(img):
    # 提取彩票中的 红色条带
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])  # red
    upper_red = np.array([10, 255, 255])
    red = cv2.inRange(hsv, lower_red, upper_red)

    # 查找边框  RETR_EXTERNAL外轮廓
    image, cnts, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsJoin = []

    for i in range(len(cnts)):
        # 只关注轮廓点数量超过10 的轮廓
        if len(cnts[i]) > 10:
            for j in range(len(cnts[i])):
                for k in range(len(cnts[i][j])):
                    (x0, y0) = cnts[i][j][k]
                    # print(x0, y0)
                    cntsJoin.append([x0, y0])

    return cv2.minAreaRect(np.array([cntsJoin]))


# 旋转
def warpAffine(img, degree):
    height, width = img.shape[:2]
    # 旋转后的尺寸
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))
    matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)
    matRotation[0, 2] += (widthNew - width) / 2  # 重点在这步，目前不懂为什么加这步
    matRotation[1, 2] += (heightNew - height) / 2  # 重点在这步
    return cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))
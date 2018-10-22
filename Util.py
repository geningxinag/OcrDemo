# encoding:utf-8
import math
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


'''旋转图像并剪裁'''
def rotate(img, pt1, pt2, pt3, pt4):
    # pt1 = [pt1[0] - 3, pt1[1] - 3]
    # pt2 = [pt2[0] + 3, pt2[1] - 3]
    # pt3 = [pt3[0] + 3, pt3[1] + 3]
    # pt4 = [pt4[0] - 3, pt4[1] + 3]

    print(pt1, pt2, pt3, pt4)

    withRect = math.sqrt((pt4[0] - pt1[0]) ** 2 + (pt4[1] - pt1[1]) ** 2)  # 矩形框的宽度
    heightRect = math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)
    print(withRect, heightRect)

    angle = acos((pt4[0] - pt1[0]) / withRect) * (180 / math.pi)  # 矩形框旋转角度
    print(angle)

    if pt4[1] > pt1[1]:
        print("顺时针旋转")

    else:
        print("逆时针旋转")
        angle = -angle

    height = img.shape[0]  # 原始图像高度
    width = img.shape[1]  # 原始图像宽度
    rotateMat = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)  # 按angle角度旋转图像
    heightNew = int(width * fabs(sin(radians(angle))) + height * fabs(cos(radians(angle))))
    widthNew = int(height * fabs(sin(radians(angle))) + width * fabs(cos(radians(angle))))

    rotateMat[0, 2] += (widthNew - width) / 2
    rotateMat[1, 2] += (heightNew - height) / 2
    imgRotation = cv2.warpAffine(img, rotateMat, (widthNew, heightNew), borderValue=(255, 255, 255))


    # 旋转后图像的四点坐标
    [[pt1[0]], [pt1[1]]] = np.dot(rotateMat, np.array([[pt1[0]], [pt1[1]], [1]]))
    [[pt3[0]], [pt3[1]]] = np.dot(rotateMat, np.array([[pt3[0]], [pt3[1]], [1]]))
    [[pt2[0]], [pt2[1]]] = np.dot(rotateMat, np.array([[pt2[0]], [pt2[1]], [1]]))
    [[pt4[0]], [pt4[1]]] = np.dot(rotateMat, np.array([[pt4[0]], [pt4[1]], [1]]))

    # 处理反转的情况
    if pt2[1] > pt4[1]:
        pt2[1], pt4[1] = pt4[1], pt2[1]
    if pt1[0] > pt3[0]:
        pt1[0], pt3[0] = pt3[0], pt1[0]

    imgOut = imgRotation[int(pt2[1]):int(pt4[1]), int(pt1[0]):int(pt3[0])]

    return imgOut  # rotated image


# 根据四点画原矩形
def drawRect(img, pt1, pt2, pt3, pt4, color, lineWidth):
    cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, pt3, color, lineWidth)
    cv2.line(img, pt3, pt4, color, lineWidth)
    cv2.line(img, pt1, pt4, color, lineWidth)

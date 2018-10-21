import os
import cv2
import numpy as np
from math import *

rootdir = 'D:/PycharmProjects/OcrDemo/1'
list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list)):
    path = os.path.join(rootdir, list[i])
    print(path)
    img = cv2.imread(path, cv2.IMREAD_COLOR)


    # 提取彩票中的 红色条带
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])  # red
    upper_red = np.array([10, 255, 255])
    red = cv2.inRange(hsv, lower_red, upper_red)

    cv2.imwrite('D:/PycharmProjects/OcrDemo/2/a_' + str(i) + '.jpg', red)

    continue

    # 查找边框
    image, cnts, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # copyImg = img.copy()
    # cv2.drawContours(copyImg, cnts, -1, (0, 0, 255), 3)
    # cv2.imshow('img2', copyImg)

    # 找最长的边框 theCnt
    count = 0
    for j in range(len(cnts)):
        if len(cnts[j]) > count:
            theCnt = cnts[j]
        count = len(cnts[j])

    # 最小面积的矩形
    [x, y], [w, h], rate = cv2.minAreaRect(theCnt)

    cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
    cv2.imwrite('D:/PycharmProjects/OcrDemo/2/a_' + str(i) + '.jpg', img)


    # TODO 暂未考虑角度问题
    print('定位红色条带区域：', x, y, w, h, rate)

    if abs(rate) > 5 :
        height, width = img.shape[:2]

        degree = rate
        # 旋转后的尺寸
        heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
        widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

        matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)

        matRotation[0, 2] += (widthNew - width) / 2  # 重点在这步，目前不懂为什么加这步
        matRotation[1, 2] += (heightNew - height) / 2  # 重点在这步

        imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

        cv2.imwrite('D:/PycharmProjects/OcrDemo/2/' + str(i) + '.jpg', imgRotation)
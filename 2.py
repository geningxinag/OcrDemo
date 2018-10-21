import os
import cv2
import numpy as np
from math import *

img = cv2.imread('D:/PycharmProjects/OcrDemo/1/1.jpg', cv2.IMREAD_COLOR)

# 提取彩票中的 红色条带
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 100, 100])  # red
upper_red = np.array([10, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

# 查找边框  RETR_EXTERNAL外轮廓
image, cnts, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
copyImg = img.copy()

cv2.drawContours(copyImg, cnts, -1, (0, 0, 255), 3)
cv2.imshow('img1', copyImg)

# print(cnts)
cntsJoin = ([])
# cntsJoin.append(cnts[0][0])
# print(cntsJoin)
#

cntsJoin = []

for i in range(len(cnts)):
    if len(cnts[i]) > 10:
        for j in range(len(cnts[i])):
            for k in range(len(cnts[i][j])):
                (x0, y0) = cnts[i][j][k]
                # print(x0, y0)
                cntsJoin.append([x0, y0])

print(cnts[0])
print(cnts[1])

cntsJoin1 = np.array([cntsJoin])
print(cntsJoin1)
[x, y], [w, h], rate = cv2.minAreaRect(cntsJoin1)

print(x, y, w, h, rate)

if abs(rate) > 5:
    height, width = img.shape[:2]

    degree = (90+rate)
    # 旋转后的尺寸
    heightNew = int(width * fabs(sin(radians(degree))) + height * fabs(cos(radians(degree))))
    widthNew = int(height * fabs(sin(radians(degree))) + width * fabs(cos(radians(degree))))

    matRotation = cv2.getRotationMatrix2D((width / 2, height / 2), degree, 1)

    matRotation[0, 2] += (widthNew - width) / 2  # 重点在这步，目前不懂为什么加这步
    matRotation[1, 2] += (heightNew - height) / 2  # 重点在这步

    # TODO 这个旋转不对
    imgRotation = cv2.warpAffine(img, matRotation, (widthNew, heightNew), borderValue=(255, 255, 255))

    cv2.imwrite('D:/PycharmProjects/OcrDemo/2/1.jpg', imgRotation)
    img = imgRotation

# 提取彩票中的 红色条带
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 100, 100])  # red
upper_red = np.array([10, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

# 查找边框  RETR_EXTERNAL外轮廓
image, cnts, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
copyImg = img.copy()

cv2.drawContours(copyImg, cnts, -1, (0, 0, 255), 3)
cv2.imshow('img1', copyImg)

# print(cnts)
cntsJoin = ([])
# cntsJoin.append(cnts[0][0])
# print(cntsJoin)
#

cntsJoin = []

for i in range(len(cnts)):
    if len(cnts[i]) > 10:
        for j in range(len(cnts[i])):
            for k in range(len(cnts[i][j])):
                (x0, y0) = cnts[i][j][k]
                # print(x0, y0)
                cntsJoin.append([x0, y0])

print(cnts[0])
print(cnts[1])

cntsJoin1 = np.array([cntsJoin])
print(cntsJoin1)
[x, y], [w, h], rate = cv2.minAreaRect(cntsJoin1)

print(x, y, w, h, rate)


copyImg2 = img.copy()
#cv2.drawContours(copyImg2, cntsJoin1, -1, (0, 0, 255), 3)
cv2.rectangle(copyImg2, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
cv2.imshow('img2', copyImg2)

cv2.waitKey()
cv2.destroyAllWindows()

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

cntsJoin = ([])

for i in range(len(cnts)):
    for j in range(len(cnts[i])):
        for k in range(len(cnts[i][j])):
            print(cnts[i][j][k])
            cntsJoin.append(cnts[i][j][k])

print(cnts[0])
print(cntsJoin)

[x, y], [w, h], rate = cv2.minAreaRect(cntsJoin[0])

copyImg2 = img.copy()
cv2.rectangle(copyImg2, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
cv2.imshow('img2', copyImg2)

cv2.waitKey()
cv2.destroyAllWindows()

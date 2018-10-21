# _*_coding:utf-8_*_

import numpy as np
import cv2
import pytesseract

# 读取图片
img = cv2.imread('images/1.jpg', cv2.IMREAD_COLOR)
cv2.imshow('img0', img)

cv2.imwrite('step/0.jpg', img)

# 提取彩票中的 红色条带
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 100, 100])  # red
upper_red = np.array([10, 255, 255])
red = cv2.inRange(hsv, lower_red, upper_red)

# cv2.imshow('red', red)
cv2.imwrite('step/1.jpg', red)

# 查找边框
image, cnts, hierarchy = cv2.findContours(red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# copyImg = img.copy()
# cv2.drawContours(copyImg, cnts, -1, (0, 0, 255), 3)
# cv2.imshow('img2', copyImg)

# 找最长的边框 theCnt
count = 0
for i in range(len(cnts)):
    if len(cnts[i]) > count:
        theCnt = cnts[i]
    count = len(cnts[i])

# 最小面积的矩形
[x, y], [w, h], rate = cv2.minAreaRect(theCnt)

# TODO 暂未考虑角度问题
print('定位红色条带区域：', x, y, w, h, rate)
tempImg = img.copy()
# 画出 红色条带 的区域
cv2.rectangle(tempImg, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
cv2.imwrite('step/2.jpg', tempImg)

# 定位号码区域
x1 = int(x - h * 433 / 681)
y1 = int(y - h / 2 + h * 271 / 681)
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
regionImg = binary.copy()
for i in range(5):
    print('号码区域：', i)
    cv2.rectangle(regionImg, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
    tempImg = binary[y1: y1 + h1, x1: x1 + w1]
    cv2.imwrite('temp/number_' + str(i) + '.tif', tempImg)
    cv2.imwrite('step/4_' + str(i) + '.tif', tempImg)
    text = pytesseract.image_to_string(tempImg, lang='num')
    # 空格没有什么好方法，  或者先定位每个数字？
    print('OCR识别结果：', text.replace(' ', ''))

    y1 += h1

cv2.imshow('img3', regionImg)
cv2.imwrite('step/3.jpg', regionImg)

cv2.waitKey()
cv2.destroyAllWindows()

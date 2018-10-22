import os
import cv2
import pytesseract
from PIL import Image
import numpy as np

import Util

img = cv2.imread('D:/PycharmProjects/OcrDemo/images/101.jpg')


cv2.imshow("img", img)
cv2.imwrite("temp1/1.jpg", img)

originalImg = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 二值化
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

cv2.imshow("binary", binary)
cv2.imwrite("temp1/2.jpg", binary)


# 膨胀和腐蚀操作的核函数
element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# 膨胀、腐蚀、再膨胀，数字连接成一个区块
dilation = cv2.dilate(binary, element0, iterations=5)
cv2.imshow("dilation", dilation)

cv2.imwrite("temp1/3.jpg", dilation)

# 查找边框  RETR_EXTERNAL外轮廓
image, cnts, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# 直方图均衡化 增加对比度
temp1Img = cv2.equalizeHist(gray)
# 二值化
ret, bitImg = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imwrite("temp1/4.jpg", bitImg)

for i in range(len(cnts)):
    # 只关注轮廓点数量超过5 的轮廓
    if len(cnts[i]) > 5:
        rect = cv2.minAreaRect(cnts[i])
        # print(rect)
        [x, y], [w, h], rate = rect
        box = cv2.boxPoints(rect)
        #print(box)

        # x1 = int(min(box[0][0], box[1][0], box[2][0], box[3][0]) - 1)
        # x2 = int(max(box[0][0], box[1][0], box[2][0], box[3][0]) + 1)
        # y1 = int(min(box[0][1], box[1][1], box[2][1], box[3][1]) - 1)
        # y2 = int(max(box[0][1], box[1][1], box[2][1], box[3][1]) + 1)

        #print(x1, x2, y1, y2)
        box = np.int0(box)
        # TODO 怎么实现 根据轮廓 抠图
        cv2.drawContours(img, [box], -1, (0, 255, 0), 1)
        print("#######   " + str(i) + "   ######")
        #长、宽 反转
        if w < h :
            tempImg = Util.rotate(bitImg,  box[1], box[2], box[3], box[0])
        else:
            tempImg = Util.rotate(bitImg, box[0], box[1], box[2], box[3])
        cv2.imwrite("temp1/9_" + str(i) + ".jpg", tempImg)

        text = pytesseract.image_to_string(tempImg, lang='num')
        # 空格没有什么好方法，  或者先定位每个数字？
        print('OCR识别结果：', text)

        #cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        # print(box)
        # print((box[1][0], box[1][1]), (box[3][0], int(box[3][1] + 10)))
        # cv2.rectangle(img, (box[1][0], box[1][1]), (box[3][0], box[3][1]), (0, 255, 0), 1)
        # cv2.drawContours(img, cnts[i], -1, (0, 255, 0), 2)

cv2.imshow("img2", img)
cv2.imwrite("temp1/5.jpg", img)


# erosion = cv2.erode(dilation, element0, iterations=1)
# cv2.imwrite("temp1/main-12.jpg", erosion)
#
# dilation_ = cv2.dilate(erosion, element1, iterations=3)
# cv2.imwrite("temp1/main-13.jpg", dilation_)


cv2.waitKey()
cv2.destroyAllWindows()

import os
import cv2
from PIL import Image

img = cv2.imread('D:/PycharmProjects/OcrDemo/images/12.jpg')

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("temp1/main-1.jpg", img)

# 直方图均衡化 增加对比度
img = cv2.equalizeHist(img)
cv2.imwrite("temp1/main-2.jpg", img)

# 高斯平滑
img = cv2.GaussianBlur(img, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
cv2.imwrite("temp1/main-3.jpg", img)

img = cv2.equalizeHist(img)
cv2.imwrite("temp1/main-4.jpg", img)

# 中值滤波
median = cv2.medianBlur(img, 5)
cv2.imwrite("temp1/main-5.jpg", img)

# Sobel算子，X方向求梯度
sobel = cv2.Sobel(median, cv2.CV_8U, 1, 0, ksize=3)
cv2.imwrite("temp1/main-6.jpg", sobel)

# 二值化
ret, binary = cv2.threshold(sobel, 170, 255, cv2.THRESH_BINARY)
cv2.imwrite("temp1/main-7.jpg", binary)

img = binary

# 膨胀和腐蚀操作的核函数
element0 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
# 膨胀、腐蚀、再膨胀，数字连接成一个区块
dilation = cv2.dilate(img, element0, iterations=1)
cv2.imwrite("temp1/main-11.jpg", dilation)

erosion = cv2.erode(dilation, element0, iterations=1)
cv2.imwrite("temp1/main-12.jpg", erosion)

dilation_ = cv2.dilate(erosion, element1, iterations=3)
cv2.imwrite("temp1/main-13.jpg", dilation_)
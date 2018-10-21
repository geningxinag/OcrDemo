import os
import cv2
from PIL import Image

rootdir = 'D:/PycharmProjects/OcrDemo/1'
list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
for i in range(0, len(list)):
    path = os.path.join(rootdir, list[i])
    print(path)

    img = Image.open(path)
    print(img.size)
    (x, y) = img.size
    x_s = 800
    y_s = int(y * 800 / x)
    new_im = img.resize((x_s, y_s), Image.ANTIALIAS)

    new_im.save('D:/PycharmProjects/OcrDemo/2/' + str(i) + '.jpg')



import cv2
from imutils.perspective import four_point_transform
import pytesseract
import os
from PIL import Image
import argparse
import matplotlib as plt
import numpy as np
# 绘图展示
def cv2_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

image = cv2.imread("D:/check2.jpg")
cv2_show('origin',image)
#ratio = image.shape[0] / 800  # 比例,h除以500，w自行计算
#print(ratio)
orig = image.copy()  # copy（）不对原图改变
#500是设置的h为500，(int(image.shape[1]/ratio))为变化后的w,(h,w)
# resize_image = cv2.resize(orig, (800,int(image.shape[1]/ratio)))
resize_image = cv2.resize(orig, None,fx=0.2,fy=0.2)
# 想用原图直接注释上一条用下一条即可
# resize_image=image.copy()
cv2_show('resize',resize_image)

# 预处理操作
gray = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)
cv2_show('gray',gray)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
cv2_show('GaussianBlur',gray)
edged = cv2.Canny(gray, 75, 200)

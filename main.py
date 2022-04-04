import imp
import cv2
import numpy
from cv2 import cvtColor
from matplotlib import pyplot as plt


# (B, G, R) = img[105, 152]
# fig = plt.figure(figsize=(6,4))
# imgRGB = cvtColor(img, cv2.COLOR_BGR2RGB)
# ax = fig.add_subplot()
# ax.imshow(imgRGB)

# plt.show()

top_left_corner = []
bottom_right_corner = []

def drawRectangle(action, x, y, flags, *userdata):
    global top_left_corner, bottom_right_corner
    if action == cv2.EVENT_LBUTTONDOWN:
        top_left_corner = [(x, y)]
    elif action == cv2.EVENT_LBUTTONUP:
        bottom_right_corner = [(x, y)]
        cv2.rectangle(img, top_left_corner[0], bottom_right_corner[0], (0,255,0), 2, 8)
        cv2.imshow('Window', img)

img = cv2.imread('images/testInfra.bmp')

temp = img.copy()

cv2.namedWindow('Window')
cv2.setMouseCallback('Window', drawRectangle)   



k = 0
while k!=113:
    cv2.imshow('Window', img)
    k = cv2.waitKey(0)
    if k == 99:
        img = temp.copy
        cv2.imshow("Window", img)

# print('R = {}, G = {}, B = {}'.format(R, G, B))

cv2.waitKey(0)
import cv2
import numpy as np
import sys

print(dir(cv2))

RESIZE_FACTOR=10

img = cv2.imread('IMG_20210414_162502.jpg',1)
#img = cv2.medianBlur(img,5)
h, w = img.shape[:2]
h = int(h/RESIZE_FACTOR)
w = int(w/RESIZE_FACTOR)
rimg = cv2.resize(img,(w,h))
gimg = cv2.cvtColor(rimg,cv2.COLOR_BGR2GRAY)

(thresh, bw) = cv2.threshold(gimg, 2, 255, cv2.THRESH_BINARY)
cv2.imwrite('/tmp/circlebw.png',bw)
#gimg = cv2.cvtColor(bw,cv2.COLOR_BINARY2GRAY)
gimg = bw

print('begin')
print(h,w)
circles = cv2.HoughCircles(gimg,cv2.HOUGH_GRADIENT,1,10,
                            param1=1,param2=10,minRadius=int(0.48*w),maxRadius=int(.5*w))
print('here')
#circles = np.uint16(np.around(circles))

circle = circles[0,0]

x, y = int(circle[0]*RESIZE_FACTOR),int(circle[1]*RESIZE_FACTOR)
r = int(circle[2]*RESIZE_FACTOR*0.99)

#cv2.circle(img,(x,y),r,(0,255,0),2)

h, w = img.shape[:2]
circle_img = np.zeros((h,w), np.uint8)
cv2.circle(circle_img,(x,y),r,1,thickness=-1)

img[circle_img==0] = [255,255,255]


cv2.imwrite('/tmp/circle.png',img)

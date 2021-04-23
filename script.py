import cv2
import numpy as np
import sys


RESIZE_FACTOR=10

## FUNCTIONS

def load():

	img = cv2.imread('IMG_20210414_162502.jpg',1)
	img1 = cv2.imread('IMG_20210414_162457.jpg',1)
	return img, img1
 

def resize_img(resize_factor):

	h, w = img.shape[:2]
	h = int(h/resize_factor)
	w = int(w/resize_factor)
	rimg = cv2.resize(img,(w,h))
	return w, rimg


def find_circle(w,rimg):
	
	gimg = cv2.cvtColor(rimg,cv2.COLOR_BGR2GRAY)
	(_, bw) = cv2.threshold(gimg, 2, 255, cv2.THRESH_BINARY)
	circles = cv2.HoughCircles(bw, cv2.HOUGH_GRADIENT, 1, 10, param1=1, param2=10, minRadius=int(0.48*w), maxRadius=int(.5*w))
	circle = circles[0,0]
	x, y, r = int(circle[0]), int(circle[1]), int(circle[2]*0.99)
	return x, y, r


def initial_coordinates_radius(x_r, y_r, r_r, resize_factor):
	
	x = x_r*resize_factor
	y = y_r*resize_factor
	r = r_r*resize_factor
	return x, y, r
	

def mask_to_img():
	
	h, w = img.shape[:2]
	circle_img = np.zeros((h,w), np.uint8)
	cv2.circle(circle_img,(x,y),r,1,thickness=-1)
	
	img[circle_img==0] = [255,255,255]
	img1[circle_img==0] = [255,255,255]
	
	cv2.imwrite('/tmp/circle.png',img)
	cv2.imwrite('/tmp/circle1.png',img1)


def combine_img():
	
	img1 = cv2.imread('/tmp/circle.png')
	img2 = cv2.imread('/tmp/circle1.png')
	vis = np.concatenate((img1, img2), axis=1)
	cv2.imwrite('/tmp/combine.tiff', vis)



## PROGRAMMA

#load photo thinsiction
(img,img1) = load()

#resize photo thinsiction
(w, rimg) = resize_img(RESIZE_FACTOR)

#find in resise photo thinsection coordinates centre and radius circle
x_r, y_r, r_r = find_circle(w, rimg)

#convert coordinates centre and radius circle to initial size photo
x, y, r = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR)

#put mask to thinsection photo
mask_to_img()

#combine two photo (-,+) thinsection
combine_img()




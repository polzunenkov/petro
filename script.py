import cv2
import numpy as np
import sys
import glob
import subprocess

RESIZE_FACTOR=10
new_path = "/tmp/petro/~/Q/1/x2.5/2/"


## FUNCTIONS
def pr(new_path):
	print(new_path)


def load(new_path):
	
	images = glob.glob(str(new_path+"*.jpg"))
	im1 = str(images[0])
	im2 = str(images[1])
	#subprocess.run(["mv", im1, new_path+"1.jpg"])
	#subprocess.run(["mv", im2, new_path+"2.jpg"])
	#images = glob.glob(str(new_path+"*.jpg"))
	#im1 = str(images[0])
	#im2 = str(images[1])
	img = cv2.imread(im1,1)
	img1 = cv2.imread(im2,1)
	return img, img1
 

def resize_img(resize_factor,img):

	h, w = img.shape[:2]
	h = int(h/resize_factor)
	w = int(w/resize_factor)
	rimg = cv2.resize(img,(w,h))
	#cv2.imwrite('/tmp/rimg.png',rimg)
	#alpha = 2.5 # Contrast control (1.0-3.0)
	#beta = 50 # Brightness control (0-100)
	#rimg = cv2.convertScaleAbs(rimg_, alpha=alpha, beta=beta)
	#cv2.imshow('adjusted', rimg)
	#cv2.waitKey()

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
	

def mask_to_img(img,img1,x,y,r):
	
	h, w = img.shape[:2]
	circle_img = np.zeros((h,w), np.uint8)
	cv2.circle(circle_img,(x,y),r,1,thickness=-1)
	
	img[circle_img==0] = [255,255,255]
	img1[circle_img==0] = [255,255,255]
	img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	img_gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
	mean = cv2.mean(img_gray, mask=circle_img)[0]
	mean1 = cv2.mean(img_gray1, mask=circle_img)[0]
	if mean1 < mean1 :
		first = img1
		second = img
	else :
		first = img
		second = img1
	cv2.imwrite('/tmp/circle.png',first)
	cv2.imwrite('/tmp/circle1.png',second)
	print("mean =" + str(mean))
	print("mean1 =" + str(mean1))


def combine_img(x,y,r,new_path):
	
	img1 = cv2.imread('/tmp/circle.png')
	img2 = cv2.imread('/tmp/circle1.png')
	crop_img1 = img1[y-r:y+r, x-r:x+r]
	crop_img2 = img2[y-r:y+r, x-r:x+r]
	#cv2.imshow("cropped", crop_img)
	#cv2.waitKey(0)
	vis = np.concatenate((crop_img1, crop_img2), axis=1)
	cv2.imwrite(new_path+'combine.tiff', vis)



## PROGRAMMA

def run_combine(new_path):
	(img,img1) = load(new_path) #load photo thinsiction
	(w, rimg) = resize_img(RESIZE_FACTOR,img) #resize photo thinsiction
	x_r, y_r, r_r = find_circle(w, rimg) #find in resise photo thinsection coordinates centre and radius circle
	x, y, r = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR) #convert coordinates centre and radius circle to initial size photo
	mask_to_img(img,img1,x, y, r) #put mask to thinsection photo
	combine_img(x,y,r,new_path) #combine two photo (-,+) thinsection


run_combine(new_path)



import cv2
import numpy as np
import sys
import glob
import os

RESIZE_FACTOR=10
path_to_images = "/tmp/petro/1/1/x5/3/"


def load(path_to_images):
	""" Загрузка двух фотографий шлифа """
	images = glob.glob(os.path.join(path_to_images,"*.jpg"))
	img1 = cv2.imread(images[0],1)
	img2 = cv2.imread(images[1],1)
	return img1, img2
 

def resize_img(resize_factor,img):
	"""  Изменение размера фотографии  """
	h, w = img.shape[:2]
	h = int(h/resize_factor)
	w = int(w/resize_factor)
	rimg = cv2.resize(img,(w,h))
	return rimg


def find_circle(img):
	""" Поиск круга на фотографии, возвращает координаты центра и радиус первого найденного круга """
	gimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	(_, w) = gimg.shape[:2]
	(_, bw) = cv2.threshold(gimg, 2, 255, cv2.THRESH_BINARY)
	circles = cv2.HoughCircles(
							   bw,
							   cv2.HOUGH_GRADIENT,
							   1,
							   10,
							   param1=1,
							   param2=10,
							   minRadius=int(0.48*w),
							   maxRadius=int(.5*w)
							   )
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
	return img, img1


def crop(x,y,r,img1,img2):
	w, h = img1.shape[:2]
	y0 = y-r
	y1 = y+r
	x0 = x-r
	x1 = x+r
	if y0 < 0:
		y0 = 0
	if x0 < 0:
		x0 = 0
	if y1>(w-1):
		y1 = w-1
	if x1>(h-1):
		x1 = h-1
	crop_img1 = img1[y0:y1, x0:x1]
	crop_img2 = img2[y0:y1, x0:x1]
	return crop_img1, crop_img2

def combine_img(img1,img2,path_to_images):
	vis = np.concatenate((img1, img2), axis=1)
	cv2.imwrite(os.path.join(path_to_images,'combine.tiff'), vis)


def montage(path_to_images):
	(img1,img2) = load(path_to_images) #load photo thinsiction
	rimg = resize_img(RESIZE_FACTOR,img1) #resize photo thinsiction
	x_r, y_r, r_r = find_circle(rimg) #find in resise photo thinsection coordinates centre and radius circle
	x, y, r = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR) #convert coordinates centre and radius circle to initial size photo
	img1_mask, img2_mask  = mask_to_img(img1,img2,x, y, r) #put mask to thinsection photo
	crop_img1, crop_img2 = crop(x,y,r,img1_mask, img2_mask) 
	combine_img(crop_img1, crop_img2, path_to_images) #combine two photo (-,+) thinsection


if __name__== "__main__":
	montage(path_to_images)


import cv2
import numpy as np
import sys
import glob
import os
from PIL import Image, ImageFont, ImageDraw
import subprocess

RESIZE_FACTOR=10
path_to_images = "/tmp/petro/1/2/x5/1/"


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
							   minRadius=int(0.18*w),
							   maxRadius=int(.8*w)
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
	

def add_scale_bar_nicoli(path_to_images):
		
	image = os.path.join(path_to_images,'combine.tiff')
	img =  cv2.imread(image)
	w, h = img.shape[:2]
	
	start_point = (0, 0) #(int(h*1), int(w*1))
	end_point = (int(h*0.05), int(w*0.1)) #(int(h*(0.92)), int(w*0.89))
	color = (0, 0, 0)
	thickness = -1
	img_draw = cv2.rectangle(img, start_point, end_point, color, thickness)
	
	start_point = (h, 0) #(int(h*1), int(w*1))
	end_point = (int(h-h*0.05), int(w*0.1)) #(int(h*(0.92)), int(w*0.89))
	color = (0, 0, 0)
	thickness = -1
	img_draw = cv2.rectangle(img, start_point, end_point, color, thickness)
	
	
	start_point = (int(h/2-h*0.05), int(0)) #(int(h*1), int(w*1))
	end_point = (int(h/2+h*0.05), int(w*0.05)) #(int(h*(0.92)), int(w*0.89))
	color = (0, 0, 0)
	thickness = -1
	img_draw = cv2.rectangle(img, start_point, end_point, color, thickness)
	
	
	BLACK = (255,255,255)
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_size = 3
	font_color = BLACK
	font_thickness = 3
	
	text = ' (-) '
	x,y = int(h*0.0005), int(w*0.05)
	print(x,y)
	img_text = cv2.putText(img_draw, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
	
	text = '0.5 mm'
	x,y = int(h/2-h*0.04), int(0+w*0.03)
	print(x,y)
	img_text1 = cv2.putText(img_text, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
	
	text = ' (+) '
	x,y = int(h-h*0.05), int(w*0.05)
	img_text2 = cv2.putText(img_text1, text, (x,y), font, font_size, font_color, font_thickness, cv2.LINE_AA)
	
	path_montage = os.path.join(path_to_images,'montage.tiff')
	path_montage_jpg = os.path.join(path_to_images,'montage.jpg')
	cv2.imwrite(path_montage, img_text2)
	
	save_montage = f"convert -resize 20% {path_montage} {path_montage_jpg}"
	subprocess.Popen(save_montage,shell=True)
	
def montage(path_to_images):
	(img1,img2) = load(path_to_images) #load photo thinsiction
	rimg = resize_img(RESIZE_FACTOR,img1) #resize photo thinsiction
	x_r, y_r, r_r = find_circle(rimg) #find in resise photo thinsection coordinates centre and radius circle
	x, y, r = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR) #convert coordinates centre and radius circle to initial size photo
	img1_mask, img2_mask  = mask_to_img(img1,img2,x, y, r) #put mask to thinsection photo
	crop_img1, crop_img2 = crop(x,y,r,img1_mask, img2_mask) 
	combine_img(crop_img1, crop_img2, path_to_images) #combine two photo (-,+) thinsection
	add_scale_bar_nicoli(path_to_images)


if __name__== "__main__":
	montage(path_to_images)


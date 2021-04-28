import cv2
import numpy as np
import sys
import glob
import os
from PIL import Image, ImageFont, ImageDraw
import subprocess
import time

RESIZE_FACTOR=10


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


def combine_img(img1,img2,path_to_images):
	""" Обьединяет две фотографии"""
	resize_factor = 0.5
	rimg1 = resize_img(resize_factor,img1)
	rimg2 = resize_img(resize_factor,img2)
	combine_image = np.concatenate((rimg1, rimg2), axis=1)
	return combine_image

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
							   maxRadius=int(0.8*w)
							   )
	circle = circles[0,0]
	x, y, r = int(circle[0]), int(circle[1]), int(circle[2]*0.99)
	return x, y, r

def find_circle_(img):
	""" Поиск круга на фотографии, возвращает координаты центра и радиус первого найденного круга """
	hh, ww = img.shape[:2]
	
	# threshold on white
	# Define lower and uppper limits
	lower = np.array([100, 100, 100])
	upper = np.array([255, 255, 255])
	
	# Create mask to only select black
	thresh = cv2.inRange(img, lower, upper)
	
	# get convex hull
	points = np.column_stack(np.where(thresh.transpose() > 0))
	hullpts = cv2.convexHull(points)
	((centx,centy), (width,height), angle) = cv2.fitEllipse(hullpts)
	
	# draw convex hull on image
	hull = img.copy()
	
	# create new circle mask from ellipse
	circle = np.zeros((hh,ww), dtype=np.uint8)
	x = int(centx)
	y = int(centy)
	r = int((width+height)/4)
	cv2.circle(hull, (x,y), r, (0,0,255), 2)
	return x, y, r
	
	

def initial_coordinates_radius(x_r, y_r, r_r, resize_factor):
	""" Возвращает истинный значения координат центра и радиуса круга"""
	x = x_r*resize_factor
	y = y_r*resize_factor
	r = r_r*resize_factor
	return x, y, r
	

def mask_to_img(img,img1,x,y,r):
	""" Заменяет черные пиксели по краям фото на белый цвет """
	h, w = img.shape[:2]
	circle_img = np.zeros((h,w), np.uint8)
	cv2.circle(circle_img,(x,y),r,1,thickness=-1)
	img[circle_img==0] = [255,255,255]
	img1[circle_img==0] = [255,255,255]
	return img, img1


def crop(x,y,r,img1,img2):
	""" Обрезает фотографии"""
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


def add_text_to_image(img, text, x,y, font = cv2.FONT_HERSHEY_SIMPLEX, size = 3, color = (255,255,255), thickness= 3, line = cv2.LINE_AA):
	""" Пишет на фото"""
	cv2.putText(img,
		 	   text,
			   (x,y),
			   font,
			   size,
			   color,
			   thickness,
			   line)


def add_draw_to_image(img, start_point, end_point, color= (0, 0, 0), thickness = -1):
	""" Рисует на фото"""
	img_draw = cv2.rectangle(img,
							 start_point,
							 end_point,
							 color,
							 thickness)
	

def convert_px_to_mm(img,diametr_pole):
	""" Пересчет координат из px в mm"""
	w, h = img.shape[:2]
	parts = 8
	h_mm = diametr_pole*2
	h_parts = h/parts
	h_mm_parts = h_mm/parts
	start_scale_h = int(3.5 * h_parts)
	end_scale_h = int(4.5 * h_parts)
	start_scale_w = int(0)
	end_scale_w = int(0.2* h_parts)
	value_scale_bar_mm = str(h_mm/h*h_parts)
	start = (start_scale_h,start_scale_w)
	end = (end_scale_h, end_scale_w)
	return  w, h, start, end, value_scale_bar_mm
	
def read_config_lense():
	# открываем файл, обязательно указывая режим и кодировку
	with open(r'config', mode='r', encoding='utf-8') as fl:
	# считываем содержимое файлам одним списком стром
		onstring = fl.readlines()
	
	lens = {}
	
	for i in onstring:
		k, v = i.split(',')
		v = v.strip()
		v = float(v)
		# добавляем в словарь соответствующие пары ключ:значение
		lens[k] =  v
	return lens

def add_scale_bar_nicoli(path_to_images,combine_image,lense_name):
	""" добавляет подписи николей и масштабную линейку на фото
		сохраняет фото в .jpg (уменьшеном) формате"""
	img =  combine_image
	lens = read_config_lense()
	diametr_pole = lens.get(lense_name)
	w, h, start, end, value_scale_bar_mm = convert_px_to_mm(img,diametr_pole)
	add_draw_to_image(img, start_point = start, end_point = end) 
	add_draw_to_image(img, start_point = (h, 0), end_point = (int(h-h*0.05), int(w*0.1))) 
	add_draw_to_image(img, start_point = (0, 0), end_point = (int(h*0.05), int(w*0.1)))
	size_text = 6
	thickness_text = 10
	add_text_to_image(img, text = ' (||) ', size = size_text, thickness = thickness_text, x = int(h*0.0005) ,y = int(w*0.05) )
	add_text_to_image(img, text = ' (+) ', size = size_text,  thickness = thickness_text, x = int(h-h*0.05) ,y = int(w*0.05))
	add_text_to_image(img, text = value_scale_bar_mm+' mm', size = size_text, thickness = thickness_text, x = int(h/2-h*0.04) ,y = int(0+w*0.035))
	path_montage_jpg = os.path.join(path_to_images,'montage.jpeg')
	cv2.imwrite(path_montage_jpg, img)
	save_montage = f"convert -resize 15% {path_montage_jpg} {path_montage_jpg}"
	subprocess.Popen(save_montage,shell=True)


def show_img_montage(path_to_images):
	image = cv2.imread(os.path.join(path_to_images,'montage.jpeg'))
	cv2.imshow('montage', image)
	cv2.waitKey()
	cv2.destroyAllWindows() 

def montage(path_to_images, lense_name):
	""" обьединяет фото с разными николями """
	print("диаметр поле", lense_name)
	(img1,img2) = load(path_to_images) #load photo thinsiction
	rimg1 = resize_img(RESIZE_FACTOR,img1) #resize photo thinsiction
	rimg2 = resize_img(RESIZE_FACTOR,img2)
	x_r, y_r, r_r = find_circle_(rimg1)
	try:
		x_r, y_r, r_r = find_circle_(rimg1) #find in resise photo thinsection coordinates centre and radius circle
	except TypeError:
		try:
			x_r, y_r, r_r = find_circle_(rimg2)
		except TypeError:
			print("Ошибка! Круг не найдет")
			return

	x, y, r = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR) #convert coordinates centre and radius circle to initial size photo
	img1_mask, img2_mask  = mask_to_img(img1,img2,x, y, r) #put mask to thinsection photo
	crop_img1, crop_img2 = crop(x,y,r,img1_mask, img2_mask) 
	combine_image = combine_img(crop_img1, crop_img2, path_to_images) #combine two photo (-,+) thinsection
	add_scale_bar_nicoli(path_to_images, combine_image,lense_name)
	time.sleep(5)
	show_img_montage(path_to_images)


if __name__== "__main__":
	montage(path_to_images,diametr_pole)


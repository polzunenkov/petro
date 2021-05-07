import cv2
import numpy as np
import sys
import glob
import os
from PIL import Image, ImageFont, ImageDraw
import subprocess
import time

RESIZE_FACTOR=10

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


def load(path_to_images):
	''' Загрузка двух фотографий шлифа '''
	all_images_in_directory = os.path.join(path_to_images,"*.jpg")
	images = sorted(glob.glob(all_images_in_directory))
	if len(images)==2:
		img1 = cv2.imread(images[0],1)
		img2 = cv2.imread(images[1],1)
	else:
		img1 = cv2.imread(images[0],1)
		img2 = cv2.imread(images[0],1)
	return img1, img2
 

def resize_img(resize_factor,img):
	'''  Изменение размера фотографии  '''
	h, w = img.shape[:2]
	h = int(h/resize_factor)
	w = int(w/resize_factor)
	rimg = cv2.resize(img,(w,h))
	return rimg


def combine_img(img1,img2,path_to_images,resize_f = 3):
	''' Обьединяет две фотографии'''
	rimg1 = resize_img(resize_f,img1)
	rimg2 = resize_img(resize_f,img2)
	combine_image = np.concatenate((rimg1, rimg2), axis=1)
	
	return combine_image


def find_circle(img):
	''' Поиск круга на фотографии, возвращает координаты центра и радиус первого найденного круга '''
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
	''' Возвращает истинный значения координат центра и радиуса круга'''
	x = x_r*resize_factor
	y = y_r*resize_factor
	r = r_r*resize_factor
	return x, y, r
	

def mask_to_img(img,img1,x,y,r):
	''' Заменяет черные пиксели по краям фото на белый цвет '''
	h, w = img.shape[:2]
	circle_img = np.zeros((h,w), np.uint8)
	cv2.circle(circle_img,(x,y),r,1,thickness=-1)
	img[circle_img==0] = [255,255,255]
	img1[circle_img==0] = [255,255,255]
	return img, img1


def crop(x,y,r,img1,img2):
	''' Обрезает фотографии'''
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
	
	
def crop_square(x,y,r,img1,img2):
	''' Обрезает фотографии'''
	w, h = img1.shape[:2]
	a = r*(2**0.5) # радиус * на корень из 2 получаем длинну стороны а вписанного квадрата 
	r = int(a/2) # к цетру прибавляем 1\2 стороны а плучаем границы вписанного квадрата, далее обрезаем изображение по квадрату
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
	''' Пишет на фото'''
	cv2.putText(img,
		 	   text,
			   (x,y),
			   font,
			   size,
			   color,
			   thickness,
			   line)


def add_draw_to_image(img, start_point, end_point, color= (0, 0, 0), thickness = -1):
	''' Рисует на фото'''
	img_draw = cv2.rectangle(img,
							 start_point,
							 end_point,
							 color,
							 thickness)
	

def convert_px_to_mm(img,diametr_pole,one_images = True ,st_h = 0, ed_h = 1, st_w = 0, ed_w = 0.08):
	''' Пересчет координат из px в mm'''
	w, h = img.shape[:2]
	print('d = ',diametr_pole)
	
	if one_images:
		D = diametr_pole
		storona_a = (D/2)*(2**0.5)
	else:
		D = diametr_pole*2
		storona_a = D
		
	print('D = ',storona_a)
	pix_mm = storona_a / h
	
	start_h = st_h * h
	end_h = ed_h * h
	start_w = st_w * w
	end_w = ed_w * w
	bar_pix = end_h - start_h
	value_bar_mm = str(round(pix_mm*bar_pix,2)) + ' mm' 
	start = (int(start_h),int(start_w))
	end = (int(end_h), int(end_w))
	
	return  w, h, start, end, value_bar_mm
	

def add_scale_bar_nicoli(combine_image,lense_name):
	''' добавляет подписи николей и масштабную линейку на фото
		сохраняет фото в .jpg (уменьшеном) формате'''
	img =  combine_image
	lens = read_config_lense()
	diametr_pole = lens.get(lense_name)
	w, h, start, end, value_scale_bar_mm = convert_px_to_mm(img,diametr_pole,one_images = False, st_h = 0.435, ed_h = 0.56, st_w = 0, ed_w = 0.04)
	add_draw_to_image(img, start_point = start, end_point = end) 
	add_draw_to_image(img, start_point = (h, 0), end_point = (int(h-h*0.05), int(w*0.1))) 
	add_draw_to_image(img, start_point = (0, 0), end_point = (int(h*0.05), int(w*0.1)))
	koef_size = 6/11680
	size_text = h*koef_size
	koef_thickness_text = 18/6
	thickness_text = int(size_text*koef_thickness_text)
	add_text_to_image(img, text = ' (||) ', size = size_text, thickness = thickness_text, x = int(h*0.0005) ,y = int(w*0.05) )
	add_text_to_image(img, text = ' (+) ', size = size_text,  thickness = thickness_text, x = int(h-h*0.05) ,y = int(w*0.05))
	add_text_to_image(img, text = value_scale_bar_mm, size = size_text, thickness = thickness_text, x = int(h/2-h*0.04) ,y = int(0+w*0.035))
	return  img


def save_img(path_to_images, image, name):
	path_montage_jpg = os.path.join(path_to_images,name)
	cv2.imwrite(path_montage_jpg, image)
	

def add_scale_bar(combine_image,lense_name):
	''' добавляет подписи николей и масштабную линейку на фото
		сохраняет фото в .jpg (уменьшеном) формате'''
	img =  combine_image
	lens = read_config_lense()
	diametr_pole = lens.get(lense_name)
	w, h, start, end, value_scale_bar_mm = convert_px_to_mm(img,diametr_pole, one_images = True, st_h = 0.8025, ed_h = 0.98, st_w = 0.03, ed_w = 0.07)
	add_draw_to_image(img, start_point = start, end_point = end, color = (255,255,255), thickness = -1)
	add_draw_to_image(img, start_point = start, end_point = end,color = (0,0,0), thickness = 5)
	koef_size = 6/11680
	size_text = h*koef_size*1.2
	koef_thickness_text = 18/6
	thickness_text = int(size_text*koef_thickness_text)*2
	add_text_to_image(img, text = value_scale_bar_mm, size = size_text*1.5, color = (0,0,0), thickness = thickness_text, x = int(h*0.83) ,y = int(w*0.058))
	img = resize_img(3, img)
	return  img

def show_img_montage(path_to_images, name):
	'''показывает изображение'''
	image = cv2.imread(os.path.join(path_to_images,name))
	cv2.imshow(str(name), image)
	cv2.waitKey()
	cv2.destroyAllWindows() 

def load_resize_find_circle(path_to_images, lense_name):
	''' возвращает исходные изображения img1, img2 ,
	перемасштабированные изображения rimg1, rimg2,
	координаты и радиус круглой маски '''
	(img1,img2) = load(path_to_images) #load photo thinsiction
	
	rimg1 = resize_img(RESIZE_FACTOR,img1) #resize photo thinsiction
	rimg2 = resize_img(RESIZE_FACTOR,img2)
	
	(x_r, y_r, r_r) = find_circle(rimg1)
	(x, y, r) = initial_coordinates_radius(x_r, y_r, r_r, RESIZE_FACTOR) #convert coordinates centre and radius circle to initial size photo
	
	return img1, img2, rimg1, rimg2, x, y, r
	
def two_photo_circle(path_to_images, lense_name):
	'''формирует изображение в виде  двух кругов
	 с маштабной линейкой и квардратами по углам
	  со значками скрещенных и паралелбных николей '''
	(img1, img2, rimg1, rimg2, x, y, r) = load_resize_find_circle(path_to_images, lense_name)
	(img1_mask, img2_mask)  = mask_to_img(img1,img2,x, y, r) #put mask to thinsection photo
	(crop_img1, crop_img2) = crop(x,y,r,img1_mask, img2_mask) 
	combine_image = combine_img(crop_img1, crop_img2, path_to_images,resize_f = 3) #combine two photo (-,+) thinsection
	image_bar = add_scale_bar_nicoli(combine_image,lense_name)
	save_img(path_to_images, combine_image, 'two_photo_circle.jpeg')
	time.sleep(1)
	show_img_montage(path_to_images, 'two_photo_circle.jpeg')
	
	
def two_photo_square(path_to_images, lense_name):
	'''формирует изображение в виде  двух квадратов
	с маштабными линейками с левой верхней стороны каждого квадрата'''
	(img1, img2, rimg1, rimg2, x, y, r) = load_resize_find_circle(path_to_images, lense_name)
	(crop_square_img1, crop_square_img2) =crop_square(x,y,r,img1,img2)
	image_bar1 = add_scale_bar(crop_square_img1,lense_name)
	image_bar2 = add_scale_bar(crop_square_img2,lense_name)
	h, w = image_bar1.shape[:2]
	idm = image_bar1.copy()[0:h,0:int(w*0.05)]
	zeros = np.zeros((h,int(w*0.05)), np.uint8)
	idm[zeros==0] = [255,255,255]
	combine_image1 = np.concatenate((image_bar1, idm, image_bar2), axis=1)
	#combine_image1 = combine_img(image_bar1, image_bar2, path_to_images,resize_f = 1) #combine two photo (-,+) thinsection
	save_img(path_to_images, combine_image1, 'two_photo_square.jpeg')
	time.sleep(1)
	show_img_montage(path_to_images, 'two_photo_square.jpeg')
	
def one_photo_circle(path_to_images, lense_name):
	'''формирует изображение в виде  круга 
	с маштабной линейкой с левой верхней стороны'''
	(img1, _, rimg1, _, x, y, r) = load_resize_find_circle(path_to_images, lense_name)
	(img1_mask, _) = mask_to_img(img1,img1,x, y, r) #put mask to thinsection photo
	(crop_img1, _) = crop(x,y,r,img1_mask, img1_mask) 
	image_bar = add_scale_bar(crop_img1,lense_name)
	save_img(path_to_images, image_bar, 'one_photo_circle.jpeg')
	time.sleep(1)
	show_img_montage(path_to_images, 'one_photo_circle.jpeg')

def one_photo_square(path_to_images, lense_name):
	'''формирует изображение в виде  квадрата 
	с маштабной линейкой с левой верхней стороны'''
	(img1, _, rimg1, _, x, y, r) = load_resize_find_circle(path_to_images, lense_name)
	(crop_square_img1, _) =crop_square(x,y,r,img1,img1)
	image_bar1 = add_scale_bar(crop_square_img1,lense_name)
	save_img(path_to_images, image_bar1, 'one_photo_square.jpeg')
	time.sleep(1)
	show_img_montage(path_to_images, 'one_photo_square.jpeg')

if __name__== "__main__":
	two_photo_circle(path_to_images,diametr_pole)


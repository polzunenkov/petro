import cv2
import numpy as np
import sys
import glob
import os
import configparser
import subprocess
import time
import matplotlib.pyplot as plt
from tkinter import filedialog as fd
RESIZE_FACTOR = 10
#from settings import folder_img


def create_config_(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Lense")
    config.set("Lense", "x5", "4")
    config.set("Lense", "x10", "2")
    config.set("Lense", "x20", "1")
    config.set("Lense", "x40", "0.5")
    config.set("Lense", "x60", "0.25")

    with open(path, "w") as config_file:
        config.write(config_file)


def create_config(
    path,
    name_lens1,
    name_lens2,
    name_lens3,
    name_lens4,
    name_lens5,
    d_lens1,
    d_lens2,
    d_lens3,
    d_lens4,
    d_lens5,
):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Lense")
    config.set("Lense", name_lens1.get(), d_lens1.get())
    config.set("Lense", name_lens2.get(), d_lens2.get())
    config.set("Lense", name_lens3.get(), d_lens3.get())
    config.set("Lense", name_lens4.get(), d_lens4.get())
    config.set("Lense", name_lens5.get(), d_lens5.get())

    with open(path, "w") as config_file:
        config.write(config_file)


def get_config(
    path,
    name_lens1,
    name_lens2,
    name_lens3,
    name_lens4,
    name_lens5,
    d_lens1,
    d_lens2,
    d_lens3,
    d_lens4,
    d_lens5,
):
    """
    Returns the config object
    """
    # if not os.path.exists(path):
    create_config(
        path,
        name_lens1,
        name_lens2,
        name_lens3,
        name_lens4,
        name_lens5,
        d_lens1,
        d_lens2,
        d_lens3,
        d_lens4,
        d_lens5,
    )

    config = configparser.ConfigParser()
    config.read(path)
    return config


def get_setting(path, section, setting):
    """
    Print out a setting
    """
    config = configparser.ConfigParser()
    config.read(path)
    value = config.get(section, setting)
    msg = "{section} {setting} is {value}".format(
        section=section, setting=setting, value=value
    )

    print(msg)
    return value


def update_setting(path, section, setting, value):
    """
    Update a setting
    """
    config = get_config(path)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def delete_setting(path, section, setting):
    """
    Delete a setting
    """
    config = get_config(path)
    config.remove_option(section, setting)
    with open(path, "w") as config_file:
        config.write(config_file)


def lens_():
    path = "settings.ini"
    if not os.path.exists(path):
        create_config_(path)

    config = configparser.ConfigParser()
    config.read(path)
    lens = list(config["Lense"])
    return lens


    
def find_circle(img):
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
    ((centx, centy), (width, height), angle) = cv2.fitEllipse(hullpts)

    # draw convex hull on image
    hull = img.copy()

    # create new circle mask from ellipse
    circle = np.zeros((hh, ww), dtype=np.uint8)
    x = int(centx)
    y = int(centy)
    r = int((width + height) / 4)
    cv2.circle(hull, (x, y), r, (0, 0, 255), 2)
    return x, y, r


def initial_coordinates_radius(x_r, y_r, r_r, resize_factor):
    """ Возвращает истинный значения координат центра и радиуса круга"""
    x = x_r * resize_factor
    y = y_r * resize_factor
    r = r_r * resize_factor
    return x, y, r


def mask_to_img(img, img1, x, y, r):
    """ Заменяет черные пиксели по краям фото на белый цвет """
    h, w = img.shape[:2]
    circle_img = np.zeros((h, w), np.uint8)
    cv2.circle(circle_img, (x, y), r, 1, thickness=-1)
    img[circle_img == 0] = [255, 255, 255]
    img1[circle_img == 0] = [255, 255, 255]
    return img, img1


def crop(x, y, r, img1, img2):
    """ Обрезает фотографии"""
    w, h = img1.shape[:2]
    y0 = y - r
    y1 = y + r
    x0 = x - r
    x1 = x + r
    if y0 < 0:
        y0 = 0
    if x0 < 0:
        x0 = 0
    if y1 > (w - 1):
        y1 = w - 1
    if x1 > (h - 1):
        x1 = h - 1
    crop_img1 = img1[y0:y1, x0:x1]
    crop_img2 = img2[y0:y1, x0:x1]
    return crop_img1, crop_img2


def crop_square(x, y, r, img1, img2):
    """ Обрезает фотографии"""
    w, h = img1.shape[:2]
    a = r * (
        2 ** 0.5
    )  # радиус * на корень из 2 получаем длинну стороны а вписанного квадрата
    r = int(
        a / 2
    )  # к цетру прибавляем 1\2 стороны а плучаем границы вписанного квадрата, далее обрезаем изображение по квадрату
    y0 = y - r
    y1 = y + r
    x0 = x - r
    x1 = x + r
    if y0 < 0:
        y0 = 0
    if x0 < 0:
        x0 = 0
    if y1 > (w - 1):
        y1 = w - 1
    if x1 > (h - 1):
        x1 = h - 1
    crop_img1 = img1[y0:y1, x0:x1]
    crop_img2 = img2[y0:y1, x0:x1]
    return crop_img1, crop_img2


def add_text_to_image(
    img,
    text,
    x,
    y,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    size=3,
    color=(255, 255, 255),
    thickness=3,
    line=cv2.LINE_AA,
):
    """ Пишет на фото"""
    cv2.putText(img, text, (x, y), font, size, color, thickness, line)


def add_draw_to_image(img, start_point, end_point, color=(0, 0, 0), thickness=-1):
    """ Рисует на фото"""
    img_draw = cv2.rectangle(img, start_point, end_point, color, thickness)


def convert_px_to_mm(
    img, diametr_pole, one_images=True, st_h=0, ed_h=1, st_w=0, ed_w=0.08
):
    """ Пересчет координат из px в mm"""
    w, h = img.shape[:2]
    print("d = ", diametr_pole)

    if one_images:
        D = float(diametr_pole)
        storona_a = (D / 2) * (2 ** 0.5)
    else:
        D = float(diametr_pole) * 2
        storona_a = D

    print("D = ", storona_a)
    pix_mm = storona_a / h

    start_h = st_h * h
    end_h = ed_h * h
    start_w = st_w * w
    end_w = ed_w * w
    bar_pix = end_h - start_h
    value_bar_mm = str(round(pix_mm * bar_pix, 1)) + " mm"
    start = (int(start_h), int(start_w))
    end = (int(end_h), int(end_w))

    return w, h, start, end, value_bar_mm


def add_scale_bar_nicoli(combine_image, lense_name, one_images_=False):
    """ добавляет подписи николей и масштабную линейку на фото
		сохраняет фото в .jpg (уменьшеном) формате"""
    img = combine_image
    lens = lens_()
    diametr_pole = float(get_setting("settings.ini", "Lense", lense_name))
    print(diametr_pole)
    
    if one_images_:
        delta_h = 0.1
        delta_w = 0.1
        ed_w_ = 0.02
        k_size = 6.5
        k_w_ = 2
    else:
        delta_h = 0.05
        delta_w = 0.1
        ed_w_ = 0.04
        k_size = 5.2
        k_w_ = 1
        
    w, h, start, end, value_scale_bar_mm = convert_px_to_mm(
        img, diametr_pole, one_images=one_images_, st_h=0.435, ed_h=0.56, st_w=0, ed_w=ed_w_
    )
    add_draw_to_image(img,
        start_point=start, 
        end_point=end
    )
    add_draw_to_image(
        img, 
        start_point=(h, 0), 
        end_point=(int(h - h * delta_h), int(w * delta_w))
    )
    add_draw_to_image(
        img,
        start_point=(0, 0),
        end_point=(int(h * delta_h), int(w * delta_w))
    )
    
    koef_size = k_size / 11680
    size_text = h * koef_size
    koef_thickness_text = 18 / k_size
    thickness_text = int(size_text * koef_thickness_text)
    
    add_text_to_image(
        img,
        text=" (||) ",
        size=size_text*(k_size/4),
        thickness=thickness_text,
        x=int(h * 0.0005),
        y=int(w * 0.05),
    )
    add_text_to_image(
        img,
        text=" (+) ",
        size=size_text*(k_size/4),
        thickness=thickness_text,
        x=int(h - h * 0.05),
        y=int(w * 0.05),
    )
    add_text_to_image(
        img,
        text=value_scale_bar_mm,
        size=size_text,
        thickness=thickness_text,
        x=int(h / 2 - h * 0.04),
        y=int(0 + w * (ed_w_-0.008/k_w_)),
    )
    return img


def save_img(path_to_images, image, name):
    path_montage_jpg = os.path.join(path_to_images, name)
    cv2.imwrite(path_montage_jpg, image)




def show_img_montage(path_to_images, name):
    """показывает изображение"""
    image = cv2.imread(os.path.join(path_to_images, name))
    cv2.imshow(str(name), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class LoadImg:
    """ возвращает исходные изображения img1, img2 ,
	перемасштабированные изображения rimg1, rimg2,
	координаты и радиус круглой маски """
 
    def __init__(self, path_to_images, lense_name, folder_img):
        """Constructor"""
        self.path_to_images=path_to_images
        self.lense_name=lense_name
        self.folder_img=folder_img
        (self.img1, self.img2, self.sample1, self.sample2, self.lens_name1, self.lens_name2) = self.load()
        self.rimg1 = self.calculate_resize_img(RESIZE_FACTOR,self.img1)
        self.rimg2 = self.calculate_resize_img(RESIZE_FACTOR,self.img2)
        (self.x_r, self.y_r, self.r_r) = find_circle(self.rimg1)
        (self.x, self.y, self.r) = initial_coordinates_radius(
        self.x_r, self.y_r, self.r_r, RESIZE_FACTOR)
        
               
    def load(self):
        """Загрузка двух фотографий шлифа"""
    
        if not self.folder_img:
            type_img="*.jpg"
            all_images_in_directory = os.path.join(self.path_to_images, type_img)
            images = sorted(glob.glob(all_images_in_directory))
            sample1=images[0]
            sample2=images[1]
            lens_name1=sample1.split("/")[-3]
            lens_name2=sample2.split("/")[-3]
        
            
        else:
            type_img="*.jpeg"
            print("выбор файлов на компьютере")
            
            for i in range(2):
                if i==0:
                    foto1 = fd.askopenfilename()
                    os.system('cp '+ foto1 + ' '+self.path_to_images +'/fig1.jpeg')
                else:
                    foto2 = fd.askopenfilename()
                    os.system('cp '+ foto2 +' '+self.path_to_images +'/fig2.jpeg')
                    
                    all_images_in_directory = os.path.join(self.path_to_images, type_img)
                    images = sorted(glob.glob(all_images_in_directory))
                    print("Проверка колво изображений:", images)
                    sample1=foto1.split("/")[-4]
                    sample2=foto2.split("/")[-4]
                    lens_name1=foto1.split("/")[-3]
                    lens_name2=foto2.split("/")[-3]
                    
                                    
        if len(images) > 1:
            img1 = cv2.imread(images[0], 1)
            img2 = cv2.imread(images[1], 1)
        else:
            img1 = cv2.imread(images[0], 1)
            img2 = cv2.imread(images[0], 1)
        return img1, img2, sample1, sample2, lens_name1, lens_name2

    
    def combine_img(self, crop_img1, crop_img2, resize_f=3):
        """ Обьединяет две фотографии"""
        rimg1 = self.calculate_resize_img(resize_f, crop_img1)
        rimg2 = self.calculate_resize_img(resize_f, crop_img2)
        combine_image = np.concatenate((rimg1, rimg2), axis=1)

        return combine_image
    
    def calculate_resize_img(self, resize_factor, img):
        """  Изменение размера фотографии  """
        h, w = img.shape[:2]
        h = int(h / resize_factor)
        w = int(w / resize_factor)
        return cv2.resize(img, (w, h))
    
    def add_scale_bar(self, combine_image, lense_name, sample_name):
        """ добавляет подписи николей и масштабную линейку на фото
		    сохраняет фото в .jpg (уменьшеном) формате"""
        img = combine_image
        lens = lens_()
        diametr_pole = float(get_setting("settings.ini", "Lense", lense_name))
        w, h, start, end, value_scale_bar_mm = convert_px_to_mm(
            img, diametr_pole, one_images=True, st_h=0.8025, ed_h=0.98, st_w=0.93, ed_w=0.94,
        )
        add_draw_to_image(
            img, start_point=start, end_point=end, color=(0, 0, 0), thickness=-1
        )
        add_draw_to_image(
            img, start_point=start, end_point=end, color=(0, 0, 0), thickness=5
        )
        koef_size = 6 / 11680
        size_text = h * koef_size * 1.2
        koef_thickness_text = 18 / 6
        thickness_text = int(size_text * koef_thickness_text) * 2
        add_text_to_image(
            img,
            text=value_scale_bar_mm,
            size=size_text * 1.5,
            color=(0, 0, 0),
            thickness=thickness_text,
            x=int(h * 0.83),
            y=int(w * 0.98),
        )
        add_text_to_image(
            img,
            text=sample_name,
            size=size_text * 3.5,
            color=(0, 0, 0),
            thickness=thickness_text,
            x=int(h * 0.35),
            y=int(w * 0.97),
        )
        img = self.calculate_resize_img(3, img)
        
        return img
    
    def add_rectangle_trans(self, combine_image, lense_name):
    
        img = combine_image
        overlay = img.copy()
        lens = lens_()
        diametr_pole = float(get_setting("settings.ini", "Lense", lense_name))
        w, h, start, end, value_scale_bar_mm = convert_px_to_mm(
            img, diametr_pole, one_images=True, st_h=0.0, ed_h=1.0, st_w=0.9, ed_w=1.0,
        )
        add_draw_to_image(
            overlay, start_point=start, end_point=end, color=(255, 255, 255), thickness=-1
        )
        #add_draw_to_image(
        #   overlay, start_point=start, end_point=end, color=(0, 0, 0), thickness=5
        #)
        
        
        #x, y, w, h = 10, 10, 10, 10  # Rectangle parameters
        #cv2.rectangle(overlay, (start, end), (start+w, end+h), (0, 200, 0), -1)  # A filled rectangle
    
        alpha = 0.7  # Transparency factor.

        # Following line overlays transparent rectangle over the image
        image_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        return image_new
       

                        
    def add_scale_bar_(self, combine_image, lense_name):
        """ добавляет подписи николей и масштабную линейку на фото
		    сохраняет фото в .jpg (уменьшеном) формате"""
        img = combine_image
        lens = lens_()
        diametr_pole = float(get_setting("settings.ini", "Lense", lense_name))
        w, h, start, end, value_scale_bar_mm = convert_px_to_mm(
            img, diametr_pole, one_images=True, st_h=0.8025, ed_h=0.98, st_w=0.93, ed_w=0.97,
        )
        add_draw_to_image(
            img, start_point=start, end_point=end, color=(255, 255, 255), thickness=-1
        )
        add_draw_to_image(
            img, start_point=start, end_point=end, color=(0, 0, 0), thickness=5
        )
        koef_size = 6 / 11680
        size_text = h * koef_size * 1.2
        koef_thickness_text = 18 / 6
        thickness_text = int(size_text * koef_thickness_text) * 2
        add_text_to_image(
            img,
            text=value_scale_bar_mm,
            size=size_text * 1.5,
            color=(0, 0, 0),
            thickness=thickness_text,
            x=int(h * 0.83),
            y=int(w * 0.958),
        )
        img = self.calculate_resize_img(3, img)
        return img
    
    def two_photo_circle(self):
        """формирует изображение в виде  двух кругов
	     с маштабной линейкой и квардратами по углам
	      со значками скрещенных и паралелбных николей """
        
        (img1_mask, img2_mask) = mask_to_img(
            self.img1, self.img2, self.x, self.y, self.r
        )  # put mask to thinsection photo
        (crop_img1, crop_img2) = crop(self.x, self.y, self.r, img1_mask, img2_mask)
        combine_image = self.combine_img(
            crop_img1, crop_img2, resize_f=3
        )  # combine two photo (-,+) thinsection
        image_bar = add_scale_bar_nicoli(combine_image, self.lense_name)
        #print("save img to : "+path_to_images)
        save_img(self.path_to_images, combine_image, "two_photo_circle.jpeg")
        time.sleep(1)
        show_img_montage(self.path_to_images, "two_photo_circle.jpeg")
        

    def two_photo_square(self):
        """формирует изображение в виде  двух квадратов
	    с маштабными линейками с левой верхней стороны каждого квадрата"""
        
        (crop_square_img1, crop_square_img2) = crop_square(self.x, self.y, self.r, self.img1, self.img2)
        image_bar1 = self.add_rectangle_trans(crop_square_img1, self.lens_name1)
        image_bar2 = self.add_rectangle_trans(crop_square_img2, self.lens_name2)
        image_bar1_ = self.add_scale_bar(image_bar1, self.lens_name1, self.sample1)
        image_bar2_ = self.add_scale_bar(image_bar2, self.lens_name2, self.sample2)
        h, w = image_bar1_.shape[:2]
        idm = image_bar1_.copy()[0:h, 0 : int(w * 0.05)]
        zeros = np.zeros((h, int(w * 0.05)), np.uint8)
        idm[zeros == 0] = [255, 255, 255]
        combine_image1 = np.concatenate((image_bar1_, idm, image_bar2_), axis=1)
        # combine_image1 = combine_img(image_bar1, image_bar2, path_to_images,resize_f = 1) #combine two photo (-,+) thinsection
        save_img(self.path_to_images, combine_image1, "two_photo_square.jpeg")
        time.sleep(1)
        show_img_montage(self.path_to_images, "two_photo_square.jpeg")


    def one_photo_circle(self):
        """формирует изображение в виде  круга 
	    с маштабной линейкой с левой верхней стороны"""
        
        (img1_mask, _) = mask_to_img(self.img1, self.img1, self.x, self.y, self.r)  # put mask to thinsection photo
        (crop_img1, _) = crop(self.x, self.y, self.r, img1_mask, img1_mask)
        image_bar = self.add_scale_bar(crop_img1, self.lense_name)
        save_img(self.path_to_images, image_bar, "one_photo_circle.jpeg")
        time.sleep(1)
        show_img_montage(self.path_to_images, "one_photo_circle.jpeg")


    def one_photo_huf_circle(self):
        """формирует изображение в виде  круга 
	    с маштабной линейкой с левой верхней стороны"""
        
        (img1_mask, img2_mask) = mask_to_img(self.img1, self.img2, self.x, self.y, self.r)  # put mask to thinsection photo
        (crop_img1, crop_img2) = crop(self.x, self.y, self.r, img1_mask, img2_mask)
        h, w = crop_img1.shape[:2]
        
        crop_img1_huf = crop_img1[0:h,0:int(w/2)]
        crop_img2_huf = crop_img2[0:h,int(w/2):w]
        combine_image = self.combine_img(crop_img1_huf, crop_img2_huf, resize_f=3)
        image_bar = add_scale_bar_nicoli(combine_image, self.lense_name, one_images_=True)
        save_img(self.path_to_images, image_bar, "one_photo_huf_circle.jpeg")
        time.sleep(1)
        show_img_montage(self.path_to_images, "one_photo_huf_circle.jpeg")
        

    def one_photo_square(self):
        """формирует изображение в виде  квадрата 
	    с маштабной линейкой с левой верхней стороны"""
       
        (crop_square_img1, _) = crop_square(self.x, self.y, self.r, self.img1, self.img1)
        image_bar1 = self.add_scale_bar(crop_square_img1, self.lense_name)
        save_img(self.path_to_images, image_bar1, "one_photo_square.jpeg")
        time.sleep(1)
        show_img_montage(self.path_to_images, "one_photo_square.jpeg")
        
   


#def load_resize_find_circle(path_to_images, lense_name):
#    """ возвращает исходные изображения img1, img2 ,#
#	перемасштабированные изображения rimg1, rimg2,
#	координаты и радиус круглой маски """
#    #(img1, img2) = load(path_to_images)  # load photo thinsiction#
#
#    #rimg1 = resize_img(RESIZE_FACTOR, img1)  # resize photo thinsiction
#    #rimg2 = resize_img(RESIZE_FACTOR, img2)
#
#    (x_r, y_r, r_r) = find_circle(rimg1)
#    (x, y, r) = initial_coordinates_radius(
#        x_r, y_r, r_r, RESIZE_FACTOR
#    )  # convert coordinates centre and radius circle to initial size photo#
#
 #   return img1, img2, rimg1, rimg2, x, y, r



if __name__ == "__main__":
    print("EE")
    #two_photo_circle(path_to_images, diametr_pole)

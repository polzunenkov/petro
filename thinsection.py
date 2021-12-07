import subprocess
import os
import click
import cv2
import numpy as np
import sys
import glob
from script import LoadImg
from tkinter import filedialog as fd

def path_new_folder_img():
    path_to_image = fd.askdirectory()#initialdir=os.path.normpath("C://"), title="Example"
    #os.mkdir(path_to_image)
    return path_to_image

def _create_new_path(old_path, thinsection_name, lense, uch_name):
    """ Возвращает новое имя для фотографий шлифов с учетом имени thinsection_name
	"""
    path_new = os.path.join(old_path, thinsection_name, lense, uch_name)
    return path_new


def copy(numbers, new_path):
    """ копирует последние две, одну фотографии с телефона из дирректории Camera 
            -стандартной камеры Honor
	"""
	
    os.makedirs(new_path, exist_ok=True)
    command = "adb shell ls -lt /sdcard/DCIM/Camera/*.jpg"
    pipe = os.popen(command)
    img = pipe.read().split('\n')
    images1 = img[0].split(' ')[::-1][0]
    images2 = img[1].split(' ')[::-1][0]
    names=[images1,images2]
    for i in names[0:numbers]:
    	subprocess.run(["adb", "pull", i, new_path])	

def del_photo_folder(pattern):
    """ удаляет фотографии с телефона из дирректории Camera 
        -стандартной камеры Honor
	pattern - <common prefix>*.расширение файла- например jpg
	"""

    subprocess.run(["adb", "shell", "rm", "-f", f"/sdcard/DCIM/Camera/{pattern}"])


@click.command()
@click.option("--path", help="Path to destination folder", required=True)
@click.option(
    "--pattern", help="pattern to delete files from Camera folder", default="IMG_*.jpg"
)
@click.option("--thinsection_name", help="name for the thin section", default="thin01")
@click.option("--lense_name", help="name of the lesne used", default="x5")
@click.option("--uch_name", help="name of the uch used", default="1")
@click.option(
    "--two_circle",
    help="combine photo after change black by white from mask circle",
    is_flag=True,
    default=False,
)
@click.option(
    "--two_square",
    help="combine photo after change black by white from mask square",
    is_flag=True,
    default=False,
)
@click.option(
    "--one_circle",
    help="combine photo after change black by white from mask circle",
    is_flag=True,
    default=False,
)
@click.option(
    "--one_square",
    help="combine photo after change black by white from mask square",
    is_flag=True,
    default=False,
)
@click.option(
    "--do_not_remove_from_phone",
    help="remove phtos from phone folder ",
    is_flag=True,
    default=False,
)
def main(path, pattern, thinsection_name, lense_name, uch_name, two_circle, two_square, one_circle, one_square, do_not_remove_from_phone):
    ready(
        path=path,
        pattern=pattern,
        thinsection_name=thinsection_name,
        lense_name=lense_name,
        uch_name=uch_name,
        two_circle=two_circle,
        two_square=two_square,
        one_circle=one_circle,
        one_square=one_square,
        do_not_remove_from_phone=do_not_remove_from_phone,
        folder_img=folder_img,
    )


def ready(path, pattern, thinsection_name, lense_name, uch_name, two_circle=False, two_square=False, one_circle=False, one_square=False, do_not_remove_from_phone=False, folder_img=False):
    """ 
    Копирует файлы с камеры телефона на компьютер
    """
    print("1: ", folder_img)
    #print(two_circle,two_square,one_circle,one_square)
    #
    #click.echo(old_path)
    #click.echo(new_path)
    if folder_img:
        print("2: ", folder_img)
        old_path = os.path.normpath(path)
        print("link 1", old_path)
        new_path = _create_new_path(old_path, thinsection_name, lense_name, uch_name)
        print("link 1", new_path)
        copy(2, new_path)
        print("cope TRUE")
        
        load_img = LoadImg(new_path, lense_name)
        if two_circle:		
	        load_img.two_photo_circle()
	        load_img.one_photo_huf_circle()
        if two_square:
	        load_img.two_photo_square()

        if one_circle:
	        copy(1, new_path)
	        load_img.one_photo_circle()
        if one_square:
	        copy(1, new_path)
	        load_img.one_photo_square()

        if not do_not_remove_from_phone:
            del_photo_folder(pattern)

    else:
        print("3: ", folder_img)
        folder_path =  path_new_folder_img()
        new_path =  os.path.join(folder_path, thinsection_name)
        os.mkdir(new_path)
        load_img = LoadImg(new_path, lense_name)
        if two_circle:
	        load_img.two_photo_circle()
	        load_img.one_photo_huf_circle()
        if two_square:
	        load_img.two_photo_square()

        if one_circle:
	        load_img.one_photo_circle()
        if one_square:
	        load_img.one_photo_square()

        
if __name__ == "__main__":
    main()

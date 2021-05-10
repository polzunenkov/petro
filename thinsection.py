import subprocess
import os	
import click
import cv2
import numpy as np
import sys
import glob
from script import two_photo_circle, two_photo_square, one_photo_circle, one_photo_square


def _create_new_path(old_path, thinsection_name, lense, uch_name):
	''' Возвращает новое имя для фотографий шлифов с учетом имени thinsection_name
	'''
	path_new = os.path.join(old_path, thinsection_name, lense, uch_name)
	return path_new

def copy(path, new_path):
	''' копирует фотографии с телефона из дирректории Camera 
            -стандартной камеры Honor
	''' 
	# create main folder
	os.makedirs(new_path, exist_ok=True)
	subprocess.run(["adb", "pull", "/sdcard/DCIM/Camera/.", new_path])
	del_cache_path = os.path.join(new_path, "cache")
	os.rmdir(del_cache_path)
	

def del_photo_folder(pattern):
	''' удаляет фотографии с телефона из дирректории Camera 
        -стандартной камеры Honor
	pattern - <common prefix>*.расширение файла- например jpg
	'''
 
	subprocess.run(["adb", "shell", "rm", "-f", 
                        f"/sdcard/DCIM/Camera/{pattern}"])		

@click.command()
@click.option('--path', help='Path to destination folder', required=True)
@click.option('--pattern', help='pattern to delete files from Camera folder', default="IMG_*.jpg")
@click.option('--thinsection_name', help='name for the thin section', default="thin01")
@click.option('--lense_name', help='name of the lesne used', default="x5")
@click.option('--uch_name', help='name of the uch used', default="1")
@click.option('--two_circle', help='combine photo after change black by white from mask circle', is_flag=True, default=False)
@click.option('--two_square', help='combine photo after change black by white from mask circle', is_flag=True, default=False)
@click.option('--one_circle', help='combine photo after change black by white from mask circle', is_flag=True, default=False)
@click.option('--one_square', help='combine photo after change black by white from mask circle', is_flag=True, default=False)
@click.option('--do_not_remove_from_phone', help='remove phtos from phone folder ', is_flag=True, default=False)
def main_(path, pattern, thinsection_name, lense_name, uch_name, two_circle, two_square, one_circle, one_square, do_not_remove_from_phone):
	ready(path=path, pattern=pattern, thinsection_name=thinsection_name, lense_name=lense_name, uch_name=uch_name, two_circle=two_circle, two_square=two_square, one_circle=one_circle, one_square=one_square, do_not_remove_from_phone=do_not_remove_from_phone)


def ready(path, pattern, thinsection_name, lense_name, uch_name, two_circle=False, two_square=False, one_circle=False, one_square=False, do_not_remove_from_phone=False):
	''' 
	Копирует файлы с камеры телефона на компьютер
	'''
	old_path = os.path.normpath(path)
	new_path = _create_new_path(old_path, thinsection_name, lense_name, uch_name)
	click.echo(old_path)
	click.echo(new_path)
	copy(old_path,new_path)
			
	if two_circle:
		two_photo_circle(new_path, lense_name)
	
	if two_square:
		two_photo_square(new_path, lense_name)
		
	if one_circle:
		one_photo_circle(new_path, lense_name)
	
	if one_square:
		one_photo_square(new_path, lense_name)
	
	if not do_not_remove_from_phone:
		del_photo_folder(pattern)




if __name__=="__main__":
	main_()







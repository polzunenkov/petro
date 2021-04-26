from tkinter import *
from tkinter.ttk import Combobox  
from PIL import ImageTk, Image
#import os
import time
import subprocess

from script import run_combine

def camera_on():
	
	i = 0
	#The interval between operations depends on the phone configuration. The higher the configuration, the shorter the time.
	sleep_time = 0.5 
	#while 1:
	#Use popen to set shell=True will not pop up cmd box
	subprocess.Popen('scrcpy',shell=True)
	time.sleep(sleep_time)
	subprocess.Popen('adb shell am start -a android.media.action.STILL_IMAGE_CAMERA',shell=True)
	#subprocess.run(["mkdir", "-p", "test"])
	#i+=1
        #print str(i) + "clicks have been completed"
        
        #os.system("adb shell")
        #os.system("am start -a android.media.action.STILL_IMAGE_CAMERA")
	
		
def photo_make():
	
	subprocess.Popen('adb shell input keyevent 27',shell=True)
	#time.sleep(sleep_time)
	#subprocess.run(["adb", "pull", f"/sdcard/DCIM/Camera/{pattern}", "/tmp/test/"])#	adb pull /sdcard/DCIM/Camera/nicole-.jpg /tmp/1.jpg

	#subprocess.run(["mv", f"/sdcard/DCIM/Camera/{pattern}"])
	
	#for img in *.jpg; do mv -- "$img" "/tmp/petro/nicole-.jpg"; done
	#for img in /sdcard/DCIM/Camera/*.jpg; do mv -- "$img" "/tmp/petro/nicole-.jpg"; done

	#os.system("adb shell input keyevent 4")
	#os.system("input keyevent 27")

def param():
	
	save_thinsection_photo = f"python3.7 thinsection.py --path=~/{colection.get()} --thinsection_name={thinsection.get()} --lense_name={obj.get()} --uch_name={uch.get()}"
	print(save_thinsection_photo)
	subprocess.Popen(str(save_thinsection_photo),shell=True)
	
	
	
#def show_image(path):
path="microscope.jpg"
root = Tk()
img = Image.open(path)
w = 500
ratio = (w / float(img.size[0]))
h = int((float(img.size[1]) * float(ratio)))
imag = img.resize((w,h), Image.ANTIALIAS)
image = ImageTk.PhotoImage(imag)
panel = Label(root, image=image)
panel.pack(side="top", fill="both", expand="no")
root.title("Фотографии шлифов")

Label(root, text="Коллекция").place(x=200,y=10)
colection = Entry(root,width=20)
colection.place(x=320,y=10)
colection.focus()

Label(root, text="Автор").place(x=250,y=30)
author = Entry(root,width=20)
author.place(x=320,y=30)

Label(root, text="Обьектив").place(x=10,y=200)
obj = Combobox(root,width=5)
obj['values'] = ("x2.5", "x4", "x5", "x10", "X20", "X40", "X50", "X100")
obj.current(0) # установите вариант по умолчанию
obj.place(x=120,y=200)

Label(root, text="№ шлифа").place(x=10,y=250)
thinsection = Entry(root,width=15)
thinsection.place(x=150,y=250)

Label(root, text="№ учатска").place(x=10,y=300)
#uch = Entry(root,width=5)
#uch.place(x=150,y=300)

uch = Spinbox(root, from_=1, to=5, width=4)  
uch.place(x=150,y=300)  

btn = Button(root, text=">", command=param, height = 6, width = 8)
btn.place(x=420,y=180)

GO = Button(root, text="Выход", command=root.quit, height = 6, width = 8)
GO.place(x=420,y=300) #



camera = Button(root, text="Камера", command=camera_on, height = 8, width = 10)
camera.place(x=10,y=340) #



#Label(root, text="Николи").place(x=30,y=380)
#nicoli_minus = Button(root, text="-", command=photo_make, height = 3, width = 4)
#nicoli_minus.place(x=10,y=410) #

#nicoli_plus = Button(root, text="+", command=photo_make, height = 3, width = 4)
#nicoli_plus.place(x=80,y=410) #



root.mainloop()
	
	
#run_combine(new_path="/tmp/petro/~/Q/1/x5/2/")

#show_image("/tmp/python_circle_detaction/microscope.jpg")

#adb shell rm /sdcard/DCIM/Camera/.


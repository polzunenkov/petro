from tkinter import *
from tkinter.ttk import Combobox  
from PIL import ImageTk, Image
import os


def camera_on():
	
	os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
	
		
def photo_make():
	
	#os.system("adb shell input keyevent 4")
	os.system("adb shell input keyevent 27")

def param():
	
	print( f"python3.7 thinsection.py --path=~/{object.get()} --thinsection_name= {thinsection.get()} --lense_name= {obj.get()}")  
	
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

Label(root, text="Обьект").place(x=250,y=10)
object = Entry(root,width=20)
object.place(x=320,y=10)
object.focus()

Label(root, text="Автор").place(x=250,y=30)
author = Entry(root,width=20)
author.place(x=320,y=30)

Label(root, text="Обьектив").place(x=10,y=200)
obj = Combobox(root,width=5)
obj['values'] = ("x5", "x10", "X20", "X40", "X50", "X100")
obj.current(0) # установите вариант по умолчанию
obj.place(x=120,y=200)

Label(root, text="№ шлифа").place(x=10,y=250)
thinsection = Entry(root,width=15)
thinsection.place(x=150,y=250)

Label(root, text="№ учатска").place(x=10,y=300)
uch = Entry(root,width=5)
uch.place(x=150,y=300)

btn = Button(root, text="создать", command=param).place(x=300,y=410)


GO = Button(root, text="X", command=root.quit)
GO.place(x=420,y=410) #



camera = Button(root, text="Камера", command=camera_on)
camera.place(x=10,y=340) #



Label(root, text="Николи").place(x=30,y=380)
nicoli_minus = Button(root, text="-", command=photo_make, height = 3, width = 4)
nicoli_minus.place(x=10,y=410) #

nicoli_plus = Button(root, text="+", command=photo_make, height = 3, width = 4)
nicoli_plus.place(x=80,y=410) #



root.mainloop()
	
	


#show_image("/tmp/python_circle_detaction/microscope.jpg")




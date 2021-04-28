from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import time
import subprocess


def camera_on():
	
	i = 0
	#The interval between operations depends on the phone configuration. The higher the configuration, the shorter the time.
	sleep_time = 0.5 
	#Use popen to set shell=True will not pop up cmd box
	subprocess.Popen('scrcpy',shell=True)
	time.sleep(sleep_time)
	subprocess.Popen('adb shell am start -a android.media.action.STILL_IMAGE_CAMERA',shell=True)
	
	
def photo_make():
	subprocess.Popen('adb shell input keyevent 27',shell=True)

def param(collection, thinsection, obj, uch, chk_state, diametr):
	save_thinsection_photo = f"python3.7 thinsection.py --path={collection.get()} --thinsection_name={thinsection.get()} --lense_name={obj.get()} --uch_name={uch.get()} --diametr_pole={diametr.get()} --do_not_remove_from_phone"
	if chk_state.get() == 1:
		save_thinsection_photo += " --montage"
	print(save_thinsection_photo)
	subprocess.Popen(str(save_thinsection_photo),shell=True)
	
class Application:
    def __init__(self):
        self.root =  Tk()
        img = Image.open("/tmp/petro/microscope.jpg")
        w = 500
        ratio = (w / float(img.size[0]))
        h = int((float(img.size[1]) * float(ratio)))
        imag = img.resize((w,h), Image.ANTIALIAS)
        images = ImageTk.PhotoImage(imag)
        panel = Label( image=images)
        panel.pack(side="top", fill="both", expand="no")
        self.root.title("PETRO PHOTO")

        Label(self.root, text="Коллекция").place(x=200,y=10)
        collection = Entry(self.root,width=20)
        collection.place(x=320,y=10)
        collection.focus()

        Label(self.root, text="Автор").place(x=250,y=30)
        author = Entry(self.root,width=20)
        author.place(x=320,y=30)
        
        Label(self.root, text="Обьектив").place(x=10,y=200)
        obj = Combobox(self.root,width=5)
        obj['values'] = ("x5", "x10", "X20", "X40", "X50", "X100")
        obj.current(0) # установите вариант по умолчанию
        obj.place(x=120,y=200)
        
        Label(self.root, text="d поле, мм").place(x=10,y=225)
        diametr = Entry(self.root,width=5)
        diametr.place(x=120,y=225)
        
        Label(self.root, text="№ шлифа").place(x=10,y=250)
        thinsection = Entry(self.root,width=15)
        thinsection.place(x=120,y=250)

        Label(self.root, text="№ учатска").place(x=10,y=275)
        #uch = Entry(root,width=5)
        #uch.place(x=150,y=300)

        uch = Spinbox(self.root, from_=1, to=5, width=4)  
        uch.place(x=120,y=275)
        
                
        chk_state = IntVar()
        chk_state.set(0) # False
        chk_state.set(1) # True
        chk = Checkbutton(self.root, text='Монтаж', var=chk_state)
        chk.place(x=10, y=325)
        
        camera = Button(self.root, text="Камера", command=camera_on, height = 8, width = 10)
        camera.place(x=400,y=50)
        
        btn = Button(self.root, text="Фото", height = 8, width = 10, command=lambda: param(collection, thinsection, obj, uch, chk_state, diametr))
        btn.place(x=10,y=350)
        
        
        GO = Button(self.root, text="Выход", command=self.root.quit, height = 8, width = 10)
        GO.place(x=400,y=350) #


        self.root.mainloop()
		#Label(root, text="Николи").place(x=30,y=380)
        #nicoli_minus = Button(root, text="-", command=photo_make, height = 3, width = 4)
        #nicoli_minus.place(x=10,y=410) #

        #nicoli_plus = Button(root, text="+", command=photo_make, height = 3, width = 4)
        #nicoli_plus.place(x=80,y=410) #

        

def main():
    app = Application()
    

if __name__ == '__main__':
    main()

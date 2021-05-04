from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import time
import subprocess
import tkinter.font as font

def open_config():
	subprocess.Popen('gedit config',shell=True)

def on_select(event, obj):
	lens = read_config_lense()
	print("on_select")
	obj['values'] = (list(lens.keys()))

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

def param(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3):
	save_thinsection_photo = f"python3.7 thinsection.py --path={collection.get()} --thinsection_name={thinsection.get()} --lense_name={obj.get()} --uch_name={uch.get()} --pattern='*.jpg' "
	if chk_state.get() == 1:
		save_thinsection_photo += " --two_circle"
	if chk_state1.get() == 1:
		save_thinsection_photo += " --two_square"
	if chk_state2.get() == 1:
		save_thinsection_photo += " --one_circle"
	if chk_state3.get() == 1:
		save_thinsection_photo += " --one_square"
	print(save_thinsection_photo)
	subprocess.Popen(str(save_thinsection_photo),shell=True)
	
class Application:
    def __init__(self):
        self.root =  Tk()
        #self.root.geometry("250x540")
        img = Image.open("microscope.jpg")
        w = 250; h = 540
        ratio = (w / float(img.size[0]))
        imag = img.resize((w,h), Image.ANTIALIAS)
        images = ImageTk.PhotoImage( imag )
        panel = Label( image=images )
        panel.pack(side="top", fill="both", expand="no")
        self.root.title("NEISRI FEB RAS")
        Times = font.Font(family='Times', size=12, weight='bold')
         
        camera = Button(self.root, text="Camera", command=camera_on, height = 5, width = 31)
        camera.place(x=4,y=65)
        
        configBtn = Button(self.root,  text="Config", height = 5, width = 31, command=open_config)
        configBtn.place(x=4,y=135)
        
        Label(self.root,font=Times, text="Collection").place(x=80,y=205)
        collection = Entry(self.root,font=Times,justify="center",width=30)
        collection.place(x=4,y=228)
        collection.focus()

        Label(self.root, font=Times, text="Sample").place(x=100,y=251)
        thinsection = Entry(self.root, font=Times,justify="center", width=30)
        thinsection.place(x=4,y=274)
        
        lens = read_config_lense()
        Label(self.root,  font=Times, text="Lense").place(x=35,y=297)
        obj = Combobox(self.root,font=Times,justify="center", width=13)
        obj['values'] = (list(lens.keys()))
        obj.current(0) # установите вариант по умолчанию
        obj.place(x=5,y=315)
        obj.bind('<Button-1>', lambda event: on_select(event, obj))    
        
        Label(self.root,  font=Times,  text="Area").place(x=160,y=297)
        uch = Spinbox(self.root, font=Times,justify="center",from_=1, to=5, width=13)  
        uch.place(x=127,y=315)
        
        Label(self.root,font=Times, text="Type of mask").place(x=70,y=338)
        
        Label(self.root,  font=Times,  text="Two photo ").place(x=5,y=360)
        
        chk_state = IntVar()
        chk_state.set(0) # False
        chk_state.set(1) # True
        chk = Checkbutton(self.root,font=Times, text='❍❍', var=chk_state)
        chk.place(x=92, y=360)
        
        chk_state1 = IntVar()
        chk_state1.set(1) # False
        chk_state1.set(0) # True
        chk1 = Checkbutton(self.root,font=Times, text='❐❐', var=chk_state1)
        chk1.place(x=170, y=360)
        
        Label(self.root,  font=Times,  text="One photo ").place(x=5,y=380)
        
        chk_state2 = IntVar()
        chk_state2.set(1) # False
        chk_state2.set(0) # True
        chk2 = Checkbutton(self.root,font=Times, text='❍', var=chk_state2)
        chk2.place(x=92, y=380)
        
        chk_state3 = IntVar()
        chk_state3.set(1) # False
        chk_state3.set(0) # True
        chk3 = Checkbutton(self.root,font=Times, text='❐', var=chk_state3)
        chk3.place(x=170, y=380)
        
        btn = Button(self.root, text="Make", height = 5, width = 31, command=lambda: param(collection, thinsection, obj, uch, chk_state,chk_state1,chk_state2,chk_state3))
        btn.place(x=5,y=400)
                       
        GO = Button(self.root, text="Exit", command=self.root.quit, height = 5, width = 31)
        GO.place(x=5,y=470) #

        self.root.mainloop()
		
        

def main():
    app = Application()
    

if __name__ == '__main__':
    main()

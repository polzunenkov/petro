from tkinter import *
from tkinter.ttk import Combobox
import time
import subprocess
import tkinter.font as font

from thinsection import ready
from script import read_config_lense


def open_config():
	subprocess.Popen('gedit config',shell=True)

def on_select(event, obj):
	lens = read_config_lense()
	print("on_select")
	obj['values'] = (list(lens.keys()))



def camera_on():
	
	i = 0
	#The interval between operations depends on the phone configuration. The higher the configuration, the shorter the time.
	sleep_time = 0.5 
	#Use popen to set shell=True will not pop up cmd box
	subprocess.Popen('scrcpy',shell=True)
	time.sleep(sleep_time)
	subprocess.Popen('adb shell am start -a android.media.action.STILL_IMAGE_CAMERA',shell=True)
	
two_circle_=False
two_square_=False
one_circle_=False
one_square_=False

def param(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3):
	print(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3)
	if chk_state.get() == 1:
		two_circle_=True
	if chk_state1.get() == 1:
		two_square_=True
	if chk_state2.get() == 1:
		one_circle_=True
	if chk_state3.get() == 1:
		one_square_=True
	
	ready(path=collection.get(), pattern='*.jpg', thinsection_name=thinsection.get(), lense_name=obj.get(), uch_name=uch.get(), two_circle=two_circle_, two_square=two_square_, one_circle=one_circle_, one_square=one_square_, do_not_remove_from_phone=True)

		
	
class Application:
    def __init__(self):
        self.root =  Tk()
        frame1 = Frame(self.root)
        frame2 = Frame(self.root)
        frame2left = Frame(frame2)
        frame2right = Frame(frame2)
        
        
        frame1.pack(side=TOP, fill=BOTH, expand=1)
        frame2.pack(side=BOTTOM, fill=BOTH, expand=1)
        frame2left.pack(side=LEFT, fill=BOTH, expand=1)
        frame2right.pack(side=RIGHT, fill=BOTH, expand=1)
       
        
        photo = PhotoImage(file = r"microscope.png")
        
        self.root.title("NEISRI FEB RAS")
        Times = font.Font(family='Times', size=12, weight='bold')
        Times1 = font.Font(family='Times', size=12, weight='bold')
        btn_font = font.Font(family='Times', size=24, weight='bold')
        
        about = Button(frame1,image=photo,font=btn_font, text="About")
        about.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        
        camera = Button(frame1,font=btn_font, text="Camera", command=camera_on)
        camera.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        
        configBtn = Button(frame1, font=btn_font, text="Config", command=open_config)
        configBtn.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        
        Label(frame1,font=Times, text="Collection").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        collection = Entry(frame1,font=Times,justify="center")
        collection.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        collection.focus()

        Label(frame1, font=Times, text="Sample").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        thinsection = Entry(frame1, font=Times,justify="center")
        thinsection.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        
        lens = read_config_lense()
        Label(frame1,  font=Times, text="Lense").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        obj = Combobox(frame1,font=Times,justify="center")
        obj['values'] = (list(lens.keys()))
        obj.current(0) # установите вариант по умолчанию
        obj.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        obj.bind('<Button-1>', lambda event: on_select(event, obj))    
        
        Label(frame1,  font=Times,  text="Area").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        uch = Spinbox(frame1, font=Times,justify="center",from_=1, to=5)  
        uch.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
        
        Label(frame1,font=Times, text="Type of mask").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        
               
        chk_state2 = IntVar()
        chk_state2.set(1) # False
        chk_state2.set(0) # True
        chk2 = Checkbutton(frame1,font=Times1, text='❍', var=chk_state2)
        chk2.pack(side=RIGHT, fill=BOTH, padx=5, pady=5, expand=1)
        
        chk_state = IntVar()
        chk_state.set(0) # False
        chk_state.set(1) # True
        chk = Checkbutton(frame1,font=Times1, text='❍❍', var=chk_state)
        chk.pack(side=LEFT, fill=BOTH, padx=5, pady=5, expand=1)
        
        chk_state3 = IntVar()
        chk_state3.set(1) # False
        chk_state3.set(0) # True
        chk3 = Checkbutton(frame1,font=Times1, text='❐', var=chk_state3)
        chk3.pack(side=RIGHT, fill=BOTH, padx=5, pady=5, expand=1)
        
        chk_state1 = IntVar()
        chk_state1.set(1) # False
        chk_state1.set(0) # True
        chk1 = Checkbutton(frame1,font=Times1, text='❐❐', var=chk_state1)
        chk1.pack(side=LEFT, padx=5, pady=5, expand=1)
        
                
        GO = Button(frame2, font=btn_font, width=13, text="Exit", command=self.root.quit)
        GO.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5, expand=1) #
        
        btn = Button(frame2, font=btn_font, text="Make", command=lambda: param(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3))
        btn.pack(side=BOTTOM, fill=BOTH, padx=5, pady=5, expand=1)
                       
        

        self.root.mainloop()
		
        

def mains():
    app = Application()
    

if __name__ == '__main__':
    mains()

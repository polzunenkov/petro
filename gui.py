from tkinter import *
from tkinter.ttk import Combobox
import time
import subprocess
import tkinter.font as font
import os
import configparser
from thinsection import ready
from script import create_config_, get_setting, update_setting, get_config, lens_

path = "settings.ini"
   
#lense_get = get_setting(path, 'Lense', lense_dict[1])


def settings():
	settings = Tk()
	settings.title("Settings lense")
	path="settings.ini"
	Times = font.Font(family='Times', size=12, weight='bold')
	
	LAB1 = Label(settings, font=Times, text="Lense 1").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	name_lens1 = Entry(settings, font=Times,justify="center")
	name_lens1.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	name_lens1.insert(0,"x5")
	LAB1_ = Label(settings, font=Times, text="Diametr pole").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	d_lens1 = Entry(settings, font=Times,justify="center")
	d_lens1.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	d_lens1.insert(0,"4")
	
	LAB2 = Label(settings, font=Times, text="Lense 2").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	name_lens2 = Entry(settings, font=Times,justify="center")
	name_lens2.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	name_lens2.insert(0,"x10")
	LAB2_ = Label(settings, font=Times, text="Diametr pole").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	d_lens2 = Entry(settings, font=Times,justify="center")
	d_lens2.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	d_lens2.insert(0,"2")
	
	LAB3 = Label(settings, font=Times, text="Lense 3").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	name_lens3 = Entry(settings, font=Times,justify="center")
	name_lens3.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	name_lens3.insert(0,"x20")
	LAB3_ = Label(settings, font=Times, text="Diametr pole").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	d_lens3 = Entry(settings, font=Times,justify="center")
	d_lens3.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	d_lens3.insert(0,"1")
	
	LAB4 = Label(settings, font=Times, text="Lense 4").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	name_lens4 = Entry(settings, font=Times,justify="center")
	name_lens4.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	name_lens4.insert(0,"x40")
	LAB4_ = Label(settings, font=Times, text="Diametr pole").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	d_lens4 = Entry(settings, font=Times,justify="center")
	d_lens4.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	d_lens4.insert(0,"0.5")
	
	LAB5 = Label(settings, font=Times, text="Lense 5").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	name_lens5 = Entry(settings, font=Times,justify="center")
	name_lens5.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	name_lens5.insert(0,"x60")
	LAB5_ = Label(settings, font=Times, text="Diametrgit  pole").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
	d_lens5 = Entry(settings, font=Times,justify="center")
	d_lens5.pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	d_lens5.insert(0,"0.25")
		
	Button(settings, font=Times, text="Make", command=lambda:get_config(path,name_lens1,name_lens2,name_lens3,name_lens4,name_lens5,d_lens1,d_lens2,d_lens3,d_lens4,d_lens5)).pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	#Button(settings, font=Times, text="Exit", command=settings.quit).pack(side=TOP, fill=BOTH, padx=5, pady=5, expand=1)
	
		
		    
def open_config():
	subprocess.Popen('gedit config',shell=True)


	
		
def on_select(event, obj):
	lens = lens_()
	obj['values'] = lens



def camera_on():
	
	i = 0
	#The interval between operations depends on the phone configuration. The higher the configuration, the shorter the time.
	sleep_time = 0.5 
	#Use popen to set shell=True will not pop up cmd box
	subprocess.Popen('scrcpy',shell=True)
	time.sleep(sleep_time)
	subprocess.Popen('adb shell am start -a android.media.action.STILL_IMAGE_CAMERA',shell=True)
	


def param(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3):
	print(collection, thinsection, obj, uch, chk_state, chk_state1, chk_state2, chk_state3)
	
	two_circle_=False
	two_square_=False
	one_circle_=False
	one_square_=False
	
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
        
        about = Button(frame1,image=photo,font=btn_font, text="About",command=settings)
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
        
        Label(frame1,  font=Times, text="Lense").pack(side=TOP, fill=BOTH, padx=5, pady=0, expand=1)
        obj = Combobox(frame1,font=Times,justify="center")
        obj['values'] = lens_()
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

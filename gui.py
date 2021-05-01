from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import time
import subprocess



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

def param(collection, thinsection, obj, uch, chk_state):
	save_thinsection_photo = f"python3.7 thinsection.py --path={collection.get()} --thinsection_name={thinsection.get()} --lense_name={obj.get()} --uch_name={uch.get()} --pattern='*.jpg' "
	if chk_state.get() == 1:
		save_thinsection_photo += " --montage"
	print(save_thinsection_photo)
	subprocess.Popen(str(save_thinsection_photo),shell=True)
	
class Application:
    def __init__(self):
        self.root =  Tk()
        img = Image.open("backround.png")
        w = 250
        ratio = (w / float(img.size[0]))
        h = 540#int((float(img.size[1]) * float(ratio)))
        imag = img.resize((w,h), Image.ANTIALIAS)
        images = ImageTk.PhotoImage(imag)
        panel = Label( image=images)
        panel.pack(side="top", fill="both", expand="no")
        self.root.title("NEISRI FEB RAS")
        
        Label(self.root, text="Автор").place(x=250,y=30)
        author = Entry(self.root,width=20)
        author.place(x=320,y=30)
        Label(self.root,font=("Times", "12", "bold"), text="Collection").place(x=80,y=205)
        collection = Entry(self.root,font=("Times",12),justify="center",width=30)
        collection.place(x=4,y=228)
        collection.focus()

        Label(self.root, font=("Times", "12", "bold"), text="Sample").place(x=100,y=251)
        thinsection = Entry(self.root, font=("Times",12),justify="center", width=30)
        thinsection.place(x=4,y=274)
        
        
        lens = read_config_lense()
        Label(self.root,  font=("Times", "12", "bold"), text="Lense").place(x=35,y=297)
        obj = Combobox(self.root,font=("Times",12),justify="center", width=13)
        obj['values'] = (list(lens.keys()))
        obj.current(0) # установите вариант по умолчанию
        obj.place(x=5,y=315)
        obj.bind('<Button-1>', lambda event: on_select(event, obj))    
               
        

        Label(self.root,  font=("Times", "12", "bold"),  text="Area").place(x=160,y=297)
        uch = Spinbox(self.root, font=("Times",12),justify="center",from_=1, to=5, width=13)  
        uch.place(x=127,y=315)
        
        
        Label(self.root,font=("Times", "12", "bold"), text="Number of photos").place(x=70,y=340)
        
        chk_state = IntVar()
        chk_state.set(0) # False
        chk_state.set(1) # True
        chk = Checkbutton(self.root,font=("Times", "12", "bold"), text='Two', var=chk_state)
        chk.place(x=160, y=360)
        
        chk_state1 = IntVar()
        chk_state1.set(1) # False
        chk_state1.set(0) # True
        chk = Checkbutton(self.root,font=("Times", "12", "bold"), text='One', var=chk_state1)
        chk.place(x=45, y=360)
        
        camera = Button(self.root, font=("Times",10,"bold"), text="Camera", command=camera_on, height = 5, width = 31)
        camera.place(x=4,y=65)
        
        
        configBtn = Button(self.root,  font=("Times",10), text="Config", height = 5, width = 31, command=open_config)
        configBtn.place(x=4,y=135)
        
        
        btn = Button(self.root, text="Make", height = 5, width = 31, command=lambda: param(collection, thinsection, obj, uch, chk_state))
        btn.place(x=5,y=400)
        
               
        GO = Button(self.root, text="Exit", command=self.root.quit, height = 5, width = 31)
        GO.place(x=5,y=470) #


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

import matplotlib  
matplotlib.use('TkAgg')   
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy
import math
import os 
import subprocess
from tkinter import filedialog
import time

os.chdir('./EDSR/src')
SAVE_DIR = '../test'
RES_DIR = '../experiment/test/results-Demo'

class APP(tk.Tk):

  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)
    self.attributes("-topmost", True)
    self.title('SISR Demo')
    self.load_image = False
    self.image_name = ""
    self.ori_image= None
    self.res_image = None
    self.v = tk.IntVar()
    self.v.set(2)
    self.e = tk.StringVar()
    tk.Label(self,text='Click <Open> to upload an image \n Press <Upscale> to upscale image by a selected factor').grid(padx=10, row=0, column=0, columnspan=4)
    tk.Label(self,text='Open image:').grid(padx=10, row=1, column=0)
    tk.Button(self, text ='Open', command = lambda : self.LoadImg()).grid(padx=10, pady=5, row=1, column=1)
    self.f_name = tk.Label(self, text='')
    self.f_name.grid(padx=10, row=1, column=2)
    tk.Label(self,text='Magnitude:').grid(padx=10, row=2, column=0)
    self.r1 = tk.Radiobutton(self, 
                  text="2x",
                  padx = 20, 
                  variable=self.v, 
                  value=2).grid(row=2, column=1)
    self.r2 = tk.Radiobutton(self, 
                  text="3x",
                  padx = 20, 
                  variable=self.v, 
                  value=3).grid(row=2, column=2)
    self.r2 = tk.Radiobutton(self, 
                  text="4x",
                  padx = 20, 
                  variable=self.v, 
                  value=4).grid(row=2, column=3)

    tk.Label(self,text='Upscale image:').grid(padx=10, row=3, column=0)
    self.submit_button = tk.Button(self, text ='Upscale', command = lambda : self.Upscale())
    self.submit_button.grid(padx=10, pady=5, row=3, column=1)
    self.pros = tk.Label(self, text='')
    self.pros.grid(padx=10, row=3, column=2)
    #self.submit_button = tk.Button(self, text ='Compare', command = lambda : self.helper())
    #self.submit_button.grid(padx=10, pady=5, row=4, columnspan=4)

  def LoadImg(self):
    self.pros['text'] = ""
    File = askopenfilename(initialdir = "../../") 
    #print(File)
    if File:
      self.load_image = True
      tmp = File.split('/')
      self.image_name = tmp[-1]
      self.image_name = self.image_name.split('.')[0] + '.png'
      self.f_name['text'] = self.image_name
      self.ori_image = Image.open(File)
      os.makedirs(SAVE_DIR, exist_ok=True)
      ori_path = os.path.join(SAVE_DIR, self.image_name)
      self.ori_image.save(ori_path)
      '''
      w, h = ori_image.size
      #load = load.resize((550, math.ceil(550/w*h)))
      #imgfile = ImageTk.PhotoImage(load )

      #canvas.image = imgfile  # <--- keep reference of your image
      #canvas.create_image(2,2,anchor='nw',image=imgfile)

      # Display image loaded
      #plt.figure(figsize=(math.ceil(w*0.005), math.ceil(h*0.005)))
      plt.title("Original image (%s x %s)"%(w,h))
      imgplot = plt.imshow(ori_image) 
      plt.show()  # display it
      '''
  def Upscale(self):
    if self.load_image:
      self.f_name['text'] = ''
      self.pros['text'] = "Processing..."
      self.update()
      #print(self.load_image)
      #print(self.v.get())
      self.Compute()

      self.load_image = False
      tmp = self.image_name.split('.')
      result_name = tmp[0] + '_x{}_SR.'.format(self.v.get()) + tmp[1]
      #print(result_name)
      self.pros['text'] = "Done."#output the result image    
      file_path = os.path.join(RES_DIR, result_name)

      while True:
        directory = filedialog.asksaveasfilename(initialdir = "../../../", initialfile=result_name)
        if directory :
          break

      cmd = "mv {} {}".format(file_path, directory)
      #print(cmd)
      return_code = subprocess.call(cmd, shell=True)
      cmd = "rm -rf {}/*".format(SAVE_DIR)
      return_code = subprocess.call(cmd, shell=True)
      self.res_image = Image.open(directory)
      self.res_image.show()

  def Compute(self):
    print('Call model...')
    #return_code = subprocess.call(cmd, shell=True)
    cmd = "python main.py --data_test Demo --scale {} --n_resblocks 16 --pre_train ../models/model_demo_x{}.pt --test_only --save_results".format(self.v.get(), self.v.get())
    return_code = subprocess.call(cmd, shell=True)
    #print(return_code)


  '''
  def change_img(self):
      if self.old:
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.new_img, anchor="nw")
        self.t.image = self.new_img
        self.old = False
      else:
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.old_img, anchor="nw")
        self.t.image = self.old_img
        self.old = True

      self.t.after(5000, self.change_img())

  def CompareImage(self):

        self.new_img = ImageTk.PhotoImage(self.res_image)

        self.ori_image = self.ori_image.resize((self.new_img.width(), self.new_img.height()), Image.ANTIALIAS)
        self.old_img = ImageTk.PhotoImage(self.ori_image)

        self.t = tk.Toplevel()
        self.canvas = tk.Canvas(self.t, width=self.new_img.width(), height=self.new_img.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.old_img, anchor="nw")
        self.t.image = self.old_img
        self.old = True

  def helper(self):
      self.CompareImage()
      self.change_img()
  '''
  def __del__(self):
    cmd = "rm -rf {}/*".format(SAVE_DIR)
    return_code = subprocess.call(cmd, shell=True)

def main():
    app = APP()
    app.mainloop()  
    return 0

if __name__ == '__main__':
    main()
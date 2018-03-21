#!/usr/bin/env python
# by duo Dec 2017

from tkinter import *
from tkinter import ttk, font
from PIL import Image, ImageTk
import cv2
import urllib.request
import numpy as np
import argparse
import time
from datetime import datetime
import os

def toggleShowing():
  global isShowing, startShow
  isShowing = not isShowing
  startShow = True
  print('toggle show: now ', isShowing)

def turnOff():
  exit(0)

def placeCall(cmd):
  global wu
  if 'http://' in wu.get():
    # must inform Wemos D1 esp8266 URL
    x = urllib.request.urlopen(wu.get() + cmd)

def convert(image):
  # Convert the Image object into a TkPhoto object
  image = Image.fromarray(image)
  image = ImageTk.PhotoImage(image=image)
  return image

def showloop():
  print('Commands arrow keys:')
  print('up   -> Foward')
  print('down -> Back')
  print('left -> Left')
  print('right-> Right')
  print('other:')
  print('s  -> stop')
  print('c  -> toggle cature')
  print('Esc-> exit')

  start_time = time.time()

  try:
    stream=urllib.request.urlopen(iwu.get())
  except:
    print('Error opening ipWebcam URL: ', iwu.get())
    print('for help run with -h option')
    exit(1)

  _bytes = bytes()
  command = ''
  is_capturing = False
  #lets make sure the path exists!
  if not os.access(path.get(), os.F_OK):
    os.makedirs(path.get())
  commands = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']
  #startShow= false
  while True:
    _bytes += stream.read(1024)
    a = _bytes.find(b'\xff\xd8')
    b = _bytes.find(b'\xff\xd9')
    # if there is at least one frame buffered
    if a!=-1 and b!=-1:
      # get the frame bytes to form an image
      jpg = _bytes[a:b+2]
      # keep the rest in the bytes buffer
      _bytes= _bytes[b+2:]
      img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
      height, width = img.shape[1::-1]
        
      if is_capturing:
        elapsed_time = time.time() - start_time
        # save image each 1 second
        if elapsed_time > 1 and command in commands:
          timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
          timestamp = timestamp + '_' + command + '.jpg'
          image_filename = os.path.join(path.get(), timestamp)
          # save the image
          cv2.imwrite(image_filename, img)
          #restart the timer
          start_time = time.time()
        
      cv2.putText(img, command, (int(width*0.1), int(height*0.05)), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
      if is_capturing:
        cap = 'Capturing'
      else:
        cap = 'Not capturing'
      cv2.putText(img, cap, (int(width*0.8), int(height*0.05)), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

      cv2.imshow('Self driving bot wifi controller',img)

      #image = convert(img)
      #if panel == None:
      #  panel = Label(mainframe, image=image)
      #  panel.grid(row=6, columnspan=2)
      #  print('panel created.')
      #else:
      #  panel.configure(image=image)
      #  panel.image = image

      retval = np.int16(cv2.waitKey(1))
      if retval != -1:
        if retval == -174:
         print('FOWARD')
         placeCall('FOWARD')
         command = 'FOWARD'
        elif retval == -172:
         print('BACK')
         placeCall('BACK')
         command = 'BACK'
        elif retval == -175:
         print('LEFT')
         placeCall('LEFT')
         command = 'LEFT'
        elif retval == -173:
         print('RIGH')
         placeCall('RIGHT')
         command = 'RIGHT'
        elif chr(retval) == 's' or chr(retval) == 'S':
         print('STOP')
         placeCall('STOP')
         command = 'STOP'
        elif chr(retval) == 'c' or chr(retval) == 'C':
         print('toggle capture')
         is_capturing = not is_capturing
        elif retval ==27:
          break
          #exit(0)
        else:
          command = 'UNKNOWN'
          print('unknown command, key: ', retval, ' type: ', type(retval))


isShowing = False
startShow = False
root = Tk()
root.title("Robot Wifi Controller")
root.minsize(width=800, height=200)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12, family='Liberation mono', weight='bold')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

Label(mainframe, text="ip webcam URL", fg="blue").grid(row=0)
Label(mainframe, text="Wemos D1 URL", fg="blue").grid(row=1)
Label(mainframe, text="Capture path", fg="blue").grid(row=2)

iwu = StringVar()
wu = StringVar()
path = StringVar()
iwu.set('http://192.168.25.7:8080/video')
wu.set("http://192.168.25.18/")
path.set('./capture')
eiwu = Entry(mainframe, textvariable = iwu, width=50, font = default_font)
eiwu.grid(row=0, column=1, sticky=(W, E))
ewu = Entry(mainframe, textvariable = wu, width = 50, font = default_font)
ewu.grid(row=1, column=1, sticky=(W, E))
epath = Entry(mainframe, textvariable = path, width = 50, font = default_font)
epath.grid(row=2, column=1, sticky=(W, E))
Button(mainframe, text="Start", fg="blue", command=showloop).grid(row=4)
Button(mainframe, text="Exit", fg="red", command = turnOff).grid(row=5)


root.mainloop()


#parser = argparse.ArgumentParser()
#parser.add_argument("iwu", help = 'ipWebcam URL, i.e. \'http://192.168.25.7:8080/video\'', nargs='?', default='http://192.168.25.7:8080/video')
#parser.add_argument("wu", help = 'Wemos D1 esp8266 URL', nargs='?', default=None)
#parser.add_argument("path", help = 'path to store captured images', nargs='?', default='capture')
#args = parser.parse_args()







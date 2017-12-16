from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import urllib.request
import numpy as np
import argparse
import time
from datetime import datetime
import os



def placeCall(cmd):
  if args.wu != None:
    # must inform Wemos D1 esp8266 URL
    x = urllib.request.urlopen(args.wu + cmd)

def convert(image):
  # Convert the Image object into a TkPhoto object
  image = Image.fromarray(image)
  image = ImageTk.PhotoImage(image=image)
  return image

root = Tk()
root.title("Robot Wifi Controller")
root.minsize(width=800, height=700)

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

Label(mainframe, text="ip webcam URL", fg="blue").grid(row=0)
Label(mainframe, text="Wemos D1 URL", fg="blue").grid(row=1)
iwu = StringVar()
wu = StringVar()
iwu.set('http://192.168.25.7:8080/video')
eiwu = Entry(mainframe, textvariable = iwu).grid(row=0, column=1, sticky=(W, E))
ewu = Entry(mainframe, textvariable = wu).grid(row=1, column=1, sticky=(W, E))
Button(root, text="Start", fg="blue", command='mainfunc').grid(row=2)
Button(root, text="Exit", fg="red", command = '').grid(row=4)

root.mainloop()


#parser = argparse.ArgumentParser()
#parser.add_argument("iwu", help = 'ipWebcam URL, i.e. \'http://192.168.25.7:8080/video\'', nargs='?', default='http://192.168.25.7:8080/video')
#parser.add_argument("wu", help = 'Wemos D1 esp8266 URL', nargs='?', default=None)
#parser.add_argument("path", help = 'path to store captured images', nargs='?', default='capture')
#args = parser.parse_args()

#print('Commands arrow keys:')
#print('up   -> Foward')
#print('down -> Back')
#print('left -> Left')
#print('right-> Right')
#print('other:')
#print('s  -> stop')
#print('c  -> toggle cature')
#print('Esc-> exit')

def mainfunc():

  start_time = time.time()

  try:
    stream=urllib.request.urlopen(iwu.get)
  except:
    print('Error opening ipWebcam URL: ', iwu.get)
    print('for help run with -h option')
    exit(1)

  bytes = bytes()
  command = ''
  is_capturing = False
  #lets make sure the path exists!
  if not os.access(wu.get(), os.F_OK):
    os.makedirs(args.path)
  commands = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STOP']

  while True:
      bytes += stream.read(1024)
      a = bytes.find(b'\xff\xd8')
      b = bytes.find(b'\xff\xd9')
      # if there is at least one frame buffered
      if a!=-1 and b!=-1:
        # get the frame bytes to form an image
        jpg = bytes[a:b+2]
        # keep the rest in the bytes buffer
        bytes= bytes[b+2:]
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        height, width = img.shape[1::-1]
          
        if is_capturing:
          elapsed_time = time.time() - start_time
          # save image each 1 second
          if elapsed_time > 1 and command in commands:
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            timestamp = timestamp + '_' + command + '.jpg'
            image_filename = os.path.join(args.path, timestamp)
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

        image = convert(img)
        # if the panel is not None, we need to initialize it
        if panel is None:
          panel = tki.Label(image=image)
          panel.image = image
          pack.panel(side="left", padx=10, pady=10)
          panel.grid(row=3, column=0, columnspawn = 2)
          # otherwise, simply update the panel
        else:
          panel.configure(image=image)
          panel.image = image

        retval = np.int16(cv2.waitKey(1))
        if retval != -1:
          if retval ==27:
            exit(0)
          elif retval == -174:
           #print('FOWARD')
           placeCall('FOWARD')
           command = 'FOWARD'
          elif retval == -172:
           #print('BACK')
           placeCall('BACK')
           command = 'BACK'
          elif retval == -175:
           #print('LEFT')
           placeCall('LEFT')
           command = 'LEFT'
          elif retval == -173:
           #print('RIGH')
           placeCall('RIGHT')
           command = 'RIGHT'
          elif chr(retval) == 's' or chr(retval) == 'S':
           #print('STOP')
           placeCall('STOP')
           command = 'STOP'
          elif chr(retval) == 'c' or chr(retval) == 'C':
           #print('toggle capture')
           is_capturing = not is_capturing
          else:
            command = 'UNKNOWN'
            #print('unknown command, key: ', retval, ' type: ', type(retval))




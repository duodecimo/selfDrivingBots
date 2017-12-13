import cv2
import urllib.request
import numpy as np
import argparse

def placeCall(cmd):
  if args.wu != None:
    # must inform Wemos D1 esp8266 URL
    x = urllib.request.urlopen(args.wu + cmd)

parser = argparse.ArgumentParser()
parser.add_argument("iwu", help = 'ipWebcam URL, i.e. \'http://192.168.25.7:8080/video\'', nargs='?', default='http://192.168.25.7:8080/video')
parser.add_argument("wu", help = 'Wemos D1 esp8266 URL', nargs='?', default=None)
args = parser.parse_args()

print('Commands arrow keys:')
print('up   -> Foward')
print('down -> Back')
print('left -> Left')
print('right-> Right')
print('other:')
print('Esc-> exit')

try:
  stream=urllib.request.urlopen(args.iwu)
except:
  print('Error opening ipWebcam URL')
  print('for help run with -h option')
  exit(1)

bytes = bytes()
msgtext = ''
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        img = cv2.imdecode(np.fromstring(jpg,     dtype=np.uint8),cv2.IMREAD_COLOR)
        cv2.putText(img, msgtext, (230, 50), cv2.FONT_HERSHEY_TRIPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('img',img)
        retval = np.int16(cv2.waitKey(1))
        if retval != -1:
          if retval ==27:
            exit(0)
          elif retval == -174:
           print('FOWARD')
           placeCall('FOWARD')
           msgtext = 'FOWARD'
          elif retval == -172:
           print('BACK')
           placeCall('BACK')
           msgtext = 'BACK'
          elif retval == -175:
           print('LEFT')
           placeCall('LEFT')
           msgtext = 'LEFT'
          elif retval == -173:
           print('RIGH')
           placeCall('RIGHT')
           msgtext = 'RIGHT'
          else:
            msgtext = 'UNKNOWN'
            print('unknown command, key: ', retval, ' type: ', type(retval))




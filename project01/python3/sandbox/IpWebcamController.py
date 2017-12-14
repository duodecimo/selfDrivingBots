from tkinter import *
import webbrowser
import urllib.request


def callback(event):
    # must inform ip webcam URL
    webbrowser.open_new(r"http://192.168.25.7:8080/video")

def placeCall(cmd):
    # must inform Wemos D1 esp8266 URL
    x = urllib.request.urlopen("http://192.168.25.18/" + cmd)
    print('comando: ', cmd)


root = Tk()
root.bind('<Escape>', lambda e: root.quit())
root.bind('<Up>', lambda e: placeCall("FOWARD"))
root.bind('<Down>', lambda e: placeCall("BACK"))
root.bind('<Left>', lambda e: placeCall("LEFT"))
root.bind('<Right>', lambda e: placeCall("RIGHT"))

link = Label(root, text="ip webcam", fg="blue", cursor="hand2")
link.pack()
# click tk window text
link.bind("<Button-1>", callback)

root.mainloop()


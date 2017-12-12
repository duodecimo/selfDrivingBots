from tkinter import *
import webbrowser

def callback(event):
    # must inform ip webcam URL
    webbrowser.open_new(r"http://192.168.25.7:8080/video")

def placeCall(cmd):
    # must inform Wemos D1 esp8266 URL
    x = urllib.request.urlopen("http://192.168.25.7/" + cmd)
    result.set(x)


root = Tk()
root.bind('<Escape>', lambda e: root.quit())
root.bind('<Up>', lambda e: placeCall("CMD=FOWARD"))
root.bind('<Down>', lambda e: placeCall("CMD=BACK"))
root.bind('<Left>', lambda e: placeCall("CMD=LEFT"))
root.bind('<Right>', lambda e: placeCall("CMD=RIGHT"))

link = Label(root, text="ip webcam", fg="blue", cursor="hand2")
link.pack()
# click tk window text
link.bind("<Button-1>", callback)

root.mainloop()


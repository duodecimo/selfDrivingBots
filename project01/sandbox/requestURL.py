import urllib.request
from tkinter import *
from tkinter import ttk

def placeCall(cmd):
  try:
    x = urllib.request.urlopen(url.get() + cmd)
    result.set(x)
  except urllib.error.URLError as e: 
    ##Show user an error
    self.update_text(str(e)) 

root = Tk()
root.title("Request URL to Wemos D1")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

url = StringVar()
result = StringVar()
url_entry = ttk.Entry(mainframe, width=22, textvariable=url)
url_entry.grid(column=2, row=1, sticky=(W, E))

#four buttons for speed
ttk.Button(mainframe, text="Faster", command = lambda : placeCall("CMD=FASTER")).grid(column=3, row=3, sticky=N)
ttk.Button(mainframe, text="Fast", command = lambda : placeCall("CMD=FAST")).grid(column=3, row=4, sticky=N)
ttk.Button(mainframe, text="Slow", command = lambda : placeCall("CMD=SLOW")).grid(column=3, row=5, sticky=N)
ttk.Button(mainframe, text="Slower", command = lambda : placeCall("CMD=SLOWER")).grid(column=3, row=6, sticky=N)

#five icons
downImg =PhotoImage(file="images/down.gif")
leftImg =PhotoImage(file="images/left.gif")
rightImg =PhotoImage(file="images/right.gif")
stopImg =PhotoImage(file="images/stop.gif")
upImg =PhotoImage(file="images/up.gif")

#five buttons for directions
ttk.Button(mainframe, image = upImg, command = lambda : placeCall("CMD=FOWARD")).grid(column=7, row=3, sticky=N)
ttk.Button(mainframe, image = leftImg, command = lambda : placeCall("CMD=LEFT")).grid(column=6, row=4, sticky=W)
ttk.Button(mainframe, image = stopImg, command = lambda : placeCall("CMD=STOP")).grid(column=7, row=4, sticky=W)
ttk.Button(mainframe, image = rightImg, command = lambda : placeCall("CMD=RIGHT")).grid(column=8, row=4, sticky=W)
ttk.Button(mainframe, image = downImg, command = lambda : placeCall("CMD=BACK")).grid(column=7, row=5, sticky=W)

ttk.Label(mainframe, text="url").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Result").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text=result.get()).grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

url_entry.focus()
root.bind('<Return>', placeCall)

root.mainloop()

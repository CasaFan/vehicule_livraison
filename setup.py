from tkinter import Tk
from src.GUI import GUI
from cefpython3 import cefpython as cef


root = Tk()
root.state('zoomed')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.maxsize(width=screen_width, height=screen_height)

# set window size to screen size by default [DEV]: 1536*864
root.geometry('%sx%s' % (screen_width, screen_height))
root.update()

myGUI = GUI(root)
# myGUI.open_file()
cef.Initialize()
root.mainloop()
cef.Shutdown()

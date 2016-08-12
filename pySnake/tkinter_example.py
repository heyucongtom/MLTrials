# from Tkinter import *

# class Application(Frame):

# 	def say_hi(self):
# 		print "hi"

# 	def createWidgets(self):
# 		self.QUIT = Button(self)
# 		self.QUIT["text"] = "QUIT"
# 		self.QUIT["fg"] = "red"
# 		self.QUIT["command"] = self.quit
# 		print(self.QUIT.config())

# 		self.QUIT.pack({"side": "left"})

# 		self.hi_there = Button(self)
# 		self.hi_there["text"] = "Hello"
# 		self.hi_there["command"] = self.say_hi

# 		self.hi_there.pack({"side": "left"})

# 	def __init__(self, master = None):
# 		Frame.__init__(self, master)
# 		self.pack(ipadx=10, ipady=10, padx=10, pady=10)
# 		self.createWidgets()

# root = Tk()
# app = Application(master=root)
# app.mainloop()
# root.destroy()

import Tkinter as tk

board = [ [None]*15 for _ in range(15) ]
snake = [(3,4),(4,4),(4,5),(4,6)]

counter = 0

win = tk.Tk()

APP_WIN_XPOS = 100
APP_WIN_YPOS = 100
APP_WIN_WIDTH = 500
APP_WIN_HEIGHT = 500
APP_WIN_TITLE = "Trial Board"
APP_BACK_GND = 'grey'
SNAKE_COLOR = "black"

win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
win.geometry('{0}x{1}'.format(APP_WIN_WIDTH, APP_WIN_HEIGHT))
win.config(bg=APP_BACK_GND)

# for i, row in enumerate(board):
# 	for j, column in enumerate(row):
# 		if (i%2==0 and j%2==1) or (i%2==1 and j%2==0):
# 			color="black"
# 		else:
# 			color="grey"
# 		L = tk.Label(win, text="    ", bg=color,padx=5, pady=5)
# 		L.grid(row=i, column=j)
# 		counter += 1

for i, j in snake:
	L = tk.Label(win, text="    ", bg=SNAKE_COLOR, padx=3, pady=3)
	L.grid(row=i, column=j)

win.mainloop()

#!/usr/bin/env python
# coding: UTF-8

# try:
#     #~~ For Python 2.x
#     import Tkinter as tk
# except ImportError:
#     #~~ For Python 3.x
#     import tkinter as tk



# APP_WIN_XPOS = 100
# APP_WIN_YPOS = 100
# APP_WIN_WIDTH = 500
# APP_WIN_HEIGHT = 500
# APP_WIN_TITLE = 'Overlapping Widgets'
# APP_BACK_GND = 'palegoldenrod'

# MSG_01 = 'Lower Frame'
# MSG_02 = 'Lift Frame'

# class App(object):
    
#     def __init__(self):
        
#         self.win = tk.Tk()
#         self.win.geometry('+{0}+{1}'.format(APP_WIN_XPOS, APP_WIN_YPOS))
#         self.win.geometry('{0}x{1}'.format(APP_WIN_WIDTH, APP_WIN_HEIGHT))
#         self.win.protocol("WM_DELETE_WINDOW", self.close)
#         self.win.config(bg=APP_BACK_GND)
        
#         self.swap_state = tk.StringVar()
#         self.swap_another_state = tk.StringVar()
        
#         canvas = tk.Canvas(self.win, highlightthickness=0,
#             bg='steelblue')
#         canvas.place(x=20, y=20, width=300, height=300)
        
#         self.frame = tk.Frame(self.win, bg='green')
#         self.frame.place(x=200, y=200, width=200, height=200)

#         self.another_frame=tk.Frame(self.win, bg='grey')
#         self.another_frame.place(x=50, y=50, width=200, height=200)

        
#         tk.Button(self.win, textvariable=self.swap_state,
#             command=self.swap).pack(side='bottom', pady=2)

#         tk.Button(self.win, textvariable=self.swap_another_state, command=self.swap_another).pack(side='bottom',pady=4)
            
#         self.swap_state.set(MSG_01)
#         self.swap_another_state.set(MSG_01)
    
#     def swap(self):
#         message = self.swap_state.get()
#         if message == MSG_01:
#             self.frame.lower()
#             self.swap_state.set(MSG_02)
            
#         if message == MSG_02:
#             self.frame.lift()
#             self.swap_state.set(MSG_01)

#     def swap_another(self):
#     	message = self.swap_another_state.get()
#         if message == MSG_01:
#             self.another_frame.lower()
#             self.swap_another_state.set(MSG_02)
            
#         if message == MSG_02:
#             self.another_frame.lift()
#             self.swap_another_state.set(MSG_01)

#     def close(self):
#         self.win.destroy()
#         print ("Shut down application")

#     def run(self):
#         self.win.mainloop()
        
# app = App()
# app.win.title("Tk App Templates")

# app.run()


# def on_click(i,j,event):
#     global counter
#     color = "red" if counter%2 else "black"
#     event.widget.config(bg=color)
#     board[i][j] = color
#     counter += 1


# for i,row in enumerate(board):
#     for j,column in enumerate(row):
#         L = tk.Label(root,text='    ',bg='grey')
#         L.grid(row=i,column=j)
#         L.bind('<Button-1>',lambda e,i=i,j=j: on_click(i,j,e))

# root.mainloop()
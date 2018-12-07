from SerialCom import SerialCom
import tkinter as tk
from tkinter import Tk, Label, Button, Frame
from threading import Thread

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation

class MainGUI:

    def __init__(self, master):
        self.master = master
        master.title("Heart Rate Variability")

        self.frameTop = Frame(master, bg='#5555EE')
        self.frameMiddle = Frame(master, bg='#55EE55')
        self.frameTop.pack(fill=tk.X)
        self.frameMiddle.pack(fill=tk.BOTH, expand=True)

        # top frame
        self.buttonConnect = Button(self.frameTop, text="Connect / Disconnect", command=self.connect, width=30)
        self.labelConnect = Label(self.frameTop, text="Disconnected", width=20)
        self.frameTop.grid_columnconfigure(0, weight=1)
        self.frameTop.grid_columnconfigure(1, weight=1)
        self.buttonConnect.grid(row=0, column=0, sticky=tk.E, pady=30, padx=5)
        self.labelConnect.grid(row=0, column=1, sticky=tk.W, padx=5)

        # middle frame
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.subfig = self.fig.add_subplot(1, 1, 1)
        self.subfig.set_ylim(0, 4096)
        self.subfig.set_yticks((0, 2048, 4096))
        # self.subfig.set_yticklabels(('-5v','0v','5v')) # 정확한 단위? Peak 만 찾으면 되기때문에 필요 X?
        # self.subfig.set_ylabel('mv')
        self.subfig.set_xlim(0, 256*10-1)
        self.subfig.set_xticks((0, 256*1-1, 256*2-1, 256*3-1, 256*4-1, 256*5-1, 256*6-1, 256*7-1, 256*8-1, 256*9-1, 256*10-1))
        self.subfig.set_xticklabels(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10 Sec'))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frameMiddle)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frameMiddle)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.X, expand=1)

        self.xarr = []
        self.yarr = []
        self.line, = self.subfig.plot(self.xarr, self.yarr, 'r')


    def connect(self):
        if(self.labelConnect.cget("text") == "Disconnected"):
            self.labelConnect.config(text="Connected")


        elif(self.labelConnect.cget("text") == "Connected"):
            self.labelConnect.config(text="Disconnected")

    def animate(self, i):

        self.xarr.append(x.X)
        self.yarr.append(x.heartRateY)

        if(len(self.xarr) > 2 and self.xarr[-1] < self.xarr[-2]):
            self.xarr = []
            self.yarr = []

        self.line.set_data(self.xarr,  self.yarr)


x = SerialCom('COM13')
t2 = Thread(target=x.read_data)
t2.start()
root = Tk()
root.state('zoomed')
my_gui = MainGUI(root)
ani = animation.FuncAnimation(my_gui.fig, my_gui.animate, interval=1, blit=False)
root.mainloop()




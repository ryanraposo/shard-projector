import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
from functools import partial

def test_menus():
    root = ThemedTk(theme='equilux')
    root.geometry('300x300')
    root.config(bg="#424242")
    root.update()

    menu_bar = CustomMenuBar(root)     
    menu_bar.place({"x":0,"y":0})

    root.mainloop()

def test_fake_toggle():
    root = ThemedTk(theme='equilux')
    root.geometry('300x300')
    root.config(bg="#424242")

    left_style = 'left.Horizontal.TProgressbar'

    # style = ttk.Style()
    # style.configure(
    #     style=left_style,
    #     background="#424242",
    #     lightcolor="#424242",
    #     bordercolor="#424242"
    # )
    root.option_add("*TProgressbar*Label.background", "#424242")

    
    
    prog = ttk.Progressbar(root, maximum=2, style=left_style)
    prog.place(x=0,y=0,height=50,width=50)
    prog.step()
    root.mainloop()


class CustomMenuBar:
    def __init__(
        self,
        parent
        ):
        self.parent = parent
        parent_width = parent.winfo_width()

        style = ttk.Style()
        style.configure('frame.TFrame', bg="#5c5c5c")

        self.frame = ttk.Frame(
            master=parent,
            width=parent_width,
            height=20
            )
        
        file_option = ttk.OptionMenu(self.frame, tk.StringVar(), "Browse", "Exit")
        file_option.grid(row=0, column=0)

        edit_option = ttk.OptionMenu(self.frame, tk.StringVar(), "Copy", "Paste")
        edit_option.grid(row=0, column=1)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
    
    def place(self, kwargs):
        self.frame.place(**kwargs)

test_fake_toggle()

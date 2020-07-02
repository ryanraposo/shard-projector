import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser
from ttkthemes import ThemedTk

import pyperclip


def iter_except(function, exception):
    """Iter-like that stops on exception"""
    try:
        while True:
            yield function()
    except exception:
        return


class Mover(ThemedTk):
    def __init__(self, target_widget : ttk.Widget, target_parent : ttk.Widget, widget_name : str, increment=1):
        super().__init__(theme='equilux')
        self.configure(bg='#353535')
        self.title("Moving: " + widget_name)
        self.target_widget = target_widget
        self.widget_x = None
        self.widget_y = None
        self.target_parent = target_parent
        self.increment = increment

        btn_left = ttk.Button(self, text="<",command=self.left)
        btn_up = ttk.Button(self, text="^",command=self.up)
        btn_down = ttk.Button(self, text="v",command=self.down)
        btn_right = ttk.Button(self, text=">",command=self.right)

        self.lbl_info = ttk.Label(self, text="")
        
        self.btn_info_to_clipboard = ttk.Button(self, text="Copy", command=self.copy_to_clipboard)

        btn_left.grid(
            row=1,
            column=0
        )    
        btn_up.grid(
            row=0,
            column=1
        )
        btn_down.grid(
            row=1,
            column=1
        )
        btn_right.grid(
            row=1,
            column=2
        )

        self.lbl_info.grid(
            row=2,
            column=0
        )

        self.btn_info_to_clipboard.grid(
            row=2,
            column=1
        )

        self._update_location()
        
    def _update_location(self):
        """Updates internal values for widget location & updates display accordingly"""

        self.target_widget.update()
        self.target_parent.update()
        
        self.widget_x = self.target_widget.winfo_x()
        self.widget_y = self.target_widget.winfo_y()
        self.lbl_info.config(text="(x=" + str(self.widget_x) + ", y=" + str(self.widget_y) + ")")
        
    def _move_target(self, x : int, y : int):
        """Checks that move is within bounds and if so, re-places widget at x,y"""
        if x >= 0 and x <= self.target_parent.winfo_width():
            if y >= 0 and y <= self.target_parent.winfo_height():
                self.target_widget.place(x=x, y=y)
                
    def copy_to_clipboard(self):
        pyperclip.copy(self.lbl_info['text'])
        
        
    def left(self):
        x = self.widget_x - self.increment
        y = self.widget_y
        self._move_target(x,y)
        self._update_location()
    
    def up(self):
        x = self.widget_x
        y = self.widget_y - self.increment
        self._move_target(x,y)
        self._update_location()

    def down(self):
        x = self.widget_x
        y = self.widget_y + self.increment
        self._move_target(x,y)
        self._update_location()

    def right(self):
        x = self.widget_x + self.increment
        y = self.widget_y
        self._move_target(x,y)
        self._update_location()

if __name__ == "__main__":
    root = ThemedTk(theme='equilux')
    root.geometry("400x400")
    root.configure(bg="#424242")

    wee = ttk.Button(root, text="WEEE")
    wee.place(x=200,y=200)

    mover_wee = Mover(wee,root, "WEE Button")
    
    root.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser
from ttkthemes import ThemedTk

import widgets

class InfoBar(ttk.LabelFrame):
    def __init__(
        self,
        master=None,
        command_configure=None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        
        style = ttk.Style()

        style.configure(style="white.TLabel", foreground="#e5e5e5", background="#424242")
        style.configure(style="blendBg.TLabel", background='#424242')
        
        null_label = ttk.Frame(master=None, height=0, width=0)

        self.configure(labelwidget=null_label, padding=[0,3,0,3]) # enws

        name_info_field = ttk.Label(self, text="Name:", style="blendBg.TLabel")
        name_info_field.grid(row=0,column=0)
        self.name_info_value = ttk.Label(self, style="white.TLabel")
        self.name_info_value.grid(row=0,column=1)
        self.columnconfigure(1, minsize=50)

        widgets.WidgetBarSeparator(self).grid(row=0, column=2)

        gamemode_info_field = ttk.Label(self, text="Gamemode:", style="blendBg.TLabel")
        gamemode_info_field.grid(row=0,column=3)
        self.gamemode_info_value = ttk.Label(self, style="white.TLabel")
        self.gamemode_info_value.grid(row=0,column=4)
        self.columnconfigure(4, minsize=50)

        widgets.WidgetBarSeparator(self).grid(row=0, column=5)

        players_info_field = ttk.Label(self, text="Players:", style="blendBg.TLabel")
        players_info_field.grid(row=0, column=6)
        self.players_info_value = ttk.Label(self, style="white.TLabel")
        self.players_info_value.grid(row=0, column=7)
        self.columnconfigure(7, minsize=10)

        widgets.WidgetBarSeparator(self).grid(row=0, column=8)

        self.btn_configure = ttk.Button(master=self, text="Configure", command=command_configure)
        self.btn_configure.grid(row=0, column=9, sticky='e')
        self.columnconfigure(9, weight=1)

        for i in range(9):
            self.columnconfigure(i, pad=10)



    def debug(self):
        self.name_info_value.configure(text="Frontbutt Beach")
        self.gamemode_info_value.configure(text="Endless")
        self.players_info_value.configure(text="8")


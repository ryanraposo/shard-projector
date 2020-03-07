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

        fx_color = tk.colorchooser.askcolor()[1]
        print(fx_color)

    
        style = ttk.Style()
        style.configure(style='info.TLabelframe', background='#505050')
        style.configure(style="white.TLabel", foreground="#e5e5e5", background="#424242")
        style.configure(style="blendBg.TLabel", background='#424242')
        
        null_label = ttk.Frame(master=None, height=0, width=0)
        self.configure(labelwidget=null_label, style='info.TLabelframe')

        name_info_field = ttk.Label(self, text="Name:", style="blendBg.TLabel")
        name_info_field.grid(row=0,column=0, padx=10)
        self.name_info_value = ttk.Label(self, style="white.TLabel")
        self.name_info_value.grid(row=0,column=1)
        self.columnconfigure(1, minsize=100)

        gamemode_info_field = ttk.Label(self, text="Gamemode:", style="blendBg.TLabel")
        gamemode_info_field.grid(row=0,column=2, padx=5)
        self.gamemode_info_value = ttk.Label(self, style="white.TLabel")
        self.gamemode_info_value.grid(row=0,column=3)
        self.columnconfigure(3, minsize=50)

        players_info_field = ttk.Label(self, text="Players:", style="blendBg.TLabel")
        players_info_field.grid(row=0,column=4, padx=5)
        self.players_info_value = ttk.Label(self, style="white.TLabel")
        self.players_info_value.grid(row=0,column=5)
        self.columnconfigure(5, minsize=30)

        self.btn_configure = ttk.Button(master=self, text="Configure", command=self.debug)
        self.btn_configure.grid(row=0, column=6, sticky='e', padx=10, pady=3)
        self.columnconfigure(6, weight=1)
        # self.btn_configure.grid(row=0, column=6, padx=5, pady=3)
        # self.btn_configure.grid(side=tk.RIGHT)

    def debug(self):
        self.name_info_value.configure(text="Frontbutt Beach")
        self.gamemode_info_value.configure(text="Endless")
        self.players_info_value.configure(text="8")
        
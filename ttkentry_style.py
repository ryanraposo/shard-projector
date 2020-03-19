import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser
from ttkthemes import ThemedTk


root = ThemedTk(theme='equilux')

style = ttk.Style()
style.configure('my.TEntry', foreground='#E4A88A')

entry = ttk.Entry(master=root)
entry.grid(row=0,column=0)

entry.configure(style='my.TEntry')

root.mainloop()
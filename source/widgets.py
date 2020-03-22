import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import os

import PIL


class WidgetCommandPanel(ttk.Labelframe):
    def __init__(
        self,
        parent=None,
        buttons=[],  # list of tuples ex. ("label_text", fn_callback)
        max_columns=-1,
        panel_text="",
    ):
        super().__init__(parent)
        self.parent = parent
        self.buttons = []

        # Style
        style = ttk.Style(self)
        font_labelframe = ("TkDefaultFont", "12")
        style.configure("TLabelframe", font=font_labelframe)
        # Frame
        self.configure(text=panel_text)
        # Buttons
        for each in buttons:
            button = ttk.Button(self, text=each[0], command=each[1])
            self.buttons.append(button)
        # Placement
        current_column = 0
        current_row = 0
        for button in self.buttons:
            button.grid(row=current_row, column=current_column)
            if (
                current_column != max_columns - 1
            ):  # If still below max_columns, or it is disabled...
                current_column += 1  # Move to next column
            else:
                current_column = 0  # Move back to column zero
                current_row += 1  # Move to new row


class WidgetConsoleView(ttk.Frame):
    """
    """

    def __init__(self, parent=None, width=450, height_in_rows=10, **kwargs):
        super().__init__(parent)
        # Frame
        self.configure(width=width)
        # Style
        self.style = ttk.Style()
        self.style.configure("status.Label", background="#353535", font="TkDefault 9")
        self.style.configure(
            "WidgetConsoleView.Treeview",
            foreground="#3eb489",
            background="#353535",
            font="Consolas, 8",
        )
        self.style.configure(
            "WidgetConsoleView.Treeview.Item",
            padding=[0,0,0,0]
        )
        self.style.configure(
            "WidgetConsoleView.Treeview.Heading",
            font="TkDefault 9"
        )
        # Tree
        self.tree = ttk.Treeview(self, style="WidgetConsoleView.Treeview", height=height_in_rows, padding=[0,0,0,0])
        self.tree.column("#0", width=width, stretch=False)
        self.rowconfigure(0, weight=1)
        # self.tree.bind("<Motion>", self.on_motion)
        self.tree.grid(column=0, row=0, sticky=("nswe"))

        self.tree.update()
        self.update()

        self.status_label = ttk.Label(self, text="Status: ", style="status.Label")

    # def on_motion(self, event):
    #     self.status_label.place_forget()

    @property
    def height_in_pixels(self):
        self.update()
        self.tree.update()
        height_in_pixels = self.tree.winfo_height()
        return height_in_pixels

    def write_line(self, line, scroll_matching=True):
        item = self.tree.insert("", tk.END, text=line)
        if scroll_matching:
            self.tree.see(item)

    def set_heading(self, text):
        self.tree.heading("#0", text=str(text))

    def set_status(self, text):
        tree_y = self.tree.winfo_y()
        tree_height = self.tree.winfo_height()
        tree_width = self.tree.winfo_width()

        self.status_label.configure(text="Status: " + text)
        self.status_label.update()
        status_width = self.status_label.winfo_width()

        self.status_label.place(
            x=tree_width - status_width - 5, y=(tree_y + tree_height - 20)
        )


    def clear(self):
        self.tree.delete(*self.tree.get_children())
        self.set_heading("")

    def place(self, **kwargs):
        super().place(**kwargs)


class WidgetDirectorySelect(ttk.Labelframe):
    """A ttk-styled Entry and Browse button for selecting a directory path. Use get to access value, set_display_name for prominent text display"""

    def __init__(self, parent, command=None):
        super().__init__(parent)
        self.command=command
        null_label = ttk.Frame(master=None, height=0, width=0)
        self.configure(labelwidget=null_label)
        self.entry = ttk.Entry(self, width=70)
        self.entry.grid(row=0, column=0)
        self.browse = ttk.Button(self, command=command, text="Browse")
        self.browse.grid(row=0, column=1)

    def show_dialog(self):
        path = filedialog.askdirectory(master=self)
        return path
    
    def set(self, display_text):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, display_text)
        # self.entry.configure(width=len(display_text) - 20)


class WidgetLabelInput(ttk.Frame):
    """A widget containing a label and input together. Accepts various ttk input widgets as input_class. Creates a paired ttk.Label to the left of
    those which lack a suitable label of their own. Ensures columns span entire widget contained. Optional end-user toggle for enabling/disabling
    the field."""

    def __init__(
        self,
        parent,
        toggle_enable=False,
        label="",
        input_class=ttk.Entry,
        input_var=None,
        input_args=None,
        label_args=None,
        placeholder=None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Radiobutton, ttk.Button):
            input_args["variable"] = input_var
        else:  # ttk.Entry
            input_args["textvariable"] = input_var

        self.label = ttk.Label(self, text=label, **label_args)
        self.label.grid(row=0, column=1)  # sticky=(tk.W))

        self.input = input_class(self, **input_args)
        self.input.grid(row=0, column=2)  # , sticky=(tk.E))

        if placeholder:
            self.set_placeholder(placeholder)

        if toggle_enable:
            enabled = self.enabled = tk.BooleanVar(value=True)
            self.toggle_enable_checkbutton = ttk.Checkbutton(self, variable=enabled)
            self.toggle_enable_checkbutton.grid(row=0, column=0)

        self.columnconfigure(1, minsize=115)

        style = ttk.Style()
        style.configure('prominent.TEntry', foreground='#ffffff')
        style.configure('non_prominent.TEntry', foreground='#969799')


    def grid(self, sticky=("we"), **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
         tk.W)"""

        super().grid(sticky=sticky, **kwargs)

    def get(self):
        """Get handling for input_class cases. If widget has an input variable,
        simply calls get on the variable. If widget is type ttk.Text, gets
        line char 0 to END. If no input variable, calls get on the widget."""

        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get("1.0", tk.END)
            # elif type(self.input) == ttk.Checkbutton:
            #     if self.input['state'] == 'selected':
            #         return True
            #     return False
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # when numeric fields are empty
            return

    def set(self, value, *args, **kwargs):
        """Set handling for widgets expecting tk.BooleanVar, widgets with variables, and tick/untick
        functionality for tk.Checkbutton and tk.Radiobutton."""

        if (
            type(self.variable) == tk.BooleanVar
        ):  # if widget expects BooleanVar, cast input to bool
            self.variable.set(bool(value))
        elif self.variable:  # for other widgets with variable, simply call set
            self.variable.set(value * args, **kwargs)
        # if Checkbutton or Radiobutton, for value=True tick button, for False untick
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.configure(variable=tk.BooleanVar(value=True))
            else:
                self.input.configure(variable=tk.BooleanVar(value=False))

        elif type(self.input) == tk.Text:  # if ttk.Text...
            self.input.delete("1.0", tk.END)  # delete row 1 char 0 to the end
            self.input.insert("1.0", value)  # insert value at row 1 char 0
        else:  # input is a ttk.Entry with no variable
            self.input.delete(0, tk.END)  # delete row 1 char 0 to the end
            self.input.insert(0, value)  # insert value at row 1 char 0

    def _populate_placeholder(self):
        self.set_prominent(False)
        self.set(self.placeholder)

    def _clear_placeholder(self):    
        if not self.get_prominent():
            self.set('')
            self.set_prominent(True)

    def set_placeholder(self, value):
        self.placeholder = value
        self.input.bind('<FocusIn>', self._on_focus_in)
        self.input.bind('<FocusOut>', self._on_focus_out)
        self._populate_placeholder()

    def set_prominent(self, isProminent):
        if isProminent:
            self.input.configure(style='prominent.TEntry')
        else:
            self.input.configure(style='non_prominent.TEntry')
    
    def get_prominent(self):
        input_style = self.input['style']
        if input_style == 'prominent.TEntry':
            return True
        return False

    def _on_focus_in(self, event):
        self._clear_placeholder()

    def _on_focus_out(self, event):
        if self.get() == '':
            self._populate_placeholder()


class WidgetPowerButton(ttk.Frame):
    def __init__(self, parent, command):
        super().__init__(master=parent)
        self.parent = parent
        self.command = command

        self.on_image = tk.PhotoImage(file=r"img/on75percent.png")
        self.off_image = tk.PhotoImage(file=r"img/off75percent.png")

        self.power_button = ttk.Button(
            self, image=self.off_image, command=self._on_click
        )
        self.power_button.grid(row=0, column=0)

    def _on_click(self):
        self.parent.focus_set()
        self.command()
    
    def set_fx(self, isPowered):
        if isPowered:
            self.power_button.configure(image=self.on_image)
        else:
            self.power_button.configure(image=self.off_image)


class WidgetBarSeparator(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.photo_image = tk.PhotoImage(master=master, file=r"img/custom-tk-bar-sep.png")
        self.configure(image=self.photo_image)

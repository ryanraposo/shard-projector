import os

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import PIL


class CommandPanel(ttk.Labelframe):
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


class ConsoleView(ttk.Frame):
    """Console-like display widget with methods for adding lines, clearing,
    and setting a heading.
    """

    def __init__(self, parent=None, width=450, height_in_rows=10, **kwargs):
        super().__init__(parent)
        # Frame
        self.configure(width=width)
        # Style
        self.style = ttk.Style()
        self.style.configure(
            "status.Label", background="#353535", font="TkDefault 9"
        )
        self.style.configure(
            "WidgetConsoleView.Treeview",
            foreground="#3eb489",
            background="#353535",
            font="Consolas, 8",
        )
        self.style.configure(
            "WidgetConsoleView.Treeview.Item", padding=[0, 0, 0, 0]
        )
        self.style.configure(
            "WidgetConsoleView.Treeview.Heading", font="TkDefault 9"
        )
        # Tree
        self.tree = ttk.Treeview(
            self,
            style="WidgetConsoleView.Treeview",
            height=height_in_rows,
            padding=[0, 0, 0, 0],
        )
        self.tree.column("#0", width=width, stretch=False)
        self.rowconfigure(0, weight=1)
        # self.tree.bind("<Motion>", self.on_motion)
        self.tree.grid(column=0, row=0, sticky=("nswe"))

        self.tree.update()
        self.update()

        self.status_label = ttk.Label(
            self, text="Status: ", style="status.Label"
        )

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


class DirectorySelectEntry(ttk.Frame):
    def __init__(self, master=None, on_select=None, entry_args=None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_select = on_select

        entry_args = entry_args or {}

        self.entry = ttk.Entry(self, width=65, **entry_args)
        self.browse_button = ttk.Button(
            self, command=self._on_browse, text="Browse"
        )

        self.columnconfigure(0, weight=1)
        self.entry.grid(row=0, column=0, sticky="we")
        self.browse_button.grid(row=0, column=1)

    def insert(self, index, string):
        self.entry.insert(index, string)

    def delete(self, first, last=None):
        self.entry.delete(first, last)

    def get(self):
        """Override of widgets get method. Redirects call to Entry from bounding Frame. 
        """
        return self.entry.get()

    def set(self, value):
        self.delete(0, tk.END)
        self.insert(0, value)

    def grid(self, sticky=("we"), **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
         tk.W)"""
        super().grid(sticky=sticky, **kwargs)

    def _on_browse(self):
        """Handles presses of the widgets Browse button.
        
        Sets Entry text to selection. Invokes on_select if supplied, passes selection.
        """
        selection_str = filedialog.askdirectory()
        if selection_str and selection_str != "":
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selection_str)
            if self.on_select:
                self.on_select(selection_str)


class LabelInput(ttk.Frame):
    """A widget containing a label and input together. 
    
    Accepts various ttk & custom input widgets. Creates a paired
    ttk.Label to the left of those which lack a suitable label of their own.
    Ensures columns span entire widget contained. Optional placeholder
    functionality and end-user toggle for enabling/disabling fields.
    """

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
        self.input.grid(row=0, column=2, sticky="we")

        if placeholder:
            self.set_placeholder(placeholder)

        if toggle_enable:
            enabled = self.enabled = tk.BooleanVar(value=True)
            self.toggle_enable_checkbutton = ttk.Checkbutton(
                self, variable=enabled
            )
            self.toggle_enable_checkbutton.grid(row=0, column=0)

        self.columnconfigure(1, minsize=115)

        style = ttk.Style()
        style.configure("prominent.TEntry", foreground="#ffffff")
        style.configure("non_prominent.TEntry", foreground="#969799")

    def grid(self, sticky=("we"), **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
         tk.W)"""
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        """Get handling for various supported input widgets.
        """
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get("1.0", tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return

    def set(self, value, *args, **kwargs):
        """Set handling for widgets expecting tk.BooleanVar, widgets with
        variables, and tick/untick where appropriate.
        """
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

        elif type(self.input) == tk.Text:  # if tk.Text...
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
            self.set("")
            self.set_prominent(True)

    def set_placeholder(self, value):
        """Set the value that will appear in the input widget with non-prominent
        syling until changed by user interaction.
        
        Useful as reference for tracking dirtied values or deviation from value
        defaults.

        Args:
            value : Value to be used.
        """
        self.placeholder = value
        self.input.bind("<FocusIn>", self._on_focus_in)
        self.input.bind("<FocusOut>", self._on_focus_out)
        self._populate_placeholder()

    def set_prominent(self, value):
        """Change prominence of input styling.
        Args:
            value (bool): Prominent styling if True, non-prominent if False.
        """
        if value == True:
            self.input.configure(style="prominent.TEntry")
        else:
            self.input.configure(style="non_prominent.TEntry")

    def get_prominent(self):
        return self.input["style"] == "prominent.TEntry"

    def _on_focus_in(self, event):
        self._clear_placeholder()

    def _on_focus_out(self, event):
        if self.get() == "":
            self._populate_placeholder()


class IniFrame(ttk.Frame):
    """A frame with controls for editing an Ini configuration supplied as a dictionary.
    
    Use get to retrieve its values in a similarly structured dictionary."""

    def __init__(
        self,
        parent,
        ini_dict=None,
        ini_defaults_dict=None,
        placeholder_FX=True,
        human_readable_labels=False,
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.inputs = {}
        self.ini = ini_dict
        self.defaults = ini_defaults_dict

        self.placeholder_FX = placeholder_FX
        self.human_readable_labels = human_readable_labels

        self._initialize_fields()
        self._populate_defined()

    def _initialize_fields(self):
        """Creates sections and their field inputs with supplied defaults for placeholder fx (if enabled).
        """
        for section in self.defaults:
            section_label_frame = ttk.LabelFrame(self, text=section)
            self.inputs[section_label_frame] = {}
            for key, value in self.defaults[section].items():
                input_class = ttk.Entry
                if "_directory" in key:
                    input_class = DirectorySelectEntry
                label = key
                if self.human_readable_labels:
                    label = str(key).replace("_", " ").title()
                self.inputs[section_label_frame][key] = LabelInput(
                    parent=section_label_frame,
                    label=label,
                    input_class=input_class,
                )
                if self.placeholder_FX:
                    self.inputs[section_label_frame][key].set_placeholder(
                        value
                    )
                else:
                    self.inputs[section_label_frame][key].set(value)
                self.inputs[section_label_frame][key].pack(
                    side=tk.TOP, expand=True, fill=tk.X
                )
            section_label_frame.pack(side=tk.TOP, expand=True, fill=tk.X)

    def _populate_defined(self):
        """Populates field inputs whose values are supplied in primary Ini dictionary.
        """
        for section in self.inputs:
            for key, _input in self.inputs[section].items():
                section_name = section["text"]
                if key in self.ini[section_name]:
                    defined_value = self.ini[section_name][key]
                    _input.set(defined_value)
                    if self.placeholder_FX:
                        _input.set_prominent(True)

    def get(self):
        """Gets data from inputs in the frame. Does not include placeholder input values.
        """
        data = {}
        for section in self.inputs:
            section_name = section["text"]
            data[section_name] = {}
            for key, entry in self.inputs[section].items():
                if entry.get_prominent():
                    data[section_name][key] = entry.get()
        return data


class PowerButton(ttk.Frame):
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


class BarSeparator(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)
        self.photo_image = tk.PhotoImage(
            master=master, file=r"img/custom-tk-bar-sep.png"
        )
        self.configure(image=self.photo_image)

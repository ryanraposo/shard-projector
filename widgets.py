import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import ThemedTk
import os, json, configparser

import dstctl

class WidgetConsoleView(ttk.Frame):
    """
    """
    def __init__(
        self,
        parent=None,
        width=450,
        **kwargs
    ):
        super().__init__(parent)   
        # Frame     
        self.configure(width=width)
        # Style
        self.style = ttk.Style()
        self.style.configure('WidgetConsoleView.Treeview', foreground='#3eb489', background='#353535', font='TkDefault, 7')  
        # Tree
        self.tree = ttk.Treeview(self, style='WidgetConsoleView.Treeview') # Tree
        self.tree.column("#0", width=width, stretch=False)
        # Placement
        self.rowconfigure(0, weight=1)
        self.tree.grid(column=0, row=0, sticky=('nswe'))


    def write_line(self, line, scroll_matching=True):
        item = self.tree.insert("", tk.END, text=line)
        if scroll_matching:
            self.tree.see(item)

    def set_heading(self, text):
        self.tree.heading('#0', text=text)

    def place(self, **kwargs):
        super().place(**kwargs)
        self.tree.grid(column=0, row=0, sticky=('nswe'))
        print(self['height'])


def test_widget_console_view(test_window_geometry='960x720'):
    parent = ThemedTk(theme='equilux') 
    parent.geometry(test_window_geometry)
    parent.configure(bg="#424242")
    parent.wm_deiconify()

    widget = WidgetConsoleView(parent=parent, view_width=460)
    widget.place(x=0,y=0)
    for i in range(100):
        widget.write_line('[000.' + str(i) + ']: ' + 'WOWOWOWOWOWOWOWOHHHHHHHHHWOWOWOWOWOOOSSSSSSSSBITCHWOWOWOWOWOWOWOWOHHHHHHHHHWOWOWOWOWOOOSSSSSSSSBITCHWOWOWOWOWOWOWOWOHHHHHHHHHWOWOWOWOWOOOSSSSSSSSBITCH')
    
    parent.mainloop()


class WidgetDirectorySelect(ttk.Frame):
    """A ttk-styled Entry and Browse button for selecting a directory path. Use attribute var to access value."""

    def __init__(self, parent):
        super().__init__(parent)
        
        self.var = tk.StringVar()

        self.entry = ttk.Entry(self, textvariable=self.var, width=35)
        self.entry.grid(row=0, column=0)
        
        self.browse = ttk.Button(self, command=self.on_browse, text="Browse")
        self.browse.grid(row=0, column=1)

    def on_browse(self):
        path = filedialog.askdirectory(master=self)
        self.var = path

        shortened_path = self.shortify(path)

        self.entry.delete(0, tk.END)
        self.entry.insert(0, shortened_path)

    def shortify(self, path):
        path_split = str(path).split('/')

        path_start = path_split[0] + "/..."
        path_end = ''

        space_left = self.entry['width'] - len(path_start)

        path_end_split = path_split[1:]
        path_end_split.reverse()
        for segment in path_end_split:
            proposed_concatenation = "/" + segment + path_end
            if len(proposed_concatenation) < space_left:
                path_end = proposed_concatenation
            else:
                break

        shortened_path = path_start + path_end

        return shortened_path


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
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Radiobutton, ttk.Button):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
        # Label
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=1) # sticky=(tk.W))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=0, column=2) #, sticky=(tk.E))

        if toggle_enable:
            enabled = self.enabled = tk.BooleanVar(value=True)
            self.toggle_enable_checkbutton = ttk.Checkbutton(self, variable=enabled)
            self.toggle_enable_checkbutton.grid(row=0, column=0)

        self.columnconfigure(1, minsize=115)

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
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
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:  # if ttk.Text...
            self.input.delete("1.0", tk.END)  # delete row 1 char 0 to the end
            self.input.insert("1.0", value)  # insert value at row 1 char 0
        else:  # input is a ttk.Entry with no variable
            self.input.delete(0, tk.END)  # delete row 1 char 0 to the end
            self.input.insert(0, value)  # insert value at row 1 char 0


class FrameConfigure(ttk.Frame):
    """Accepts a dictionary representing an .ini file and frame containing LabelInputs for
    viewing and configuring the values. Use get to retrieve its values in a similarly structured dictionary."""

    def __init__(self, parent, target_configuration=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.inputs = {}
        self.target_configuration = target_configuration
        self._initialize_widgets()

    def _get_structure(self):
        if "GAMEPLAY" in self.target_configuration.keys():
            return self._get_cluster_ini_structure()
        return self._get_shard_ini_structure()

    def _get_cluster_ini_structure(self):
        with open("./data/ini/cluster_configuration.json") as json_file:
            cluster_config_structure = dict(json.load(json_file))
            return cluster_config_structure
    
    def _get_shard_ini_structure(self):
        with open("./data/ini/shard_configuration.json") as json_file:
            shard_config_structure = dict(json.load(json_file))
            return shard_config_structure

    def _initialize_widgets(self):
        """Loops through """

        configuration_json = self._get_structure()
        x = 0
        for section in configuration_json.keys():
            y = 0
            frmSection = ttk.Labelframe(self, text=section)
            frmSection.grid(row=x, column=0)
            for option in configuration_json[section].keys():
                self.inputs[option] = WidgetLabelInput(
                    parent=frmSection,
                    toggle_enable=False,
                    label=option,
                    input_class=ttk.Entry,
                    label_args={},
                )
                
                self.inputs[option].grid(row=y, column=0)
                if self.target_configuration:
                    try:
                        target_section = self.target_configuration[section]
                        self.inputs[option].set(target_section[option])
                    except:
                        pass
                y += 1
            x += 1

    def grid(self, sticky=(tk.W + tk.E), fill=tk.BOTH, expand=True, **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
        tk.W)"""
        super().grid(sticky=sticky, fill=fill, expand=expand **kwargs)

    def get(self):  # TODO fix get method in configure cluster frame so that it returns sections as in the structure json
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data


class DialogConfirmShardDirectories(tk.Toplevel):
    def __init__(self, parent, detected_shard_directories):
        super().__init__(parent)
        # Root
        self.wm_iconify()
        self.title("Confirm shard directories...")

        dialog_frame = ttk.Frame(self)
        dialog_frame.grid(row=0, column=0)

        self.vars = []

        self.inputs = {}
        row_count = 0
        for path in detected_shard_directories:
            var = tk.StringVar()
            self.vars.append(var)
            frame_shard = ttk.Frame(dialog_frame)
            self.inputs[row_count] = WidgetLabelInput(
                parent=frame_shard,
                toggle_enable=True,
                label=os.path.basename(path),
                input_var=var,
                input_args={"width":50}
            )
            var.set(path)
            self.inputs[row_count].grid(row=row_count, column=0)
            ttk.Button(frame_shard, text="Browse").grid(row=row_count, column=1)
            frame_shard.grid(row=row_count, column=0)
            row_count += 1

        self.button_confirm = ttk.Button(dialog_frame, text="Confirm", command=self.on_confirm)
        self.button_confirm.grid(row=row_count, column=0, sticky=tk.E, padx=8, pady=8)

    def on_confirm(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        submitted_directories = []
        for each in self.vars:
            submitted_directories.append(each.get())
        return submitted_directories


class DialogConfigureServer(tk.Toplevel):
    def __init__(self, parent, server):
        super().__init__(parent)
        self.title("Settings")
        self.configure(bg="#424242")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()

        self.server = server        

        self.notebook = self._initialize_notebook()

        self.page_cluster = FrameConfigure(self.notebook, server.config.as_dict())
        self.notebook.add(child=self.page_cluster, text="Cluster")        

        for shard in server.shards:
            page = FrameConfigure(self.notebook, shard.configuration.as_dict())
            self.notebook.add(page, text=shard.name)

        print(self.notebook.tabs())

        self.apply = ttk.Button(self, text="Apply", command=self._on_apply)
        self.cancel = ttk.Button(self, text = "Cancel", command=self._on_cancel)

    
    def _initialize_notebook(self):
        notebook = ttk.Notebook(self) # , width=400, height=700)
        notebook.pack(fill=tk.BOTH, expand=True, padx=3, pady=3)
        return notebook

    def _on_apply(self):
        pass

    def _on_cancel(self):
        pass

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        
    def close(self):
        self.destroy()


class DialogCustomCommand(tk.Toplevel):
    """Dialog window for entering a custom command to be issued to all shards belonging to the current server."""
    def __init__(self, parent, callback_fn):
        super().__init__(parent)
        self.callback_fn = callback_fn
        self.configure(bg="#424242") #TODO: May not be necessary, but appears white when testing with simple instantiation at the bottom of this module. Widgets seem to inherit styling, though 
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.wm_iconify()
        self.title("Enter a custom command...")

        dialog_frame = ttk.Frame(self)
        dialog_frame.grid(row=0, column=0)

        self.entry_custom_command = ttk.Entry(
            master=self,
            textvariable=tk.StringVar(),
            width=30
        )
        self.entry_custom_command.grid(row=0,column=0)
        
        self.button_submit_command = ttk.Button(
            master=self,
            text="Submit",
            command=self._on_confirm,
            width=20
        )
        self.button_submit_command.grid(row=0,column=1)

    def _on_confirm(self, event=None):
        try:
            user_entered_command = str(self.entry_custom_command.get())
            if len(user_entered_command) > 0:
                self.callback_fn(user_entered_command) 
        except:
            tk.messagebox.showwarning(
                title="Custom Command",
                message="Failed to issue command to server"
                )
        finally:
            self.destroy()

    def _on_cancel(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()


def test_dialog(cls_dialog, **kwargs):

    parent = ThemedTk(theme='equilux') 
    parent.wm_iconify()

    server = dstctl.DedicatedServer("C:/Users/ryanr/source/dstctl/data/Eden", parent)
    
    dialog = cls_dialog(parent, server)
    dialog.show()

    parent.mainloop()


if __name__ == "__main__":
    test_widget_console_view()


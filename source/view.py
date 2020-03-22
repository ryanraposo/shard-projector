import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser
from ttkthemes import ThemedTk

import os, json

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


class FrameConfigure(ttk.Frame):
    """Accepts a dictionary representing an .ini file and frame containing LabelInputs for
    viewing and configuring the values. Use get to retrieve its values in a similarly structured dictionary."""

    def __init__(self, parent, target_configuration=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.section_frames = {}
        self.inputs = {}
        self.target_configuration = target_configuration
        self.defaults = self._get_defaults()
        self._initialize_widgets()
        self._populate_defined()

    def _get_defaults(self):
        if "GAMEPLAY" in self.target_configuration.keys():
            return self._get_cluster_ini_defaults()
        return self._get_shard_ini_defaults()

    def _get_cluster_ini_defaults(self):
        with open("./data/ini/cluster_configuration.json") as json_file:
            cluster_config_structure = dict(json.load(json_file))
            return cluster_config_structure

    def _get_shard_ini_defaults(self):
        with open("./data/ini/shard_configuration.json") as json_file:
            shard_config_structure = dict(json.load(json_file))
            return shard_config_structure

    def _initialize_widgets(self):
        """Loops through defaults, creating a dict (self.inputs) that mirrors the structure but where
        config values are the inputs on the form."""
        x = 0
        for section in self.defaults.keys(): # Iterate structure (sections, keys, defaults)
            y = 0
            label_frame = ttk.Labelframe(self, text=section)
            label_frame.grid(row=x, column=0)
            self.inputs[section] = {} # Create key in self.inputs for each section       
            for key in self.defaults[section].keys(): # Iterate keys in each section of defaults
                self.inputs[section][key] = widgets.WidgetLabelInput( # Create InputLabel for each option
                    parent=label_frame,
                    toggle_enable=False,
                    label=key,
                    input_class=ttk.Entry,
                    label_args={},
                    placeholder=self.defaults[section][key]['default']
                )
                self.inputs[section][key].grid(row=y, column=0)
                y += 1
            x += 1
    
    def _populate_defined(self):
        """Iterate self.inputs and populate with values from defaults, indicating
        with prominent (white) text color"""
        for section in self.inputs:
            fields = self.inputs[section]
            for key, label_input in fields.items():
                try:
                    defined_value = self.target_configuration[section][key]
                except:
                    print('%s : %s not defined in user config'%(section, key))
                else:
                    label_input.set_prominent(True)
                    label_input.set(defined_value)
        
    def grid(self, sticky=(tk.W + tk.E), fill=tk.BOTH, expand=True, **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
        tk.W)"""
        super().grid(sticky=sticky, fill=fill, expand=expand ** kwargs)

    def get(self):
        """Gets a dict of data from inputs in the frame. Does not return non-prominent placeholder input values
        """
        data = {}
        for section in self.inputs:
            data[section] = {}
            for key, entry in self.inputs[section].items():
                if entry.get_prominent(): # Prominent in this case represents a non-default value, prevents writing unnecessary values to file
                    data[section][key] = entry.get()
        return data


class DialogConfigureServer(tk.Toplevel):
    def __init__(self, parent, server, fn_on_apply):
        super().__init__(parent)
        self.title("Settings")
        self.configure(bg="#424242")
        self.wm_transient(parent)

        self.fn_on_apply = fn_on_apply

        self.server = server

        self.notebook = ttk.Notebook(self)
        self.tabs = {}
        self.tabs[server] = FrameConfigure(self.notebook, server.config.as_dict())
        self.notebook.add(child=self.tabs[server], text="Cluster")
        for shard in server.shards:
            self.tabs[shard] = FrameConfigure(self.notebook, shard.config.as_dict())
            self.notebook.add(self.tabs[shard], text=shard.name)

        self.apply = ttk.Button(self, text="Apply", command=self._on_apply)

        self.cancel = ttk.Button(self, text="Cancel", command=self._on_cancel)

        self.notebook.grid(column=0,row=0, padx=3, pady=3)
        self.apply.grid(column=0,row=1,sticky=('w'))
        self.apply.grid(column=0,row=2,sticky=('w'))

    def _on_apply(self):
        """Retrieves a dict representing an ini config from each
        tab of the notebook, and passes it to the fn_on_apply supplied on instantiation"""

        for target, tab in self.tabs.items():
            data = tab.get()
            self.fn_on_apply(target, data)

    def _on_cancel(self):
        pass

    def show(self):
        self.wm_deiconify()
        self.wait_window()

    def close(self):
        self.destroy()


class DialogConfirmShardDirectories(tk.Toplevel):
    def __init__(self, parent, detected_shard_directories):
        super().__init__(parent)
        # Root
        self.wm_iconify()
        self.title("Confirm shard directories...")
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()

        dialog_frame = ttk.Frame(self)
        dialog_frame.grid(row=0, column=0)

        self.vars = []

        self.inputs = {}
        row_count = 0
        for path in detected_shard_directories:
            var = tk.StringVar()
            self.vars.append(var)
            frame_shard = ttk.Frame(dialog_frame)
            self.inputs[row_count] = widgets.WidgetLabelInput(
                parent=frame_shard,
                toggle_enable=True,
                label=os.path.basename(path),
                input_var=var,
                input_args={"width": 60}
            )
            var.set(path)
            self.inputs[row_count].grid(row=row_count, column=0)
            ttk.Button(frame_shard, text="Browse").grid(row=row_count, column=1)
            frame_shard.grid(row=row_count, column=0)
            row_count += 1

        self.button_confirm = ttk.Button(
            dialog_frame, text="Confirm", command=self.on_confirm
        )
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


class DialogCustomCommand(tk.Toplevel):
    """Dialog window for entering a custom command to be issued to all shards belonging to the current server."""

    def __init__(self, parent):
        super().__init__(parent)
        self.configure(
            bg="#424242"
        )  # TODO: May not be necessary, but appears white when testing with simple instantiation at the bottom of this module. Widgets seem to inherit styling, though
        self.lift()
        self.focus_force()
        self.grab_set()
        self.grab_release()
        self.wm_iconify()
        self.title("Enter a custom command...")
        self.var = ""

        dialog_frame = ttk.Frame(self)
        dialog_frame.grid(row=0, column=0)

        self.entry_custom_command = ttk.Entry(
            master=self, textvariable=tk.StringVar(), width=30
        )
        self.entry_custom_command.grid(row=0, column=0)

        self.button_submit_command = ttk.Button(
            master=self, text="Submit", command=self._on_confirm, width=20
        )
        self.button_submit_command.grid(row=0, column=1)

    def _on_confirm(self, event=None):
        try:
            user_entered_command = str(self.entry_custom_command.get())
            if len(user_entered_command) > 0:
                self.var = user_entered_command
        except:
            tk.messagebox.showwarning(
                title="Custom Command", message="Failed to issue command to server"
            )
        finally:
            self.destroy()

    def _on_cancel(self, event=None):
        self.destroy()

    def show(self):
        """
        Displays the dialog. Returns inputted string.
        """
        self.wm_deiconify()
        self.wait_window()
        return self.var

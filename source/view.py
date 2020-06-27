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

        widgets.BarSeparator(self).grid(row=0, column=2)

        gamemode_info_field = ttk.Label(self, text="Gamemode:", style="blendBg.TLabel")
        gamemode_info_field.grid(row=0,column=3)
        self.gamemode_info_value = ttk.Label(self, style="white.TLabel")
        self.gamemode_info_value.grid(row=0,column=4)
        self.columnconfigure(4, minsize=50)

        widgets.BarSeparator(self).grid(row=0, column=5)

        players_info_field = ttk.Label(self, text="Players:", style="blendBg.TLabel")
        players_info_field.grid(row=0, column=6)
        self.players_info_value = ttk.Label(self, style="white.TLabel")
        self.players_info_value.grid(row=0, column=7)
        self.columnconfigure(7, minsize=10)

        widgets.BarSeparator(self).grid(row=0, column=8)

        self.btn_configure = ttk.Button(master=self, text="Configure", command=command_configure)
        self.btn_configure.grid(row=0, column=9, sticky='e')
        self.columnconfigure(9, weight=1)

        for i in range(9):
            self.columnconfigure(i, pad=10)



    def debug(self):
        self.name_info_value.configure(text="Frontbutt Beach")
        self.gamemode_info_value.configure(text="Endless")
        self.players_info_value.configure(text="8")


class DialogConfigureApplication(tk.Toplevel):
    """Application settings dialog.
    """
    def __init__(
        self,
        application=None
    ):
        super().__init__(master=application.window)
        self.title("Shard Projector Settings")
        self.configure(bg="#424242")
        self.wm_transient(application.window)

        self.root_frame =ttk.Frame(self)        

        config = application.config.as_dict()
        config_defaults = application.config.defaults

        configuration_frame = widgets.ConfigurationFrame(
            parent=self.root_frame,
            ini_dict=config,
            ini_defaults_dict=config_defaults, 
            placeholder_FX=True,
            human_readable_labels=True
        )
        configuration_frame.grid(row=0, column=0)


        btn_apply = ttk.Button(self.root_frame, text='Apply', command=lambda: application.config.update_from_dict(configuration_frame.get()))
        btn_apply.grid(row=1, column=0)
        
        self.root_frame.grid(row=0,column=0, sticky='nswe')
    

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
        self.tabs[server] = widgets.ConfigurationFrame(
            parent=self.notebook,
            ini_dict=server.config.as_dict(),
            ini_defaults_dict=server.config.defaults
        )

        self.notebook.add(child=self.tabs[server], text="Cluster")
        for shard in server.shards:
            self.tabs[shard] = widgets.ConfigurationFrame(
                parent=self.notebook,
                ini_dict=shard.config.as_dict(),
                ini_defaults_dict=shard.config.defaults
            )
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
    def __init__(self, parent, detected_shard_directories, fn_callback):
        super().__init__(parent)
        self.title("Confirm shard directories...")
        self.grab_set()
        self.transient(parent)

        self.detected_shard_directories = detected_shard_directories
        self.fn_callback = fn_callback

        self.inputs = {}

        self.root_frame = ttk.Frame(self)

        self._initialize_widgets()
        
        self.root_frame.grid(row=0, column=0, sticky='nswe')

    def _initialize_widgets(self):
        row_count = 0
        for path in self.detected_shard_directories:
            frame_shard = ttk.Frame(self.root_frame)
            self.inputs[row_count] = widgets.LabelInput(
                parent=frame_shard,
                toggle_enable=True,
                label=os.path.basename(path),
                input_class=widgets.DirectorySelectEntry
            )
            self.inputs[row_count].set(path)
            self.inputs[row_count].grid(row=row_count, column=0)
            frame_shard.grid(row=row_count, column=0)
            row_count += 1

        self.button_confirm = ttk.Button(
            self.root_frame, text="Confirm", command=self.on_confirm
        )
        self.button_confirm.grid(row=row_count, column=0, sticky=tk.E, padx=8, pady=8)

    def on_confirm(self):
        submitted_directories = []
        for each in self.inputs.values():
            submitted_directories.append(each.get())
        self.fn_callback(submitted_directories)        
        self.destroy()
        

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

        root_frame = ttk.Frame(self)
        root_frame.grid(row=0, column=0)

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


class DialogInstallSteamCMD:
    def __init__(self, task_fn):
        confirm = messagebox.askokcancel(
            title="Task",
            message="This will attempt to install SteamCMD as an add-in.\n\nNote: Shard Projector will always prioritize add-ins to external installations. Delete the contents of the add-ins folder to safely uninstall them."
        )

        if confirm == True:
            try:
                task_fn()
            except FileExistsError:
                messagebox.showinfo("Info", "The SteamCMD add-in is already installed!")
            except Exception as e:
                messagebox.showerror("Error", "Installation of the SteamCMD add-in failed with error: " + e)
    

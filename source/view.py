import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser 
from ttkthemes import ThemedTk

import os, json
from queue import Queue, Empty
from threading import Thread
from subprocess import Popen, PIPE

import widgets

from util import iter_except
from constants import *


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
        self.iconbitmap(os.path.join(DIR_IMG, "icon.ico"))
        self.configure(bg="#424242")
        self.grab_set()
        # Centers dialog
        application.window.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        self.root_frame =ttk.Frame(self)        

        config = application.config.as_dict()
        config_defaults = application.config.defaults

        configuration_frame = widgets.IniFrame(
            parent=self.root_frame,
            ini_dict=config,
            ini_defaults_dict=config_defaults, 
            placeholder_FX=True,
            human_readable_labels=True
        )
        configuration_frame.grid(row=0, column=0)

        lbl_nullrenderer_priority_reminder = ttk.Label(self.root_frame,
            text="""
    NOTE: an external nullrenderer path can be defined here,
    but SteamCMD Add-In nullrenderer always takes priority.

    To uninstall add-ins, delete folders found in:
    'shard_projector/add-ins'
        """
            # relief="groove"
        )
        lbl_nullrenderer_priority_reminder.grid(row=1, column=0)

        btn_apply = ttk.Button(self.root_frame, text='Apply', command=lambda: application.config.update_from_dict(configuration_frame.get()))
        btn_apply.grid(row=2, column=0)
        
        self.root_frame.grid(row=0,column=0, sticky='nswe')
    

class DialogConfigureServer(tk.Toplevel):
    def __init__(self, parent, server, fn_on_apply):
        super().__init__(parent)
        self.title("Settings")
        self.iconbitmap(os.path.join(DIR_IMG, "icon.ico"))
        self.configure(bg="#424242")
        self.grab_set()
        # Centers dialog
        parent.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())
        
        self.fn_on_apply = fn_on_apply

        self.server = server

        self.notebook = ttk.Notebook(self)
        self.tabs = {}
        self.tabs[server] = widgets.IniFrame(
            parent=self.notebook,
            ini_dict=server.config.as_dict(),
            ini_defaults_dict=server.config.defaults
        )

        self.notebook.add(child=self.tabs[server], text="Cluster")
        for shard in server.shards:
            self.tabs[shard] = widgets.IniFrame(
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
        self.iconbitmap(os.path.join(DIR_IMG, "icon.ico"))
        self.grab_set()
        # Centers dialog
        parent.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

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
        self.title("Enter a custom command...")
        self.iconbitmap(os.path.join(DIR_IMG, "icon.ico"))
        self.configure(bg="#424242")
        # Centers dialog
        parent.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())
        self.grab_set()

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
    def __init__(self, fn_download, fn_install):
        confirm = messagebox.askokcancel(
            title="Task",
            message="This will attempt to install SteamCMD as an add-in.\n\nNote: Shard Projector will always prioritize add-ins to external installations. Delete the contents of the add-ins folder to safely uninstall them."
        )
        if confirm == True: # TODO: refactor
            try:
                exec_path = fn_download()
                messagebox.showinfo("Shard Projector", "SteamCMD Add-In downloaded successfully. Press OK to continue the installation.")
                fn_install(exec_path)
                messagebox.showinfo("Shard Projector", "SteamCMD Add-In was successfully installed.")
            except FileExistsError:
                messagebox.showinfo("Info", "The SteamCMD Add-In is already installed!")
            except Exception as e:
                messagebox.showerror("Error", "Installation of the SteamCMD Add-In failed with error: " + e)

    
class DialogStatus(tk.Toplevel):
    """Dialog for indicating status of various application activities.

    Args:
        parent (Tk): Tk window object responsible for spawning the dialog and handling callbacks
    """    

    def __init__(self, parent, blocking_enabled=False):
        super().__init__(parent)
        self.title("")
        self.iconbitmap(os.path.join(DIR_IMG, "icon.ico"))
        if blocking_enabled:
            self.grab_set()

        self.root_frame = ttk.Frame(self)
        self.status_view = widgets.ConsoleView(self, 400, 10)

        self.status_view.grid(row=0, column=0)
        self.root_frame.grid(row=0, column=0, sticky='nswe')


    def update_status(self, line):
        """Updates dialog's status view.
        """
        if line:
            self.status_view.write_line(line)
#!/usr/bin/python
"""
Desktop control application for Don't Starve Together dedicated servers.
"""
import sys
import os
import json
import shutil
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

import configparser

from queue import Queue, Empty


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class Shard:
    """Represents primarily the subprocess instance for server shards and its in/out pipes."""
    
    def __init__(self, cmd, name):
        self.cmd = cmd
        self.name = name
        self.output_queue = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.input_queue = Queue(maxsize=1024)

    def start(self):
        cwd = os.path.realpath("C:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
        self.process = Popen(self.cmd, stdout=PIPE, stdin=PIPE, shell=True, cwd=cwd)
        self.q = Queue(maxsize=1024)
        self.thread_reader = Thread(target=self._update_output, args=[self.q])
        self.thread_reader.daemon = True
        self.thread_reader.start()
    
    def stop(self):
        """Terminates process associated with shard. Returns Exception on failure."""
        try:
            self.process.terminate()
            self.process = None
        except:
            return Exception # TODO: Non-standard error handling

    def _update_output(self, q):
        """Adds stdout of associated process to shard's output queue."""
        if self.is_started():
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b''):
                        q.put(line)
            finally:
                q.put(None)

    def get_output(self): # Schedule me
        """Returns output queue of the shard."""
        if self.is_started():
            for line in iter_except(self.q.get_nowait, Empty): # display all 
                if line is None:
                    return None
                else:
                    return line

    def write_input(self, line):
        """Writes the input queue of the shard to the stdin of its associated process."""
        if self.is_started():
            try:
                with self.process.stdin as pipe:
                    pipe.write(line.encode())
                print(line + ' recieved by ' + self.name)
            except:
                print(line + ' NOT recieved by ' + self.name)

    def status(self):
        """Returns 'UP' if associated process is found, and 'DOWN' if not.""" 
        if self.is_started():
            poll = self.process.poll()
            if poll == None:
                return "UP"
            else:
                return "DOWN"
    
    def is_started(self):
        return hasattr(self,"process")


class DedicatedServer:
    """Represents the configuration directory for a given server instance. Note: expects within directory_path subdirectory 'Master' and optionally 'Slave' or 'Caves'."""

    class NonexistentDirectory(Exception): pass

    class InvalidServerDirectory(Exception): pass


    def __init__(self, directory_path):
        try:
            assert self.is_valid_server_config(directory_path)
            self.root_path = os.path.abspath(directory_path)
            self.master_config = self._get_shard_config('Master')
            self.cluster_config = self._get_cluster_config()
            try:
                self.slave_config = self._get_shard_config('Caves')
            except:
                self.slave_config = self._get_shard_config('Slave')
        except:
            raise ValueError

    def is_valid_server_config(self, directory_path):
        #Check for real path, server.ini, clustertoken.txt, at least one folder containing cluster.ini
        root_file_reqs = ["cluster.ini", "cluster_token.txt"]
        if os.path.isdir(os.path.abspath(directory_path)): # Check 1: Real path
            directory_root_contents = os.listdir(directory_path)
            if all(item in directory_root_contents  for item in root_file_reqs): # Check 2: contains server.ini and clustertoken.txt
                for member in directory_root_contents: 
                    full_member_path = os.path.join(directory_path, member)
                    if os.path.isdir(full_member_path): # Check 3: contains at least one subdirectory containing cluster.ini
                        if "server.ini" in os.listdir(full_member_path):
                            return True
        return False

    def _get_shard_config(self, dirname):
        try:
            shard_path = os.path.join(self.root_path, dirname)
            config = configparser.ConfigParser()
            config.read(os.path.join(shard_path, 'server.ini'))
            shard_config = as_dict(config)
        except:
            raise ValueError
        else:
            return shard_config
    
    def _get_cluster_config(self):
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(self.root_path, 'cluster.ini'))
            cluster_config = as_dict(config)
        except:
            raise ValueError
        else:
            return cluster_config


class ServerControl:
    """Main window of the application. Displays output from shards and is host to various server controls."""
    def __init__(self, root):
        self.root = root
        self.initialize_ui()

        nullrenderer = os.path.realpath("C:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe")     
        self.master = Shard([nullrenderer, "-console_enabled", "-cluster", "Eden", "-shard", "Master"],'MASTER')
        self.slave = Shard([nullrenderer, "-console_enabled", "-cluster", "Eden", "-shard", "Caves"],'SLAVE')

        # self.settings()

        self.update()

    def initialize_ui(self):
        """Setup widgets and styling of main window."""
        
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("DST Server Control")
        icon_path = os.path.join("./", "dstctl.ico")
        self.root.iconbitmap(icon_path)
        self.root.configure(bg="#424242")

        # TTK Style
        style = ttk.Style()
        text_font = ('TkDefaultFont', '14')

            # Combobox
        self.root.option_add('*TButton*Label.font', text_font)
        self.root.option_add('*TCombobox*Listbox.background', "#424242")
        self.root.option_add('*TCombobox*Listbox.selectBackground', '#525252') # change highlight color

        # Widgets
            # Top Bar
        self.frmTopBar = ttk.Frame(root, height=20, width=761)
        self.frmTopBar.place(x=21, y=10)
                # Server Select
        # self.server_picker = ServerPicker(self.frmTopBar)
        # self.server_picker.widget.grid(row=0, column=0)
                # Server config
        self.entServer = ttk.Entry(self.frmTopBar, width=25)
        self.entServer.grid(row=0, column=0)

        self.btnSelectServer = ttk.Button(self.frmTopBar, command=self.select_server, text='Browse')
        self.btnSelectServer.grid(row=0, column=1)
        
        # self.icon_settings_photo_image = ImageTk.PhotoImage(file="settings.png")
        # self.btnSettings = ttk.Button(self.frmTopBar, image=self.icon_settings_photo_image, command=self.settings, style='Img.TButton')
        # self.btnSettings.grid(row=0, column=2)
        # style.configure("Img.TButton", background="#424242", padding=[0,0,0,0])

        # Console Displays        
        self.lstMaster = ttk.Treeview(root,padding=[0,0,0,0])
        self.lstMaster.place(x=21, y=50, height=375, width=372)
        self.lstMaster.heading("#0",text="Master")

        self.lstSlave = ttk.Treeview(root)
        self.lstSlave.place(x=407, y=50, height=375, width=372)
        self.lstSlave.heading("#0",text="Caves")

        # Status Labels
        self.lblMasterStatus = ttk.Label(root, text='Status: ')
        self.lblMasterStatus.place(x=21,y=419)

        self.lblSlaveStatus = ttk.Label(root, text='Status: ')
        self.lblSlaveStatus.place(x=407,y=419)

        # Command Buttons
        self.cvsCommands = ttk.Frame(root)
        self.cvsCommands.place(x=473,y=440,height=100,width=300)
        style.configure('TFrame', background="#424242")
        
        self.btnStartAll = ttk.Button(self.cvsCommands, command=self.start_shards, text="Start")
        self.btnStartAll.grid(row=0,column=0)

        self.btnShutdownAll = ttk.Button(self.cvsCommands, command=self.shutdown_all, text="Shutdown")
        self.btnShutdownAll.grid(row=1,column=0)

        self.btnRegenerateWorld = ttk.Button(self.cvsCommands, command=self.regenerate_world, text="Regenerate")
        self.btnRegenerateWorld.grid(row=0,column=1)

        self.btnReset = ttk.Button(self.cvsCommands, command=self.reset, text="Reset")
        self.btnReset.grid(row=1,column=1)

        self.btnSave = ttk.Button(self.cvsCommands, command=self.save, text="Save")
        self.btnSave.grid(row=0,column=2)

        self.btnUpdate = ttk.Button(self.cvsCommands, command=self.update_steamcmd_dedicated_server, text="Update")
        self.btnUpdate.grid(row=1,column=2)

        self.btnQuit = ttk.Button(self.cvsCommands, command=self.quit, text="Quit")
        self.btnQuit.grid(row=3,column=2)

        # Other buttons
        
    def update(self):
        """Update GUI with information from Shards."""
        # If items in read queue, update GUI with them
        try:
            line = self.master.get_output()
            if line:
                item = self.lstMaster.insert("",END,text=line)
                self.lstMaster.see(item)
            line = self.slave.get_output()
            if line:
                item = self.lstSlave.insert("",END,text=line)
                self.lstSlave.see(item)
            if self.master.is_started():
                self.lblMasterStatus.configure(text='Status: ' + self.master.status())
            if self.slave.is_started():    
                self.lblSlaveStatus.configure(text='Status: ' + self.slave.status())
        finally:
            self.root.after(40, self.update)
    # Server-related methods
    def start_shards(self):
        self.master.start()
        self.slave.start()

    def shutdown_all(self):
        self.master.write_input("c_shutdown()")
        self.slave.write_input("c_shutdown()")
    
    def regenerate_world(self):
        self.master.write_input("c_regenerateworld()")
        self.slave.write_input("c_regenerateworld()")
    
    def reset(self):
        self.master.write_input("c_reset()")
        self.slave.write_input("c_reset()")

    def save(self):
        self.master.write_input("c_save()")
        self.slave.write_input("c_save()")   
        
    def update_status(self):
        self.lblMasterStatus.configure(text='MASTER status: ' + self.master.status())
        self.lblSlaveStatus.configure(text='SLAVE status: ' + self.slave.status())

    def update_steamcmd_dedicated_server(self):
        self.shutdown_all()
        os.system(os.path.realpath("./scripts/updatesteamcmd.bat"))
    # Application-related methods
    def settings(self):
        settings_dialog = SettingsDialog()
        settings_dialog.show(self.root)

    def select_server(self):
        selection = filedialog.askdirectory(initialdir=os.path.realpath("%CURRENTUSER%"),title = "Select a server directory...")
        try:
            self.server = DedicatedServer(selection)
            self.entServer.delete(0, END)
            self.entServer.insert(0, self.server.directory_path)
        except:
            messagebox.showwarning(title="DST Server Control", message=selection + " does not appear to be a valid dedicated server directory. Should contain server.ini, clustertoken.txt, at least one folder containing cluster.ini")

    def quit(self):
        self.shutdown_all()
        self.root.destroy()


class SettingsDialog:
    def show(self, mainwindow):
        self.window = Toplevel(mainwindow)
        self.window.geometry("400x300")
        self.window.resizable(0,0)
        self.window.title("Settings")
        self.window.configure(bg="#424242")
    
    def close(self):
        self.window.destroy()
       
def as_dict(config):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict

def kill_existing_server_procs():
    process = Popen('taskkill /F /IM "dontstarve_dedicated_server_nullrenderer.exe"', stdout=PIPE)
    stdout = process.communicate()[0]
    if "SUCCESS" in str(stdout):
        return "Existing server processes (dontstarve_dedicated_server_nullrenderer.exe) were found and terminated."
    elif "ERROR" in str(stdout):
        return None
                
kill_existing_server_procs()
root = ThemedTk(theme="equilux")
app = ServerControl(root)
root.mainloop()

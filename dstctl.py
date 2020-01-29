#!/usr/bin/python
"""
Control App for Ryan & Nicole's Don't Starve Together dedicated server.
"""
import sys
import os
import json
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk


from queue import Queue, Empty


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

def import_dst_colors():
    dst_colors = {}
    with open("./data/ui/dstcolor.json", 'r') as file:
        dst_colors = json.load(file)
    return dst_colors

class Shard:
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
            return Exception


    def _update_output(self, q):
        """Adds stdout of associated process to shard's output queue."""
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def get_output(self): # Schedule me
        """Returns output queue of the shard."""
        for line in iter_except(self.q.get_nowait, Empty): # display all 
            if line is None:
                return None
            else:
                return line
            
    def write_input(self, line):
        """Writes the input queue of the shard to the stdin of its associated process."""
        try:
            with self.process.stdin as pipe:
                pipe.write(line.encode())
            print(line + ' recieved by ' + self.name)
        except:
            print(line + ' NOT recieved by ' + self.name)

    def status(self):
        """Returns 'UP' if associated process is found, and 'DOWN' if not.""" 
        poll = self.process.poll()
        if poll == None:
            return "UP"
        else:
            return "DOWN"


class ServerControl:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x550")
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("DST Server Control")
        icon_path = os.path.join("./", "dstctl.ico")
        self.root.iconbitmap(icon_path)
        self.root.configure(bg="#424242")

        nullrenderer = os.path.realpath("C:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe")     
        self.master = Shard([nullrenderer, "-console_enabled", "-cluster", "Eden", "-shard", "Master"],'MASTER')
        self.slave = Shard([nullrenderer, "-console_enabled", "-cluster", "Eden", "-shard", "Caves"],'SLAVE')

        self.master.start()
        self.slave.start()

        DST_COLORS = import_dst_colors()

        BG_ROOT = DST_COLORS["screen"]["bg_medium"]
        FG_ROOT = DST_COLORS["screen"]["fg"]

        BG_TERM = DST_COLORS["frame"]["bg_dark"]
        FG_TERM = DST_COLORS["frame"]["fg"]
        RELIEF_TERM = GROOVE

        style = ttk.Style()
        
        # Console Displays
        self.lstMaster = ttk.Treeview(root,padding=[0,0,0,0])
        self.lstMaster.place(x=21, y=21, height=375, width=372)
        self.lstMaster.heading("#0",text="Master")

        self.lstSlave = ttk.Treeview(root)
        self.lstSlave.place(x=407, y=21, height=375, width=372)
        self.lstSlave.heading("#0",text="Caves")

        # Status Labels
        self.lblMasterStatus = ttk.Label(root, text='Status: ')
        self.lblMasterStatus.place(x=21,y=398)

        self.lblSlaveStatus = ttk.Label(root, text='Status: ')
        self.lblSlaveStatus.place(x=407,y=398)

        # Command Buttons
        self.cvsCommands = ttk.Frame(root)
        self.cvsCommands.place(x=473,y=429,height=100,width=300)
        style.configure('TFrame', background="#424242")
        
        self.btnStartAll = ttk.Button(self.cvsCommands, command=self.start_all, text="Start")
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
        
        self.update()

    def update(self):
        """Update GUI with items from both shard's output queues."""
        # If items in read queue, update GUI with them
        try:
            line = self.master.get_output()
            if line:
                print(line)
                item = self.lstMaster.insert("",END,text=line)
                self.lstMaster.see(item)
            line = self.slave.get_output()
            if line:
                item = self.lstSlave.insert("",END,text=line)
                self.lstSlave.see(item)
        finally:
            # self.lstMaster.configure()
            self.lblMasterStatus.configure(text='Status: ' + self.master.status())
            self.lblSlaveStatus.configure(text='Status: ' + self.slave.status())
            self.root.after(40, self.update)

    def shutdown_all(self):
        self.master.write_input("c_shutdown()")
        self.slave.write_input("c_shutdown()")

    def start_all(self):
        self.master.start()
        self.slave.start()
    
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

    def quit(self):
        self.shutdown_all()
        self.root.destroy()


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

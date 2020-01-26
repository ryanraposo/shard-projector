#!/usr/bin/python
"""
Control App for Ryan & Nicole's Don't Starve Together dedicated server.
"""
import sys
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
from tkinter import *


from queue import Queue, Empty

from shard import Shard



CWD = "c:\\steamcmd\\steamapps\\common\\Don't Starve Together Dedicated Server\\bin"
CMD_MASTER_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster RyansTestServer -shard Master"
CMD_SLAVE_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster RyansTestServer -shard Slave"

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

BG_ROOT = '#21252B'
FG_ROOT = '#CCCCCC'

BG_TERM = '#383E4A'
FG_TERM = '#409E68'
RELIEF_TERM = GROOVE


class ServerControl:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.configure(bg=BG_ROOT)        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.master = Shard(CMD_MASTER_START, CWD, 'MASTER')
        self.slave = Shard(CMD_SLAVE_START, CWD, 'SLAVE')

        self.master.start()
        self.slave.start()

        # Buttons
        self.btnStartAll = Button(root, command=self.start_all, text="Start", bg=BG_TERM, fg=FG_ROOT)
        self.btnStartAll.grid(row=1,column=1,pady=2)

        self.btnShutdownAll = Button(root, command=self.shutdown_all, text="Shutdown", bg=BG_TERM, fg=FG_ROOT)
        self.btnShutdownAll.grid(row=2,column=1,pady=2)

        self.btnRegenerateWorld = Button(root, command=self.regenerate_world, text="Regenerate World", bg=BG_TERM, fg=FG_ROOT)
        self.btnRegenerateWorld.grid(row=3,column=1)

        self.separator1 = Label(root,text="", height=2, bg=BG_ROOT)
        self.separator1.grid(row=4,column=1)

        self.btnQuit = Button(root, command=self.quit, text="Quit", bg=BG_TERM, fg=FG_ROOT)
        self.btnQuit.grid(row=5,column=1)
        
        # Labels
        self.lblMasterStatus = Label(root, text='MASTER status: ', fg=FG_ROOT, bg=BG_ROOT)
        self.lblMasterStatus.grid(row=1,column=0)

        self.lblSlaveStatus = Label(root, text='SLAVE status: ', fg=FG_ROOT, bg=BG_ROOT)
        self.lblSlaveStatus.grid(row=2,column=0)

        self.lstMaster = Listbox(root,
            font=(None, 8),
            width="60",
            height="25",
            bg=BG_TERM,
            fg=FG_TERM,
            relief=RELIEF_TERM,
            highlightcolor=BG_ROOT,
            highlightthickness=0)
        self.lstMaster.grid(row=0,column=0,ipadx=8, padx=11, ipady=8, pady=11)

        self.lstSlave = Listbox(root,
            font=(None, 8),
            width="60",
            height="25",
            bg=BG_TERM,
            fg=FG_TERM,
            relief=RELIEF_TERM,
            highlightcolor=BG_ROOT,
            highlightthickness=0)
        self.lstSlave.grid(row=0,column=1,ipadx=8, padx=11, ipady=8, pady=11)
        
        self.update()

    def update(self):
        """Update GUI with items from both shard's output queues."""
        # If items in read queue, update GUI with them
        try:
            line = self.master.get_output()
            if line:
                self.lstMaster.insert(END, [line])
                self.lstMaster.see(END)
            line = self.slave.get_output()
            if line:
                self.lstSlave.insert(END, [line])
                self.lstSlave.see(END)
        finally:
            self.lblMasterStatus.configure(text='MASTER status: ' + self.master.status())
            self.lblSlaveStatus.configure(text='SLAVE status: ' + self.slave.status())
            self.root.after(40, self.update)

    def shutdown_all(self):
        self.master.write_input("c_shutdown()")
        self.slave.write_input("c_shutdown()")

    def start_all(self):
        self.master.start()
        self.slave.start()
    
    def regenerate_world(self):
        self.master.write_input("c_regenerateworld()")

    def update_status(self):
        self.lblMasterStatus.configure(text='MASTER status: ' + self.master.status())
        self.lblSlaveStatus.configure(text='SLAVE status: ' + self.slave.status())

    def quit(self):
        self.shutdown_all()
        self.root.destroy()


root = Tk()
root.wm_protocol(name='WM_DELETE_WINDOW',func=root.quit)
app = ServerControl(root)
root.mainloop()

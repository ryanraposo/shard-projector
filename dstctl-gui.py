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
CMD_MASTER_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster RNDSTServer -shard Master"
CMD_SLAVE_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster RNDSTServer -shard Slave"


def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


def start_master():
    """Starts the Master server shard and returns the process"""
    proc = Popen(CMD_MASTER_START, stdout=PIPE, stdin=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
    return proc

def start_slave():
    """Starts the Slave server shard and returns the process"""
    proc = Popen(CMD_SLAVE_START, stdout=PIPE, stdin=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
    return proc


class ServerControl:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.configure(bg='#1D2024')        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.master = Shard(CMD_MASTER_START, CWD, 'MASTER')
        self.slave = Shard(CMD_SLAVE_START, CWD, 'SLAVE')

        self.master.start()
        self.slave.start()

        # self.btnReset = Button(root, command=self.reset, text="Reset")
        # self.btnReset.grid(row=1,column=1)

        self.btnShutdown = Button(root, command=self.shutdown, text="Shutdown")
        self.btnShutdown.grid(row=2,column=1)

        foreground = '#1D7D68'

        self.lstMaster = Listbox(root, font=(None, 8), width="60", bg='#000000', fg=foreground)
        self.lstMaster.grid(row=0,column=0,ipadx=4, padx=4, ipady=4, pady=4)

        self.lstSlave = Listbox(root, font=(None, 8), width="60", bg='#000000', fg=foreground)
        self.lstSlave.grid(row=0,column=1,ipadx=4, padx=4, ipady=4, pady=4)
        
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
            self.root.after(40, self.update)


    def shutdown(self):
        self.master.write_input("c_shutdown()")
        self.slave.write_input("c_shutdown()")

    def quit(self):
        self.shutdown()
        self.root.destroy()


root = Tk()
app = ServerControl(root)
root.mainloop()

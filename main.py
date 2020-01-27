#!/usr/bin/python
"""
Control App for Ryan & Nicole's Don't Starve Together dedicated server.
"""
import sys
import os
from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
import tkinter as tk


from queue import Queue, Empty


CWD = "c:\\steamcmd\\steamapps\\common\\Don't Starve Together Dedicated Server\\bin"
CMD_MASTER_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster Eden -shard Master"
CMD_SLAVE_START = "dontstarve_dedicated_server_nullrenderer.exe -console -cluster Eden -shard Caves"

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return

class Shard:
    def __init__(self, cmd, cwd, name):
        self.cmd = cmd
        self.cwd = cwd
        self.name = name
        self.output_queue = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.input_queue = Queue(maxsize=1024)

    def start(self):
        self.process = Popen(self.cmd, stdout=PIPE, stdin=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
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

BG_ROOT = '#21252B'
FG_ROOT = '#CCCCCC'

BG_TERM = '#383E4A'
FG_TERM = '#409E68'
RELIEF_TERM = tk.GROOVE

class ServerControl:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.configure(bg=BG_ROOT)        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("DST Server Control")
        icon_path = os.path.join("./", "dstctl.ico")
        self.root.iconbitmap(icon_path)

        self.master = Shard(CMD_MASTER_START, CWD, 'MASTER')
        self.slave = Shard(CMD_SLAVE_START, CWD, 'SLAVE')

        self.master.start()
        self.slave.start()

        # Buttons
        button_width = 25
        
        self.btnStartAll = tk.Button(root, command=self.start_all, text="Start", bg=BG_TERM, fg=FG_ROOT, width=button_width)
        self.btnStartAll.grid(row=1,column=1,pady=2)

        self.btnShutdownAll = tk.Button(root, command=self.shutdown_all, text="Shutdown", bg=BG_TERM, fg=FG_ROOT, width=button_width)
        self.btnShutdownAll.grid(row=2,column=1,pady=2)

        self.btnRegenerateWorld = tk.Button(root, command=self.regenerate_world, text="Regenerate World", bg=BG_TERM, fg=FG_ROOT, width=button_width)
        self.btnRegenerateWorld.grid(row=3,column=1)


        self.separator1 = tk.Label(root,text="", height=2, bg=BG_ROOT, width=button_width)
        self.separator1.grid(row=4,column=1)

        self.btnQuit = tk.Button(root, command=self.quit, text="Quit", bg=BG_TERM, fg=FG_ROOT, width=button_width)
        self.btnQuit.grid(row=5,column=1)
        
        # Labels
        self.lblMasterStatus = tk.Label(root, text='MASTER status: ', fg=FG_ROOT, bg=BG_ROOT)
        self.lblMasterStatus.grid(row=1,column=0)

        self.lblSlaveStatus = tk.Label(root, text='SLAVE status: ', fg=FG_ROOT, bg=BG_ROOT)
        self.lblSlaveStatus.grid(row=2,column=0)

        self.lstMaster = tk.Listbox(root,
            font=(None, 8),
            width="60",
            height="25",
            bg=BG_TERM,
            fg=FG_TERM,
            relief=RELIEF_TERM,
            highlightcolor=BG_ROOT,
            highlightthickness=0)
        self.lstMaster.grid(row=0,column=0,ipadx=8, padx=11, ipady=8, pady=11)

        self.lstSlave = tk.Listbox(root,
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
                self.lstMaster.insert(tk.END, [line])
                self.lstMaster.see(tk.END)
            line = self.slave.get_output()
            if line:
                self.lstSlave.insert(tk.END, [line])
                self.lstSlave.see(tk.END)
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


def kill_existing_server_procs():
    process = Popen('taskkill /F /IM "dontstarve_dedicated_server_nullrenderer.exe"', stdout=PIPE)
    stdout = process.communicate()[0]
    if "SUCCESS" in str(stdout):
        return "Existing server processes (dontstarve_dedicated_server_nullrenderer.exe) were found and terminated."
    elif "ERROR" in str(stdout):
        return None
                
kill_existing_server_procs()
root = tk.Tk()
app = ServerControl(root)
root.mainloop()

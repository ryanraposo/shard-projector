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


class DisplayServerControl:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(0,0)
        self.root.configure(bg='#1D2024')        
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self.p_master = start_master()
        self.p_slave = start_slave()

        self.btnReset = Button(root, command=self.reset, text="Reset")
        self.btnReset.grid(row=1,column=1)

        self.btnShutdown = Button(root, command=self.shutdown, text="Shutdown")
        self.btnShutdown.grid(row=2,column=1)

        # master thread & queue
        q_master_output = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.q_master_input = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t_master_reader = Thread(target=self.reader_thread_master, args=[q_master_output])
        t_master_reader.daemon = True
        t_master_reader.start()

        # slave thread & queue
        q_slave_output = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.q_slave_input = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t_slave_reader = Thread(target=self.reader_thread_slave, args=[q_slave_output])
        t_slave_reader.daemon = True
        t_slave_reader.start()

        # gui widgets for output
        self.lstMaster = Listbox(root, font=(None, 8), width="60")
        self.lstMaster.grid(row=0,column=0,ipadx=4, padx=4, ipady=4, pady=4)

        self.lstSlave = Listbox(root, font=(None, 8), width="60")
        self.lstSlave.grid(row=0,column=1,ipadx=4, padx=4, ipady=4, pady=4)
        
        # start update loop
        self.update_master(q_master_output)
        self.update_slave(q_slave_output)

    def shutdown(self):
        print('Shutdown Initiated')
        try:
            self.q_master_input.put("c_shutdown()")
        finally:
            self.q_master_input.put(None)
        try:
            self.q_slave_input.put("c_shutdown()")
        finally:
            self.q_slave_input.put(None)

    def reset(self):
        print('Reset Initiated')
        try:
            self.q_master_input.put("c_reset()")
        finally:
            self.q_master_input.put(None)
        try:
            self.q_slave_input.put("c_reset()")
        finally:
            self.q_slave_input.put(None)
    # Master

    def reader_thread_master(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.p_master.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update_master(self, q):
        """Check if write queue has input, if so write to Master stdin. Then Update GUI with items from the reader queue."""
        # If items in write queue, write to Master stdin
        for line in iter_except(self.q_master_input.get_nowait, Empty): 
            if line:
                with self.p_master.stdin as pipe:
                    pipe.write(line.encode())
        # If items in read queue, update GUI with them
        for line in iter_except(q.get_nowait, Empty): # display all content
            if line is None:
                # self.quit()
                return
            else:
                self.lstMaster.insert(END, [line])
                self.lstMaster.see(END)
                break # display no more than one line per 40 milliseconds
        self.root.after(40, self.update_master, q) # schedule next update

    #Slave
    def reader_thread_slave(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.p_slave.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update_slave(self, q):
        """Check if write queue has input, if so write to Master stdin. Then Update GUI with items from the reader queue."""
        # If items in write queue, write to Slave stdin
        for line in iter_except(self.q_slave_input.get_nowait, Empty): 
            if line:
                with self.p_slave.stdin as pipe:
                    pipe.write(line.encode())
        # If items in read queue, update GUI with them
        for line in iter_except(q.get_nowait, Empty): # display all content
            if line is None:
                # self.quit()
                return
            else:
                self.lstSlave.insert(END, [line])
                self.lstSlave.see(END)
                break # display no more than one line per 40 milliseconds
        self.root.after(40, self.update_slave, q) # schedule next update

    def quit(self):
        # self.close_shards()
        self.p_master.kill()
        self.p_slave.kill()
        # self.p_slave.kill()
        self.root.destroy()





root = Tk()

app = DisplayServerControl(root)


root.mainloop()

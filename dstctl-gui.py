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
    proc = Popen(CMD_MASTER_START, stdout=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
    return proc


def start_slave():
    """Starts the Slave server shard and returns the process"""
    proc = Popen(CMD_SLAVE_START, stdout=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
    return proc


class DisplayServerControl:
    def __init__(self, root):
        self.root = root

        # start dummy subprocess to generate some output
        self.p = start_master()

        # launch thread to read the subprocess output
        #   (put the subprocess output into the queue in a background thread,
        #    get output from the queue in the GUI thread.
        #    Output chain: process.readline -> queue -> label)
        q = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        t = Thread(target=self.reader_thread, args=[q])
        t.daemon = True # close pipe if GUI process exits
        t.start()

        # show subprocess' stdout in GUI
        self.label = Label(root, text="  ", font=(None, 15))
        self.label.pack(ipadx=4, padx=4, ipady=4, pady=4, fill='both')
        self.update(q) # start update loop

    def reader_thread(self, q):
        """Read subprocess output and put it into the queue."""
        try:
            with self.p.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    q.put(line)
        finally:
            q.put(None)

    def update(self, q):
        """Update GUI with items from the queue."""
        for line in iter_except(q.get_nowait, Empty): # display all content
            if line is None:
                self.quit()
                return
            else:
                self.label['text'] = line # update GUI
                break # display no more than one line per 40 milliseconds
        self.root.after(40, self.update, q) # schedule next update

    def quit(self):
        self.p.kill() # exit subprocess if GUI is closed (zombie!)
        self.root.destroy()


root = Tk()
app = DisplayServerControl(root)

root.mainloop()

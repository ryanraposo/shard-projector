import sys

from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from queue import Queue, Empty
from threading import Thread

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

    def _update_output(self, q):
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
        try:
            with self.process.stdin as pipe:
                pipe.write(line.encode())
            print(line + ' recieved by ' + self.name)
        except:
            print(line + ' NOT recieved by ' + self.name)



"""
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
"""
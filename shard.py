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
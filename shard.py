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
    def __init__(self, cmd, cwd):
        self.cmd = cmd
        self.cwd = cwd
        self.output_queue = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.input_queue =  Queue(maxsize=1024)

    def start(self):
        self.process = Popen(self.cmd, stdout=PIPE, stdin=PIPE, shell=True, cwd="c:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin")
        self.thread_reader = Thread(target=self._reader_thread_fn)
        self.thread_reader.daemon = True
        self.thread_reader.start()

    def shutdown(self):
        print('Shutdown Initiated')
        try:
            self.input_queue.put("c_shutdown()")
        finally:
            self.input_queue.put(None)


    def _reader_thread_fn(self):
        """Read process output and put it into the reader queue."""
        try:
            with self.process.stdout as pipe:
                for line in iter(pipe.readline, b''):
                    self.output_queue.put(line)
        finally:
            self.output_queue.put(None)

    def get_output_queue(self):
        return self.output_queue.get_nowait
            
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
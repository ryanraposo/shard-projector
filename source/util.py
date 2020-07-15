from itertools import islice
from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty

def iter_except(function, exception):
    """Iter-like that stops on exception."""
    try:
        while True:
            yield function()
    except exception:
        return


class Job:
    """A system job with threaded output queueing. Has methods for controlling
    and monitoring a supplied subprocess.
    """
    def __init__(self, args):
        self.process = Popen(args, stdout=PIPE, stdin=PIPE, shell=True)
        self.q = Queue(maxsize=1024)
        self.thread_reader = Thread(target=self._update_output, args=[self.q])
        self.thread_reader.daemon = True
        self.thread_reader.start()

    def _update_output(self, q):
        """Primary threaded method. Places lines from the process' stdout into a queue."""
        if self.process:
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b""):
                        q.put(line)
            finally:
                q.put(None)

    def get_output(self):
        """Returns lines from the Job's stdout. Use on a scheduled interval to handle output
        without disrupting Tkinter's execution loop."""
        for line in iter_except(self.q.get_nowait, Empty):
            if line is None:
                return None
            else:
                return line
    
    def write_input(self, line):
        """Writes a line to the stdin of the Job's associated process."""
        if self.process:
            with self.process.stdin as pipe:
                pipe.write(line.encode())
            
    def terminate(self):
        """Kills the Job's process and ceases all threaded activity."""
        self.process.kill()
        self.thread_reader = None


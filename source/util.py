import os
import shutil
import requests
from itertools import islice
from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty
import zipfile
from enum import Enum

from constants import DIR_EXT, DIR_TEMP


def iter_except(function, exception):
    """Iter-like that stops on exception."""
    try:
        while True:
            yield function()
    except exception:
        return

class STATE(Enum):
    USERDEFINED=1
    ADDIN=2

class SteamCMD:
    """Represents SteamCMD as an application utility.
    
    Methods allow installing SteamCMD as an add-in. If add-in is installed,
    the object's methods will use it. Otherwise, it will attempt to use an
    installation defined in parent application configs.
    """
    def __init__(self, parent, logging=False):
        self.parent = parent
        self.logging = logging

    @property
    def state(self):
        if self.path:
            if 'shard_projector' in self.path:
                self.state = STATE.ADDIN
            else:
                self.state = STATE.USERDEFINED

    @property
    def path(self):
        addin_path = os.path.join(DIR_EXT, "steamcmd")
        userdefined_path = self.parent.config.get("ENVIRONMENT", "steamcmd")
        if os.path.exists(userdefined_path):
            return userdefined_path
        elif os.path.exists(addin_path):
            return addin_path

    def _log(self, message):
        """Debug prints SteamCMD log message if logging is enabled.
        """
        print(">>> STEAMCMD: " + str(message))

    def _download(self):
        """Downloads the latest SteamCMD installer zip to the 'temp' directory.
        """
        z_url = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip"
        response = requests.get(z_url)
        z_path = os.path.join(DIR_TEMP, os.path.basename(z_url))
        z_file_io = open(z_path, "wb")
        z_file_io.write(response.content)
        z_file_io.close()
        self._log("download finished.")

    def _unpack(self):
        """Unzips the SteamCMD zip to the 'ext' directory from 'temp' then
         deletes the archive. 
        """
        self._log("unzipping installer...")
        z_path = os.path.join(DIR_TEMP, "steamcmd.zip")
        z_file = zipfile.ZipFile(z_path)
        z_file.extractall(os.path.join(DIR_EXT, "steamcmd"))
        z_file.close()
        os.remove(z_path)
        self._log("unzip finished.")

    def install(self):
        """Installs SteamCMD into the 'ext' directory, overwriting any existing
        installation. 
        """
        dest = os.path.join(DIR_EXT, "steamcmd")

        if os.path.exists(dest):
            self._log("removing existing installation...")
            shutil.rmtree(dest, True)
            self._log("removal finished.")

        self._download()
        self._unpack()

        self._log("installing...")
        return Popen(
            args=os.path.join(dest, "steamcmd.exe"), universal_newlines=True
        )

    def gameserver_install(self, appid):
        """Installs/updates a gameserver using the supplied appid.
        """
        cmd = os.path.join(
            self.path,
            f"steamcmd.exe +login anonymous +app_update {appid} validate +quit",
        )
        return Job(cmd)

    def get_gameserver(self, appid):
        """Gets a gameserver path if an installation is found. Returns None if
        not.
        """
        pass

class Job:
    """A system job with threaded output queueing. Has methods for controlling
    and monitoring a supplied subprocess.
    """

    def __init__(self, cmd):
        self.process = Popen(
            args=cmd,
            stdout=PIPE, stdin=PIPE,
            shell=True,
        )
        self.q = Queue(maxsize=1024)
        self.thread_reader = Thread(
            target=self._update_output,
            args=[self.q],
            daemon=True
        )
        self.thread_reader.start()

    def _update_output(self, q):
        """Primary threaded method. Places lines from the process' stdout into\
        a queue. If process has ended, triggers Thread cleanup by returning."""
        if self.is_running():
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b""):
                        q.put(line)
            finally:
                q.put(None)
        else:
            return

    def get_output(self):
        """Returns lines from the Job's stdout. Use on a scheduled interval to handle output
        without blocking Tkinter's execution loop."""
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
        """Kills the Job's process and ceases threaded activity."""
        if self.is_running():
            self.process.kill()
            self.thread_reader = None
 
    def is_running(self):
        exit_code = self.process.poll()
        if exit_code != None:
            return False
        return True
"""
Desktop application for running & managing Don't Starve Together Dedicated Servers on local machines running Windows
"""
import sys, os, json, shutil, configparser

from itertools import islice
from subprocess import Popen, PIPE
from textwrap import dedent
from threading import Thread
from queue import Queue, Empty

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk

import widgets

TEMP_CONST_STEAMCMD_DST_BIN_PATH = "C:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin"
TEMP_CONST_NULLRENDERER_PATH = "C:/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe"

def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


def kill_existing_server_procs():
    """Executes a Windows native 'taskkill' command targeting any dedicated server nullrenderer
    instances. Returns a string containing the commands encoded stdout."""

    process = Popen(
        'taskkill /F /IM "dontstarve_dedicated_server_nullrenderer.exe"', stdout=PIPE
    )
    stdout = process.communicate()[0]
    return str(stdout)


class Configuration:
    """A reader/writer for a specific configuration file. Accepts a file path (*.ini) that does not need to be accesible at instantiation.
    Throws an exception if read/write methods call fail."""

    class AccessError(Exception):
        pass

    def __init__(self, ini_file_path):
        self.path = ini_file_path
        self.config = configparser.ConfigParser()

    def _read(self):
        paths_succesfully_read = self.config.read(self.path)
        return self.path in paths_succesfully_read

    def as_dict(self):
        """Returns configuration as a dictionary of sections as keys with option:option_value as values. """
        self._read()
        the_dict = {}
        for section in self.config.sections():
            the_dict[section] = {}
            for key, val in self.config.items(section):
                the_dict[section][key] = val
        return the_dict

    def get(self, section, option):
        self._read()
        return self.config.get(section, option)

    def get_sections(self):
        self._read()
        return self.config.sections()

    def set_value(self, section, option, value):
        self.config.set(section,option,value)
        

class Shard:
    """Represents a server shard instance, has has methods and properties related to its folder on disk, 
    configuration (server.ini), and the translated subprocess to be threaded when controlling a parent server cluster.

    Attributes:
        path (str): An absolute-path to the shard's directory

        configuration (obj): A read/writeable interface with a server.ini file
        
        cluster_name (str): The name of the shards parent server-cluster
        
        command (str): The command executed when starting the coressponding subprocess
        
        process (subprocess): The subprocess associated with the shard
        
        thread_reader (Thread): The thread started to house the subprocess and run it successfully in parallel with the GUI loop.
        
        queue_input (Queue): A queue used for writing to the shard's process stdin, processed at constant intervals
        
        queue_output (Queue): A queue used for reading the shard's process stdout, written to at constant intervals
    """

    def __init__(self, path, cluster_name):
        self.path = os.path.realpath(path)
        self.configuration = Configuration(os.path.join(self.path, "server.ini"))
        self.cluster_name = cluster_name
        self.name = os.path.basename(path)
        self.command = self._get_command()
        self.output_queue = Queue(
            maxsize=1024
        )  # limit output buffering (may stall subprocess)
        self.input_queue = Queue(
            maxsize=1024
            )
    
    def __repr__(self):
        return self.name
    
    def start(self):
        cwd = os.path.realpath(
            TEMP_CONST_STEAMCMD_DST_BIN_PATH
        )
        self.process = Popen(self.command,
            cwd=cwd,
            stdout=PIPE,
            stdin=PIPE,
            shell=True
        )
        self.q = Queue(maxsize=1024)
        self.thread_reader = Thread(target=self._update_output, args=[self.q])
        self.thread_reader.daemon = True
        self.thread_reader.start()
                
    def _get_command(self):
        command = [
            TEMP_CONST_NULLRENDERER_PATH,
            "-console_enabled",
            "-cluster",
            self.cluster_name,
            "-shard",
            self.name,
        ]        
        return command

    def _update_output(self, q):
        """Adds stdout of associated process to shard's output queue."""
        if self.is_started():
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b""):
                        q.put(line)
            finally:
                q.put(None)

    def get_output(self):  # Schedule me
        """Returns output queue of the shard."""
        if self.is_started():
            for line in iter_except(self.q.get_nowait, Empty):  # display all
                if line is None:
                    return None
                else:
                    return line

    def write_input(self, line):
        """Writes the input queue of the shard to the stdin of its associated process."""
        if self.is_started():
            try:
                with self.process.stdin as pipe:
                    pipe.write(line.encode())
                print(line + " recieved by " + self.name)
            except:
                print(line + " NOT recieved by " + self.name)

    def status(self):
        """Returns 'UP' if associated process is found, and 'DOWN' if not."""
        if self.is_started():
            poll = self.process.poll()
            if poll == None:
                return "UP"
            else:
                return "DOWN"

    def is_started(self):
        return hasattr(self, "process")

    def get_pid(self):
        if self.is_started():
            try:
                return self.process.pid
            except:
                print('Could not retrieve pid for shard ' + self.name)
        else:
            print('Shard ' + self.name + ' is not started. A pid could not be retrieved.')

    def kill(self):
        try:
            pid = self.get_pid()
            self.process.kill()
        except:
            print('Could not kill process associated with shard: ' + self.name + '. (pid: ' + str(pid) + ")")
        else:
            print('Successfully killed process associated with shard: ' + self.name + '. (pid: ' + str(pid) + ")")

    def get_config_value(self, section, option):
        return self.configuration.get(section, option)


class DedicatedServer:
    """Represents a server cluster instance. Has methods and properties related to its folder on disk,
    its configuration (cluster.ini), and is parent to one or multiple Shards. Is the high-level container
    object controlled by the ServerControl class."""

    class NonexistentDirectory(Exception):
        pass

    class InvalidServerDirectory(Exception):
        pass

    def __init__(self, path, server_control_window):
        self.server_control_window = server_control_window
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)
        self.config = Configuration(os.path.join(self.path, "cluster.ini"))

        self._get_shards()

    def _get_shards(self):
        self.shards = []
        detected_shard_directories = self._detect_shard_directories()
        user_confirmed_shard_directories = widgets.DialogConfirmShardDirectories(
            parent=self.server_control_window,
            detected_shard_directories=detected_shard_directories,
        ).show()
        for each in user_confirmed_shard_directories:
            shard = Shard(each, self.name)
            self.shards.append(shard)

    def _detect_shard_directories(self):
        shard_directories = []
        for directory in os.listdir((self.path)):
            path = os.path.join(self.path, directory)
            if os.path.isdir(path):
                if "server.ini" in os.listdir(path):
                    shard_directories.append(path)
        return shard_directories

    def set_shard_directories(self, directories):
        self.shard_directories = directories

    def is_valid_server_config(self, directory_path):
        # Check for real path, server.ini, clustertoken.txt, at least one folder containing cluster.ini
        root_file_reqs = ["cluster.ini", "cluster_token.txt"]
        if os.path.isdir(os.path.abspath(directory_path)):  # Check 1: Real path
            directory_root_contents = os.listdir(directory_path)
            if all(
                item in directory_root_contents for item in root_file_reqs
            ):  # Check 2: contains server.ini and clustertoken.txt
                for member in directory_root_contents:
                    full_member_path = os.path.join(directory_path, member)
                    if os.path.isdir(
                        full_member_path
                    ):  # Check 3: contains at least one subdirectory containing cluster.ini
                        if "server.ini" in os.listdir(full_member_path):
                            return True
        return False
    # def add_shard(self, path):


class ServerControl:
    """Main window of the application. Displays output from shards and is host to various server controls."""

    def __init__(self, root, server=None):
        self.root = root
        self.initialize_ui()
        self.server = server

        self.update_ui()

    def initialize_ui(self):
        """Setup widgets and styling of main window."""

        self.root.geometry("960x720")
        self.root.resizable(0, 0)
        self.root.protocol("WM_DELETE_WINDOW", self.quit)
        self.root.title("DST Server Control")
        icon_path = os.path.join("./img/dstctl.ico")
        self.root.iconbitmap(icon_path)
        self.root.configure(bg="#424242")

        # Style
        style = ttk.Style()
        text_font = ("TkDefaultFont", "14")
        console_font = ("TkDefaultFont", "8")
        style.configure("console.Treeview", highlightthickness=0, bd=0, font=console_font)
        # Style: Combobox
        self.root.option_add("*TButton*Label.font", text_font)
        self.root.option_add("*TCombobox*Listbox.background", "#424242")
        self.root.option_add("*TCombobox*Listbox.selectBackground", "#525252")
        # Top Bar
        self.frmTopBar = ttk.Frame(root, height=20, width=761)
        self.frmTopBar.place(x=20, y=10)
        # Server
        self.entServer = ttk.Entry(self.frmTopBar, width=50)
        self.entServer.grid(row=0, column=0)

        self.btnSelectServer = ttk.Button(
            master=self.frmTopBar, command=self.select_server, text="Browse"
        )
        self.btnSelectServer.grid(row=0, column=1)

        self.btnConfigureServer = ttk.Button(
            master=self.frmTopBar, command=self.configure_server, text="Configure"
        )
        self.btnConfigureServer.grid(row=0, column=2)

        # Console Views
        self.console_view_master = widgets.WidgetConsoleView(self.root, width=450, height_in_rows=21)
        self.console_view_master.place(
            x=20,
            y=50
        )

        self.console_view_slave = widgets.WidgetConsoleView(self.root, width=450, height_in_rows=21)
        self.console_view_slave.place(
            x=490,
            y=50
        )

        # Status Labels
        self.lblMasterStatus = ttk.Label(root, text="STATUS: ")
        self.lblMasterStatus.update()
        self.lblMasterStatus.place(x=20, y=(self.console_view_master.winfo_y() + self.console_view_master.height_in_pixels))

        self.lblSlaveStatus = ttk.Label(root, text="STATUS: ")
        self.lblSlaveStatus.update()
        self.lblSlaveStatus.place(x=490, y=(self.console_view_master.winfo_y() + self.console_view_master.height_in_pixels))

        # Command Buttons
        self.frame_commands = ttk.Frame(root)
        self.frame_commands.place(x=560, y=540, height=150, width=300)
        style.configure("TFrame", background="#424242")

        self.btnStartAll = ttk.Button(
            self.frame_commands, command=self.start_shards, text="Start"
        )
        self.btnStartAll.grid(row=0, column=0)

        self.btnShutdownAll = ttk.Button(
            self.frame_commands, command=self.shutdown_all, text="Shutdown"
        )
        self.btnShutdownAll.grid(row=1, column=0)

        self.btnCustomCommand = ttk.Button(
            self.frame_commands, command=self.custom_command, text="Custom..."
        )
        self.btnCustomCommand.grid(row=0, column=3)

        self.btnRegenerateWorld = ttk.Button(
            self.frame_commands, command=self.regenerate_world, text="Regenerate"
        )
        self.btnRegenerateWorld.grid(row=0, column=1)

        self.btnReset = ttk.Button(self.frame_commands, command=self.reset, text="Reset")
        self.btnReset.grid(row=1, column=1)

        self.btnSave = ttk.Button(self.frame_commands, command=self.save, text="Save")
        self.btnSave.grid(row=0, column=2)

        self.btnUpdate = ttk.Button(
            self.frame_commands,
            command=self.update_steamcmd_dedicated_server,
            text="Update",
        )
        self.btnUpdate.grid(row=1, column=2)

        self.sepFrame = ttk.Frame(self.frame_commands, height=20, width=0)
        self.sepFrame.grid(row=3, column=2)

        # self.cvsCommands.grid_rowconfigure(3, weight=1)

        self.btnQuit = ttk.Button(self.frame_commands, command=self.quit, text="Quit")
        self.btnQuit.grid(row=4, column=2)

    def update_ui(self):
        """Updates GUI, including widgets displaying info from/about the selected server's shards."""
        try:
            if self.server is not None:
                # Update Master status label & console output listbox
                if self.master.is_started():
                    self.lblMasterStatus.configure(text="Status: " + self.master.status())
                line = self.master.get_output()
                if line:
                    self.console_view_master.write_line(line)
                # Update Slave status label & console output listbox (if slave server exists)
                if hasattr(self, "slave") and self.slave.is_started():
                    self.lblSlaveStatus.configure(text="Status: " + self.slave.status())
                    line = self.slave.get_output()
                    if line:
                        self.console_view_slave.write_line(line)
        finally:
            self.root.after(40, self.update_ui)

    def start_shards(self):
        if self._server_selected():
            try:
                for shard in self.server.shards:
                    shard.start()
            except:
                print('Start error')

    def shutdown_all(self):
        self.send_command("c_shutdown()")
        self.root.after(5000, self.kill_all_shards)

    def regenerate_world(self):
        self.send_command("c_regenerateworld()")

    def reset(self):
        self.send_command("c_reset()")

    def save(self):
        self.send_command("c_save()")

    def custom_command(self): 
        dialog = widgets.DialogCustomCommand(parent=self.root, callback_fn=self.send_command)
        dialog.show()

    def send_command(self, command):
        if self._server_selected():
            try:
                for shard in self.server.shards:
                    shard.write_input(command)
                print(command + ' delivered')
            except:
                print(command + ' not delivered')

    def update_steamcmd_dedicated_server(self):
        self.shutdown_all()
        os.system(os.path.realpath("./scripts/updatesteamcmd.bat"))

    def configure_server(self):
        widgets.DialogConfigureServer(self.root, self.server)

    def select_server(self):
        # Prompt user for directory...
        selection = filedialog.askdirectory(
            initialdir=os.path.realpath("%CURRENTUSER%"),
            title="Select a server directory...",
        )
        try: # use selection
            self.server = DedicatedServer(selection, self.root)
            self.entServer.delete(0, tk.END)
            self.entServer.insert(0, self.server.path)
        except: # show warning that directory is unsuitable
            messagebox.showwarning(
                title="DST Server Control",
                message=selection + " does not appear to be a valid dedicated server directory.",
            )
        else: # shorthand master shard with self.master, slave shard with self.slave, update respective console window headings
            for shard in self.server.shards:
                if shard.get_config_value("SHARD", 'is_master') == 'true':
                    self.master = shard
                    self.console_view_master.set_heading(shard.name)
                else:
                    self.slave = shard
                    self.console_view_slave.set_heading(shard.name)

    def kill_all_shards(self):
        if self._has_master():
            self.master.kill()
        if self._has_slave():
            self.slave.kill()

    def _server_selected(self):
        return self.server is not None

    def _has_master(self) -> bool:
        return hasattr(self, 'master')

    def _has_slave(self) -> bool:
        return hasattr(self, 'slave')
        
    def quit(self):
        self.shutdown_all()
        self.root.after
        self.root.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = ServerControl(root)
    root.mainloop()
    


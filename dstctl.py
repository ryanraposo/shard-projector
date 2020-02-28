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


class ConfigurationIO:
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
        """Gets value text as it appears in the configuration file. ex 'true' will return string 'true'."""
        self._read()
        return self.config.get(section, option)

    def get_typed(self, section, option):
        """Gets value from configuration file as expected type. ex 'true' will return boolean True, '2' will return int 2."""
        self._read()
        value = self.config.get(section, option)
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        if value.isnumeric():
            return int(value)

    def _get_sections(self):
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
        self.configuration = ConfigurationIO(os.path.join(self.path, "server.ini"))
        self.is_master = self.configuration.get_typed('SHARD', 'is_master')
        self.cluster_name = cluster_name
        self.name = os.path.basename(path)
        self.process = None
        self.command = self._get_command()
        self.output_queue = Queue(
            maxsize=1024
        )  # limit output buffering (may stall subprocess)
        self.input_queue = Queue(
            maxsize=1024
            )
    
    def __repr__(self):
        if self.is_master:
            return 'master'
        return 'slave'
    
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
        if self.is_running:
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b""):
                        q.put(line)
            finally:
                q.put(None)

    def get_output(self):  # Schedule me
        """Returns output queue of the shard."""
        if self.is_running:
            for line in iter_except(self.q.get_nowait, Empty):  # display all
                if line is None:
                    return None
                else:
                    return line
        else:
            return None

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
           
    def write_input(self, line):
        """Writes the input queue of the shard to the stdin of its associated process."""
        if self.is_running:
            try:
                with self.process.stdin as pipe:
                    pipe.write(line.encode())
                print(line + " recieved by " + self.name)
            except:
                print(line + " NOT recieved by " + self.name)

    def get_process_id(self):
        return self.process.pid

    def kill_process(self):
        if self.is_running:
            self.process.kill()
    @property
    def is_running(self):
        if self.process != None:
            poll = self.process.poll()
            if poll == None:
                return True
            else:
                return False


class DedicatedServer:
    """Represents a server cluster configuration and fileset. Has methods and properties related to its folder on disk,
    its configuration (cluster.ini), and is parent to one or multiple Shards. Is the high-level container
    object loaded by the ServerControl class."""

    class NonexistentDirectory(Exception):
        pass

    class InvalidServerDirectory(Exception):
        pass

    def __init__(self, path, server_control_window):
        self.server_control_window = server_control_window
        self.path = os.path.abspath(path)
        self.name = os.path.basename(self.path)
        self.config = ConfigurationIO(os.path.join(self.path, "cluster.ini"))
        self.shards = self._get_shards()

    def _get_shards(self):
        shards = []
        detected_shard_directories = self._detect_shard_directories()
        user_confirmed_shard_directories = widgets.DialogConfirmShardDirectories(
            parent=self.server_control_window,
            detected_shard_directories=detected_shard_directories,
        ).show()
        for each in user_confirmed_shard_directories:
            shard = Shard(each, self.name)
            shards.append(shard)
        return shards

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
    @property
    def master(self):
        for shard in self.shards:
            if shard.is_master:
                return shard
    @property
    def slave(self):
        for shard in self.shards:
            if not shard.is_master:
                return shard
    @property
    def processes(self):
        processes = []
        for shard in self.shards:
            if shard.is_running:
                processes.append(shard.process)
        return processes

    def start(self):
        for shard in self.shards:
            if not shard.is_running:
                shard.start()
        
    def run_command(self, command):
        for shard in self.shards:
            shard.write_input(command)

    def kill(self):
        for shard in self.shards:
            if shard.is_running:
                shard.kill_process()


class ServerControl:
    """Main application. Includes the window and its components. Displays output from shards and is host to various server controls. Parent to a DedicatedServer object."""

    def __init__(self, root):
        self.window = root
        self.initialize_ui()
        self.active_server = None

        if self.active_server:
            print('')

        self.update_ui()

    def initialize_ui(self):
        """Setup widgets and styling of main window."""

        # Window
        self.window.geometry("960x650")
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.title("DST Server Control")
        icon_path = os.path.join("./img/dstctl.ico")
        self.window.iconbitmap(icon_path)
        self.window.configure(bg="#424242")

        # Styling
        text_font = ("TkDefaultFont", "14")
        self.window.option_add("*TButton*Label.font", text_font)
        self.window.option_add("*TCombobox*Listbox.background", "#424242")
        self.window.option_add("*TCombobox*Listbox.selectBackground", "#525252")       

        # Top Bar
        self.frmTopBar = ttk.Frame(root, height=20, width=761)
        self.frmTopBar.place(x=20, y=25)

        self.entServer = ttk.Entry(self.frmTopBar, width=50)
        self.entServer.grid(row=0, column=0)
        
        self.btnSelectServer = ttk.Button(master=self.frmTopBar, command=self.on_browse, text="Browse")
        self.btnSelectServer.grid(row=0, column=1)
        
        self.btnConfigureServer = ttk.Button(master=self.frmTopBar, command=self.on_configure, text="Configure")
        self.btnConfigureServer.grid(row=0, column=2)

        # Power Button
        self.btn_power = widgets.WidgetPowerButton(root, command=self.on_power)
        self.btn_power.place(x=840,y=8)

        # Console Views
        self.console_view_master = widgets.WidgetConsoleView(self.window, width=450, height_in_rows=21)
        self.console_view_master.place(x=20,y=75)

        self.console_view_slave = widgets.WidgetConsoleView(self.window, width=450, height_in_rows=21)
        self.console_view_slave.place(x=490,y=75)

        # Quick Commands
        self.command_panel = widgets.WidgetCommandPanel(
            parent=self.window,
            buttons=[
                ("Regenerate", self.on_regenerate),
                ("Reset", self.on_reset),
                ("Save", self.on_save),
                ("Update", self.on_update),
                ("Custom...", self.on_custom),
                ("Quit", self.quit)
            ],
            max_columns=4,
            panel_text="Commands"        
        )
        self.command_panel.place(x=550,y=520)
        
        # Info Panel (Server)
        self.info_panel_server = widgets.WidgetInfoPanel(
            parent=self.window,
            info_items=[
                ("Server:", self.get_server_info, ['NETWORK', 'cluster_name']),
                ("Description:", self.get_server_info, ['NETWORK', 'cluster_description']),
                ("PVP Enabled:", self.get_server_info, ['GAMEPLAY', 'pvp']),
                ("Gamemode:", self.get_server_info, ['GAMEPLAY', 'game_mode'])
            ],
            header='Server Info'
        )
        self.info_panel_server.place(x=50,y=550,width=300)

    def update_ui(self):
        """Retrieves info from the active server and its shards for display in the UI.
        Includes: Shard (nullrenderer) output into ConsoleViews.
        Self-reschedules for 40ms effective intervals """
        try:
            if self.active_server: # Update ConsoleViews & button states    
                self.btn_power.set_state('normal')
                self.update_console_view(self.console_view_master, self.active_server.master)
                self.update_console_view(self.console_view_slave, self.active_server.slave)
            else:
                self.btn_power.set_state('disabled')
        finally:
            self.window.after(40, self.update_ui)

    def update_console_view(self, view, shard):
        if self.active_server:
            for shard in self.active_server.shards:
                if shard.is_running:
                    view.set_status("Runnning (pid: " + str(shard.get_process_id()))
                    line = shard.get_output()
                    if line:
                        view.write_line(line)
                else:
                    view.set_status(" -")

    def on_power(self):
        if self.active_server:
            if len(self.active_server.processes) > 0:
                self.active_server.run_command('c_shutdown()')
                self.window.after(1000)
                self.active_server.kill()
            else:
                self.active_server.start()

    def on_regenerate(self):
        self._send_command("c_regenerateworld()")

    def on_reset(self):
        self._send_command("c_reset()")

    def on_save(self):
        self._send_command("c_save()")

    def on_custom(self): 
        custom_command = widgets.DialogCustomCommand(parent=self.window).show()
        self._send_command(custom_command)

    def on_update(self):
        if self.active_server:
            self.active_server.kill_processes
        self.window.after(5000)
        os.system(os.path.realpath("./scripts/updatesteamcmd.bat"))

    def on_configure(self):
        widgets.DialogConfigureServer(self.window, self.active_server)

    def on_browse(self):
        # Prompt user for directory...
        selection = filedialog.askdirectory(
            initialdir=os.path.realpath("%CURRENTUSER%"),
            title="Select a server directory...",
        )
        if len(selection) > 0:
            try: # Try to create a DedicatedServer instance with user selected path
                server = DedicatedServer(selection, self.window)
            except: # If unable, show warning that directory is unsuitable
                messagebox.showwarning(
                    title="DST Server Control",
                    message="Failed to set active server from selection.",
                )
            else: # If successful, unload any current server and set new 
                self.unload_server()
                self.set_active_server(server)

    def unload_server(self):
        if self.active_server != None:
            # Shutdown server
            self.active_server.run_command('c_shutdown()')
            # Wait 2 seconds
            self.window.after(2000)
            # Kill procs
            self.active_server.kill()
            # Clear console views
            self.console_view_master.clear()
            self.console_view_slave.clear()

    def set_active_server(self, server): 
        """Updates active_server attribute from server and updates various UI elements accordingly."""
        self.active_server = server
        self.entServer.delete(0, tk.END)
        self.entServer.insert(0, self.active_server.path)
        self.info_panel_server.update_values()
        # self.info_panel_server.configure(info_items=[
        #     ("Server:", self.active_server.config.get('NETWORK', 'cluster_name')),
        #     ("Description:", self.active_server.config.get('NETWORK', 'cluster_description')),
        #     ("Gamemode:", self.active_server.config.get('GAMEPLAY', 'game_mode')),
        #     ("Players:", self.active_server.config.get('GAMEPLAY', 'max_players'))
        # ])
        return server
        
    def _send_command(self, command):
        if hasattr(self, 'active_server'):
            self.active_server.run_command(command)

    def get_server_info(self, section, option):
        if hasattr(self, 'active_server'):
            return self.active_server.config.get(section, option)

    def quit(self):
        self.unload_server()
        self.window.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = ServerControl(root)
    root.mainloop()
    


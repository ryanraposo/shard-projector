"""
Desktop application for running & managing Don't Starve Together Dedicated Servers
"""
import sys, os, pathlib
from os.path import join

from itertools import islice
from subprocess import Popen, PIPE
from threading import Thread
from queue import Queue, Empty

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from ttkthemes import ThemedTk

from constants import ADDINS
from configuration import Ini, ResourceManager

import view
import widgets
from util import iter_except
    

class Shard:
    """Represents a server shard instance, has has methods and properties related to its folder on disk, 
    configuration (server.ini), and the translated subprocess to be threaded when controlling a parent server cluster.

    Attributes:
        path (str): An absolute-path to the shard's directory.

        config (Ini): A read/writeable interface to shard configuration (server.ini) file.
        
        cluster_name (str): The name of the shards parent server-cluster.
        
        command (str): The command executed when starting the coressponding subprocess.
        
        process (subprocess): The subprocess associated with the shard.
        
        thread_reader (Thread): The thread started to read stdout from the subprocess into a queue in parallel with the GUI loop. 
        
        queue_input (Queue): A queue used for writing to the shard's process stdin, processed at constant intervals.
        
        queue_output (Queue): A queue used for reading the shard's process stdout, written to at constant intervals.
    """

    def __init__(self, path, cluster_name):
        self.path = os.path.realpath(path)
        self.config = Ini(join(self.path, "server.ini"), './ini/shard_defaults.ini')
        self.is_master = self.config.get_typed("SHARD", "is_master")
        self.cluster_name = cluster_name
        self.name = os.path.basename(path)
        self.process = None
        self.output_queue = Queue(maxsize=1024)  # limit output buffering (may stall subprocess)
        self.input_queue = Queue(maxsize=1024)

    def __repr__(self):
        if self.is_master:
            return "master"
        return "slave"

    def _get_command_args(self, nullrenderer):
        command = [
            str(nullrenderer),
            "-console_enabled",
            "-cluster",
            self.cluster_name,
            "-shard",
            self.name,
        ]
        return command

    def _update_output(self, q):
        """Adds stdout of associated process to shard's output queue."""
        if self.process:
            try:
                with self.process.stdout as pipe:
                    for line in iter(pipe.readline, b""):
                        q.put(line)
            finally:
                q.put(None)

    def get_output(self):
        """Returns output queue of the shard."""
        for line in iter_except(self.q.get_nowait, Empty):
            if line is None:
                return None
            else:
                return line

    def start(self, nullrenderer):
        cwd = pathlib.Path(nullrenderer).parent
        command_args = self._get_command_args(nullrenderer)

        self.process = Popen(command_args, cwd=cwd, stdout=PIPE, stdin=PIPE, shell=True)
        self.q = Queue(maxsize=1024)
        self.thread_reader = Thread(target=self._update_output, args=[self.q])
        self.thread_reader.daemon = True
        self.thread_reader.start()

    def write_input(self, line):
        """Writes the input queue of the shard to the stdin of its associated process."""
        if self.process:
            try:
                with self.process.stdin as pipe:
                    pipe.write(line.encode())
                print(line + " recieved by " + self.name)
            except:
                print(line + " NOT recieved by " + self.name)

    def get_process_id(self):
        return self.process.pid

    def kill_process(self):
        if self.process:
            self.process.kill()
            self.process = None

    def poll(self): #TODO: test polling methods 
        """Checks for a process id associated with attr process, if none, sets process to None."""
        if self.process:
            exit_code = self.process.poll()
            if exit_code != None:
                self.process = None


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
        self.path = os.path.normpath(path)
        self.name = os.path.basename(self.path)
        self.config = Ini(join(self.path, "cluster.ini"), './ini/cluster_defaults.ini')

        self.shards = []
        self._show_confirm_shard_directories_dialog()

    def _detect_shard_directories(self):
        shard_directories = []
        for directory in os.listdir((self.path)):
            path = join(self.path, directory)
            if os.path.isdir(path):
                if "server.ini" in os.listdir(path):
                    shard_directories.append(path)
        return shard_directories

    def _show_confirm_shard_directories_dialog(self):
        detected_shard_directories = self._detect_shard_directories()
        view.DialogConfirmShardDirectories(
            parent=self.server_control_window,
            detected_shard_directories=detected_shard_directories,
            fn_callback=self.on_confirmed_shard_directories
        )

    def on_confirmed_shard_directories(self, directories):
        for each in directories:
            shard = Shard(each, self.name)
            self.shards.append(shard)

    def is_valid_server_config(self, directory_path):
        # Check for real path, server.ini, clustertoken.txt, at least one folder containing cluster.ini
        root_file_reqs = ["cluster.ini", "cluster_token.txt"]
        if os.path.isdir(os.path.abspath(directory_path)):  # Check 1: Real path
            directory_root_contents = os.listdir(directory_path)
            if all(
                item in directory_root_contents for item in root_file_reqs
            ):  # Check 2: contains server.ini and clustertoken.txt
                for member in directory_root_contents:
                    full_member_path = join(directory_path, member)
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
        return None
    @property
    def slave(self):
        for shard in self.shards:
            if not shard.is_master:
                return shard
        return None
    @property
    def processes(self):
        processes = []
        for shard in self.shards:
            if shard.process:
                processes.append(shard.process)
        return processes

    def start(self, nullrenderer):
        for shard in self.shards:
            if not shard.process:
                shard.start(nullrenderer)

    def run_command(self, command):
        for shard in self.shards:
            shard.write_input(command)

    def poll(self):
        for shard in self.shards:
            shard.poll()

    def kill(self):
        for shard in self.shards:
            if shard.process:
                shard.kill_process()


class ServerControl:
    """Main application. Includes the window and its components. 
    
    Displays output from shards and is host to various server controls. Parent to a DedicatedServer object.
    """
    def __init__(self, root):
        self.window = root
        self.initialize_ui()

        self.active_server=None
        script_path = os.path.dirname(os.path.realpath(__file__))
        config_path = join(script_path, 'ini/settings.ini')
        config_defaults_path = join(script_path, 'ini/settings_defaults.ini')
        self.config = Ini(config_path, config_defaults_path)

        self.update()

    def initialize_ui(self):
        """Setup widgets and styling of main window.
        """
     # Window
        self.window.geometry("960x650")
        self.window.resizable(0, 0)
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.title("Shard Projector")
        icon_path = join("./img/icon.ico")
        self.window.iconbitmap(icon_path)
     # Styling
        self.window.option_add("*TCombobox*Listbox.background", "#424242")
        self.window.option_add("*TCombobox*Listbox.selectBackground", "#525252")
        self.window.option_add("*Menu.background", "#424242")
     # Main Frame
        self.frame_main = ttk.Frame(self.window, width=960, height=650)
     # Top Bar
        self.frame_main = ttk.Frame(self.frame_main)
        self.frame_main.place(x=36, y=0)
        self.widget_directory_select = widgets.DirectorySelectEntry(
            master=self.frame_main,
            on_select=self.on_browse)
        self.widget_directory_select.grid(row=0, column=0)
     # Action Bar
        self.action_bar = ttk.Frame(self.frame_main)
        self.action_bar.columnconfigure(0, minsize=30)
        self.action_bar.columnconfigure(1, minsize=30)
        self.action_bar.rowconfigure(0, minsize=10)
        self.action_settings = ttk.Button(self.action_bar, text="Settings", command=self.on_settings)
        self.action_settings.grid(row=0, column=0, sticky="ns")
        self.action_tasks = ttk.Menubutton(self.action_bar, text="Tasks")
        self.action_tasks.menu = tk.Menu(self.action_tasks,
            tearoff = 0,
            background="#424242",
            foreground="white")
        self.action_tasks["menu"] = self.action_tasks.menu
        self.action_tasks.grid(row=0, column=1, sticky="ns")
        self.action_bar.place(x=620, y=0)
     # Power Button
        self.btn_power = widgets.PowerButton(root, command=self.on_power)
        self.btn_power.set_fx(False)
        self.btn_power.place(x=868, y=12)
     # Info Bar
        self.info_bar = view.InfoBar(master=self.frame_main, command_configure=self.on_configure)
        self.info_bar.place(x=0, y=85, width=960)
     # Console Views
        s = ttk.Style()
        s.configure("console.TFrame", background="#3A3A3A")
        self.console_view_frame = ttk.Frame(self.frame_main, style="console.TFrame")
        cv_width = 470
        cv_height_in_rows = 20
        self.console_view_master = widgets.ConsoleView(self.console_view_frame, width=cv_width, height_in_rows=cv_height_in_rows)
        self.console_view_master.pack(side=tk.LEFT)
        self.console_view_slave = widgets.ConsoleView(self.console_view_frame, width=cv_width, height_in_rows=cv_height_in_rows)
        self.console_view_slave.pack(side=tk.RIGHT)
        self.console_view_frame.place(x=3, y=123, width=954)
     # (Disabled) Toggle Listen Server 
        self.listen_server_enabled = tk.BooleanVar(False)
        self.toggle_listen_server = widgets.LabelInput(self.frame_main, label='Allow remote commands:', input_class=ttk.Checkbutton, label_args={'padding':[8,0,0,0]}, input_var=self.listen_server_enabled)
        self.toggle_listen_server.place(x=664, y=40)
        self.toggle_listen_server.input.state(["disabled"])
     # Quick Commands
        self.command_panel = widgets.CommandPanel(
            parent=self.frame_main,
            buttons=[
                ("Regenerate", self.on_regenerate),
                ("Reset", self.on_reset),
                ("Save", self.on_save),
                ("Custom...", self.on_custom),
            ],
            max_columns=5,
            panel_text="Commands",
        )
        self.command_panel.place(x=556, y=574)
     # End
        self.frame_main.place(x=0, y=0)

    def update(self):
        """Self-scheduling update (40ms) of various UI elements and application states.
        """
        try:
            if self.active_server != None:  # Update ConsoleViews & button states
                self.active_server.poll()
                if self.active_server.master:
                    self.update_console_view(self.console_view_master, self.active_server.master)
                if self.active_server.slave:
                    self.update_console_view(self.console_view_slave, self.active_server.slave)
                self.update_power_button_fx()
        finally:
            self.window.after(20, self.update)

    def update_info_bar(self):
        dict_server_config = self.active_server.config.as_dict()

        cluster_name = dict_server_config["NETWORK"]["cluster_name"]
        game_mode = dict_server_config["GAMEPLAY"]["game_mode"]
        max_players = dict_server_config["GAMEPLAY"]["max_players"]

        self.info_bar.name_info_value.configure(
            text=cluster_name
        )
        self.info_bar.gamemode_info_value.configure(
            text=game_mode.title()
        )
        self.info_bar.players_info_value.configure(
            text=max_players
        )

    def update_console_view(self, view, shard):
        if self.active_server:
            if shard.process:
                str_pid = str(shard.get_process_id())
                view.set_status("runnning (pid: " + str_pid + ")")
                line = shard.get_output()
                if line:
                    view.write_line(line)
            else:
                view.set_status(" - ")

    def update_power_button_fx(self):
        if self.active_server:
            if len(self.active_server.processes) > 0:
                self.btn_power.set_fx(True)
            else:
                self.btn_power.set_fx(False)

    def on_power(self): # # TODO: ResourceManager refactor
        if self.active_server:
            if len(self.active_server.processes) > 0:
                self.unload_server(clearOutput=False)
            else:
                nullrenderer = self.get_nullrenderer()
                self.active_server.start(nullrenderer)

    def on_regenerate(self):
        self.send_command("c_regenerateworld()")

    def on_reset(self):
        self.send_command("c_reset()")

    def on_save(self):
        self.send_command("c_save()")

    def on_custom(self):
        custom_command = view.DialogCustomCommand(parent=self.window).show()
        self.send_command(custom_command)

    def on_update(self):
        if self.active_server:
            self.active_server.kill_processes
        self.window.after(5000)
        os.system(os.path.realpath("./scripts/updatesteamcmd.bat"))

    def on_configure(self):
        if self.active_server:
            view.DialogConfigureServer(self.window, self.active_server, self.apply_config)

    def on_browse(self, selection_string):
        try:  # Try to create a DedicatedServer instance with user selected path
            server = DedicatedServer(selection_string, self.window)
        except:  # If unable, show warning that directory is unsuitable
            messagebox.showwarning(
                title="DST Server Control",
                message="Failed to set active server from selection.",
            )
        else:  # If successful, unload any current server and set new
            self.unload_server()
            self.set_active_server(server)

    def on_settings(self):
        """Handler for showing the application settings dialog.
        """
        view.DialogConfigureApplication(self)

    def get_nullrenderer(self): # TODO: ResourceManager refactor
        """Gets a nullrenderer with an Add-In installation taking priority over user-defined.
        """
        addin_nullrenderer = join(pathlib.Path(__file__).parents[1], "add-ins/steamcmd/steamapps/common/Don't Starve Together Dedicated Server/bin/dontstarve_dedicated_server_nullrenderer.exe")
        if os.path.exists(addin_nullrenderer):
            return addin_nullrenderer
        else:
            user_nullrenderer = self.config.get("ENVIRONMENT", "nullrenderer")
            if os.path.exists(user_nullrenderer):
                return user_nullrenderer
        return None
        
    def unload_server(self, clearOutput=True):
        """Attempts to safely shutdown any active server, waits 2 seconds before killing it and
        optionally clears any output.
        """
        if self.active_server != None:
            # Shutdown server
            self.active_server.run_command("c_shutdown()")
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
        self.widget_directory_select.set(
            "%s (%s)" % (os.path.basename(self.active_server.path), self.active_server.path)
        )
        self.update_info_bar()

        if self.active_server.master:
            self.console_view_master.set_heading(self.active_server.master.name)
        if self.active_server.slave:
            self.console_view_slave.set_heading(self.active_server.slave.name)

    def apply_config(self, target, data):
        """Takes a target (a Server or Shard) and a dict of data representing an ini 
        configuration, and applies it."""
        try:
            target.config.set_from_dict(data)
        except Exception as e:
            print(e)
    
    def send_command(self, command):
        """Helper function that forwards a command to the active server
        if one is present.

        Args:
            command (str): [description]
        """
        if self.active_server:
            self.active_server.run_command(command)

    def get_server_info(self, section, option):
        if self.active_server:
            return self.active_server.config.get(section, option)

    def quit(self):
        self.unload_server()
        self.window.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = ServerControl(root)
    root.mainloop()


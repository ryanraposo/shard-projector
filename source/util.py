from ttkthemes import ThemedTk
import pyperclip

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, colorchooser


def iter_except(function, exception):
    """Iter-like that stops on exception."""
    try:
        while True:
            yield function()
    except exception:
        return


class Mover(ThemedTk):
    def __init__(self, target_widget : ttk.Widget, target_parent : ttk.Widget, widget_name : str, increment=1):
        super().__init__(theme='equilux')
        self.configure(bg='#353535')
        self.title("Moving: " + widget_name)
        self.target_widget = target_widget
        self.widget_x = None
        self.widget_y = None
        self.target_parent = target_parent
        self.increment = increment

        btn_left = ttk.Button(self, text="<",command=self.left)
        btn_up = ttk.Button(self, text="^",command=self.up)
        btn_down = ttk.Button(self, text="v",command=self.down)
        btn_right = ttk.Button(self, text=">",command=self.right)

        self.lbl_info = ttk.Label(self, text="")
        
        self.btn_info_to_clipboard = ttk.Button(self, text="Copy", command=self.copy_to_clipboard)

        btn_left.grid(
            row=1,
            column=0
        )    
        btn_up.grid(
            row=0,
            column=1
        )
        btn_down.grid(
            row=1,
            column=1
        )
        btn_right.grid(
            row=1,
            column=2
        )

        self.lbl_info.grid(
            row=2,
            column=0
        )

        self.btn_info_to_clipboard.grid(
            row=2,
            column=1
        )

        self._update_location()
        
    def _update_location(self):
        """Updates internal values for widget location & updates display accordingly"""

        self.target_widget.update()
        self.target_parent.update()
        
        self.widget_x = self.target_widget.winfo_x()
        self.widget_y = self.target_widget.winfo_y()
        self.lbl_info.config(text="(x=" + str(self.widget_x) + ", y=" + str(self.widget_y) + ")")
        
    def _move_target(self, x : int, y : int):
        """Checks that move is within bounds and if so, re-places widget at x,y"""
        if x >= 0 and x <= self.target_parent.winfo_width():
            if y >= 0 and y <= self.target_parent.winfo_height():
                self.target_widget.place(x=x, y=y)
                
    def copy_to_clipboard(self):
        pyperclip.copy(self.lbl_info['text'])
        
        
    def left(self):
        x = self.widget_x - self.increment
        y = self.widget_y
        self._move_target(x,y)
        self._update_location()
    
    def up(self):
        x = self.widget_x
        y = self.widget_y - self.increment
        self._move_target(x,y)
        self._update_location()

    def down(self):
        x = self.widget_x
        y = self.widget_y + self.increment
        self._move_target(x,y)
        self._update_location()

    def right(self):
        x = self.widget_x + self.increment
        y = self.widget_y
        self._move_target(x,y)
        self._update_location()


# class CallEvent:
#     """A function call with optionally conditional behaviour. 
    
#     Schedule on GUI loop with anonymous functions as needed. Use the evaluate method in 
#     conjunction with the strict parameter to monitor execution flow for further handling.
    
#     Args:
#         name (str): ID for the call being registered.
#         fn (function): Function to be called.
#         conditional (function): Optional. Determines whether the call will be made. Default is None.
#         condition_unmet (function): Optional. A function to be called if the condition is not met. Default is None.
#         strict (bool): Optional. Toggle reporting of execution results. Default is False."""

#     def __init__(self, name, fn, conditional=None, condition_unmet=None, strict=False):
#         self.name = fn
#         self.fn = fn
#         self.conditional = conditional
#         self.condition_unmet = condition_unmet
#         self.strict = strict

#     def evaluate(self):
#         """Processes the CallEvent. Returns False if strict and condition was unmet.
#         """
#         if not self.conditional or self.conditional() == True:
#             self.fn()
#         else:
#             if callable(self.condition_unmet):
#                 self.condition_unmet()
#                 if self.strict:
#                     return False

# class Environment:
#     """Has methods for bootstrapping dependencies & initializing environment variables.
#     """

#     def __init__(self):
#         self.platform = self._get_platform()
#         self.programs = self._get_installed_programs()

#     def _get_platform(self) -> PLATFORMS:
#         if sys.platform == "win32":
#             return PLATFORMS.WINDOWS
#         elif sys.platform == "linux" or sys.platform == "linux2":
#             return PLATFORMS.LINUX
#         elif sys.platform == "darwin":
#             return PLATFORMS.MACOSX
    
#     def _get_installed_programs(self):
#         if self.platform == PLATFORMS.WINDOWS:
#             return wh.get_all()

#     def program_is_installed(self, patterns):
#         for each in self.programs:
#             name = each['name'].lower()
#             if all(elem in name for elem in patterns):
#                 return True
#         return False

#     def debug_search_installed_programs(self, patterns):
#         matches = []
#         for each in self.programs:
#             name = each['name'].lower()
#             if all(elem in name for elem in patterns):
#                 matches.append(name)
#         print('[debug search installed programs] matches:', matches)

# class Job:
#     """A system job with threaded queueing of stdout. Use method get_output on a scheduled
#     interval to monitor & handle output."""

#     def __init__(self, args):
#         self.process = Popen(args, stdout=PIPE, stdin=PIPE, shell=True)
#         self.q = Queue(maxsize=1024)
#         self.thread_reader = Thread(target=self._update_output, args=[self.q])
#         self.thread_reader.daemon = True
#         self.thread_reader.start()

#     def _update_output(self, q):
#         """Adds stdout of associated process to job's output queue."""
#         if self.process:
#             try:
#                 with self.process.stdout as pipe:
#                     for line in iter(pipe.readline, b""):
#                         q.put(line)
#             finally:
#                 q.put(None)


#     def get_output(self):
#         """Returns output queue of the job."""
#         for line in iter_except(self.q.get_nowait, Empty):
#             if line is None:
#                 return None
#             else:
#                 return line
    
#     def write_input(self, line):
#         """Writes the input queue of the shard to the stdin of its associated process."""
#         if self.process:
#             try:
#                 with self.process.stdin as pipe:
#                     pipe.write(line.encode())
#                 print(line + " recieved by " + self.name)
#             except:
#                 print(line + " NOT recieved by " + self.name)
    
#     def terminate(self):
#         self.process.kill()
#         self.thread_reader = None

if __name__ == "__main__":
    root = ThemedTk(theme='equilux')
    root.geometry("400x400")
    root.configure(bg="#424242")

    wee = ttk.Button(root, text="WEEE")
    wee.place(x=200,y=200)

    mover_wee = Mover(wee,root, "WEE Button")
    
    root.mainloop()
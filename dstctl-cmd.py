# This Python file uses the following encoding: utf-8
import sys, os
import subprocess

import pyfiglet

import npyscreen


def chop_cmd(cmd:str):
        chopped = cmd.split(" ")
        return chopped

class RNDSTApp(npyscreen.NPSApp):


        def main(self):

                banner = pyfiglet.figlet_format("RNDST", "slant", justify='center')

                form  = npyscreen.Form(name = 'RNDST Server Control')

                title_rndst = form.add(npyscreen.MultiLineEdit, max_height=6, value=banner)

                self.sel_update = form.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Update?",
                        values = ["Yes","No"], scroll_exit=True)             

                btn_start = form.add(npyscreen.ButtonPress,when_pressed_function=self.start_server,
                        name="Start",
                        value="Start",
                        height=5,
                        width=5,
                        max_height=5,
                        max_width=5,
                )

                btn_stop = form.add(npyscreen.ButtonPress,when_pressed_function=self.kill_all,
                        name="Stop",
                        value="Stop",
                        height=5,
                        width=5,
                        max_height=5,
                        max_width=5
                )

                btn_reset = form.add(npyscreen.ButtonPress,when_pressed_function=self.reset,
                        name="Reset",
                        value="Reset",
                        height=5,
                        width=5,
                        max_height=5,
                        max_width=5
                )

                form.edit()


        def start_server(self):
                if self.sel_update.value == 'Yes':
                        subprocess.call(['./start.bat'])
                elif self.sel_update.value == 'No':
                        subprocess.call(['./start_noupdate.bat'])


        def kill_all(self):
                proc_name = "dontstarve_dedicated_server_nullrenderer.exe"
                subprocess.Popen("taskill " + proc_name).wait()

        def reset(self):
                self.kill_all()
                self.start_server()


if __name__ == "__main__":
    global app
    app = RNDSTApp()
    app.run()
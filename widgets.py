import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import os, json, configparser


def as_dict(config):
    """
    Converts a ConfigParser object into a dictionary.

    The resulting dictionary has sections as keys which point to a dict of the
    sections options as key => value pairs.
    """
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict


class LabelInput(ttk.Frame):
    """A widget containing a label and input together. Accepts various ttk input widgets. Creates a paired ttk.Label to the left of
    those which lack a suitable label of their own. Ensures columns span entire widget contained. Optional toggle for enabling/disabling
    field."""

    def __init__(
        self,
        parent,
        toggle_enable=False,
        label="",
        input_class=ttk.Entry,
        input_var=None,
        input_args=None,
        label_args=None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Radiobutton, ttk.Button):
            input_args["text"] = label
            input_args["variable"] = input_var
            input_args["width"] = 10
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=1, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=0, column=2, sticky=(tk.W + tk.E))

        if toggle_enable:
            enabled = self.enabled = tk.BooleanVar(value=True)
            self.toggle_enable_checkbutton = ttk.Checkbutton(self, variable=enabled)
            self.toggle_enable_checkbutton.grid(row=0, column=0)

        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
         tk.W)"""

        super().grid(sticky=sticky, **kwargs)

    def get(self):
        """Get handling for input_class cases. If widget has an input variable,
        simply calls get on the variable. If widget is type ttk.Text, gets
        line char 0 to END. If no input variable, calls get on the widget."""

        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get("1.0", tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # when numeric fields are empty
            return

    def set(self, value, *args, **kwargs):
        """Set handling for widgets expecting tk.BooleanVar, widgets with variables, and tick/untick
        functionality for tk.Checkbutton and tk.Radiobutton."""

        if (
            type(self.variable) == tk.BooleanVar
        ):  # if widget expects BooleanVar, cast input to bool
            self.variable.set(bool(value))
        elif self.variable:  # for other widgets with variable, simply call set
            self.variable.set(value * args, **kwargs)
        # if Checkbutton or Radiobutton, for value=True tick button, for False untick
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:  # if ttk.Text...
            self.input.delete("1.0", tk.END)  # delete row 1 char 0 to the end
            self.input.insert("1.0", value)  # insert value at row 1 char 0
        else:  # input is a ttk.Entry with no variable
            self.input.delete(0, tk.END)  # delete row 1 char 0 to the end
            self.input.insert(0, value)  # insert value at row 1 char 0


class DialogConfirmShardDirectories(tk.Toplevel):
    def __init__(self, parent, detected_shard_directories):
        tk.Toplevel.__init__(self, parent)

        self.title("Confirm shard directories...")
        dialog_frame = ttk.Frame(self, height=300, width=300)
        dialog_frame.grid(row=0, column=0)

        self.vars = []

        self.inputs = {}
        row_count = 0
        for path in detected_shard_directories:
            var = tk.StringVar()
            self.vars.append(var)
            frame_shard = ttk.Frame(dialog_frame)
            self.inputs[row_count] = LabelInput(
                frame_shard, True, label=os.path.basename(path), label_args={'width':8}, input_var=var, input_args={'width':50}
            )
            var.set(path)
            self.inputs[row_count].grid(row=row_count, column=0)
            ttk.Button(frame_shard, text="Browse").grid(row=row_count, column=1)
            frame_shard.grid(row=row_count, column=0)
            row_count += 1

        self.button_confirm = ttk.Button(dialog_frame, text="Confirm", command=self.on_confirm)
        self.button_confirm.grid(row=row_count, column=0, pady=10, padx=30)

    def on_confirm(self, event=None):
        self.destroy()

    def show(self):
        self.wm_deiconify()
        self.wait_window()
        submitted_directories = []
        for each in self.vars:
            submitted_directories.append(each.get())
        return submitted_directories

class FrameConfigureCluster(ttk.Frame):
    """Accepts a dictionary representing a cluster.ini file and frame containing LabelInputs for
    viewing and configuring the values. Use get to retrieve its values in a similarly structured dictionary."""

    def __init__(self, parent, target_configuration=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.inputs = {}
        self.target_configuration = target_configuration
        self.initialize_widgets()

    def _get_cluster_ini_structure(self):
        with open("./data/ini/cluster_configuration.json") as json_file:
            cluster_config_structure = dict(json.load(json_file))
            return cluster_config_structure

    def initialize_widgets(self):
        """Loops through """

        cluster_configuration_json = self._get_cluster_ini_structure()
        x = 0
        for section in cluster_configuration_json.keys():
            y = 0
            frmSection = ttk.Labelframe(self, text=section)
            frmSection.grid(row=x, column=0)
            for option in cluster_configuration_json[section].keys():
                self.inputs[option] = LabelInput(
                    parent=frmSection,
                    toggle_enable=False,
                    label=option,
                    input_class=ttk.Entry,
                    label_args={"padding": [9, 0, 0, 0]},
                )
                self.inputs[option].grid(row=y, column=0)
                if self.target_configuration:
                    try:
                        target_section = self.target_configuration[section]
                        self.inputs[option].set(target_section[option])
                    except:
                        pass
                y += 1
            x += 1

    def grid(self, sticky=(tk.W + tk.E), **kwargs):
        """Override of geometry manager's grid method, supplies sticky=(tk.E +
        tk.W)"""
        super().grid(sticky=sticky, **kwargs)

    def get(
        self,
    ):  # TODO fix get method in configure cluster frame so that it returns sections as in the structure json
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data


class DialogConfigureServer:
    def __init__(self, parent, server):
        self.server = server
        window = self.window = tk.Toplevel(parent)
        # window.geometry("400x800")
        window.title("Settings")
        window.configure(bg="#424242")

        self.nbkConfigPanes = ttk.Notebook(window, width=400, height=700)
        self.nbkConfigPanes.place(x=0, y=0)
        frame_configure_cluster = FrameConfigureCluster(
            self.nbkConfigPanes, server.cluster_config
        )
        self.add_pane(frame_configure_cluster, "Cluster")

    def add_pane(self, frame, name):
        self.nbkConfigPanes.add(frame, text=name)

    def close(self):
        self.window.destroy()


def test_configure_cluster_frame():
    root = ThemedTk(theme="equilux")
    # root.geometry("800x800")
    config = configparser.ConfigParser()
    config.read(
        os.path.abspath("C:\\Users\\ryanr\\source\\dstctl\\data\\Eden\\cluster.ini")
    )
    cluster_config = as_dict(config)
    frame_cluster_config = FrameConfigureCluster(root, cluster_config)
    frame_cluster_config.grid(row=0, column=0)
    print(frame_cluster_config.get())
    root.mainloop()


# test_configure_cluster_frame()

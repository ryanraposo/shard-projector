from ttkthemes import ThemedTk

import tkinter as tk
from tkinter import ttk
import unittest
from unittest import TestCase

from view import DialogCustomCommand
 

class TkTestCase(TestCase):
    def setUp(self):
        self.root = ThemedTk(theme="equilux")
        self.pump_events()

    def tearDown(self):
        if self.root:
            self.root.destroy()
            self.pump_events()

    def pump_events(self):
        while self.root.dooneevent(tk._tkinter.ALL_EVENTS | tk._tkinter.DONT_WAIT):
            pass

class TestDialogCustomCommand(TkTestCase):
    def test_enter(self):
        dialog = DialogCustomCommand(self.root)                                                  
        self.pump_events()
        
        dialog.entry_custom_command.focus_set()
        dialog.entry_custom_command.insert(tk.END, 'test')
        dialog.entry_custom_command.event_generate('<Return>')

        self.pump_events()

        self.assertEqual(dialog.entry_custom_command.get(), "test")


unittest.main()
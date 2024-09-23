
import keyboard
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QApplication
import subprocess
import os
import time
from PyQt6.QtWidgets import QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout
from functools import partial
from PyQt6.QtGui import QTextCursor, QTextCharFormat
from PyQt6.QtCore import Qt
import re

class Schedule:
    def __init__(self, ui):
        self.ui = ui
        self.resize_table()
        
    def resize_table(self):
        count = self.ui.tableWidget_2.rowCount()
        for i in range(count):
            self.ui.tableWidget_2.setRowHeight(i, 150)
        
        

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

class ViewFlow:
    def __init__(self, ui):
        self.ui = ui

    def print(self):
        layout = self.ui.gridLayout_7
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        text = self.ui.textEdit_3.toPlainText()
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        for index, match in enumerate(matches):
            start, end = match.span()
            code = text[start:end]
            name = code.split("\n")[0].replace("# ---------------------", "").replace(" ---------------------", "")
            step_widget = QWidget()
            step_widget.setStyleSheet("border: 0px")
            step_layout = QHBoxLayout()
            button = QPushButton(parent=self.ui.scrollAreaWidgetContents_2, text=name)
            button.setStyleSheet("background-color: blue; color: white")
            button.clicked.connect(lambda checked, i=index: self.highlight_code(i))
            step_layout.addWidget(button)
            delete_button = QPushButton(parent=self.ui.scrollAreaWidgetContents_2, text="X")
            delete_button.setStyleSheet("background-color: red")
            delete_button.clicked.connect(lambda checked, i=index: self.delete_step(i))
            step_layout.addWidget(delete_button)
            step_widget.setLayout(step_layout)
            step_widget.setFixedSize(300, 60)
            delete_button.setFixedSize(30, 30)
            layout.addWidget(step_widget)
            
            

    def delete_step(self, index):
        text = self.ui.textEdit_3.toPlainText()
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            match = matches[index]
            start, end = match.span()
            text = text[:start] + text[end:]
            text = text.strip().strip("\n")
            self.ui.textEdit_3.setPlainText(text)
            self.print()

    def highlight_code(self, index):
        text = self.ui.textEdit_3.toPlainText()
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            for match in matches:
                start, end = match.span()
                cursor = self.ui.textEdit_3.textCursor()
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
                char_format = QTextCharFormat()
                char_format.setBackground(Qt.GlobalColor.white)
                cursor.setCharFormat(char_format)
                cursor.setPosition(end)
        text = self.ui.textEdit_3.toPlainText()
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            match = matches[index]
            start, end = match.span()
        cursor = self.ui.textEdit_3.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        char_format = QTextCharFormat()
        char_format.setBackground(Qt.GlobalColor.green)
        cursor.setCharFormat(char_format)
        cursor.setPosition(end)
        
        
            
        
            
        
        

# tạo 1 hàm lắng nghe phím bấm sau đó trả về ký tự tương ứng
def listen_key():
    key = keyboard.read_event()
    if key.event_type == keyboard.KEY_DOWN:
        return key.name
    
    
class Scripts:
    def __init__(self, ui, dashboard):
        self.ui = ui
        self.dashboard = dashboard
        self.connect_button()
        self.view_flow = ViewFlow(ui)
    
        
    # Tab Chrome
    def add_chrome(self):
        link = self.ui.lineEdit_19.text()
        code_python = '''# --------------------- ADD CHROME {link} ---------------------
import webbrowser
webbrowser.open_new_tab('{link}')
import time
time.sleep(1)
# --------------------------------------------------------'''.format(link=link)
        # ghi thêm textedit ở đây
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_sleep(self):
        time = self.ui.lineEdit_20.text()
        time_random = self.ui.lineEdit_21.text()
        code_python = '''# --------------------- ADD SLEEP {time_} ---------------------
import time
import random
time.sleep({time} - random.randint(-{time_random}, {time_random}))
# --------------------------------------------------------'''.format(time=time, time_random=time_random, time_=f'{time} + random.randint(-{time_random}, {time_random})')
        # ghi thêm textedit ở đây
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_chrome_new_undetected_chromedriver(self):
        code_python = '''# --------------------- ADD CHROME NEW UNDETECTED CHROMEDRIVER ---------------------
from undetected_chromedriver import Chrome, ChromeOptions
options = ChromeOptions()
driver = Chrome(options=options)
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_resize_chrome(self):
        width = self.ui.lineEdit_95.text()
        height = self.ui.lineEdit_96.text()
        code_python = '''# --------------------- ADD RESIZE CHROME {width}x{height} ---------------------
driver.set_window_size({width}, {height})
import time
time.sleep(1)
# --------------------------------------------------------'''.format(width=width, height=height)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_maximize_chrome(self):
        code_python = '''# --------------------- ADD MAXIMIZE CHROME ---------------------
driver.maximize_window()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_zoom_chrome(self):
        zoom = self.ui.lineEdit_98.text()
        code_python = '''# --------------------- ADD ZOOM CHROME {zoom}% ---------------------
driver.execute_script("document.body.style.zoom='{zoom}%'")
import time
time.sleep(1)
# --------------------------------------------------------'''.format(zoom=zoom)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_go_to_url(self):
        url = self.ui.lineEdit_99.text()
        code_python = '''# --------------------- ADD GO TO URL {url} ---------------------
driver.get('{url}')
import time
time.sleep(1)
# --------------------------------------------------------'''.format(url=url)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_chrome_profile(self):
        profile = self.ui.lineEdit_77.text()
        code_python = '''# --------------------- ADD CHROME PROFILE ---------------------
import undetected_chromedriver as uc
import time
options = uc.ChromeOptions()
profile = 'C:/Users/Admin/AppData/Local/Google/Chrome/User Data/'
options.add_argument(f'--user-data-dir=' + profile)
options.add_argument('--profile-directory={}')
driver = uc.Chrome(options=options)
time.sleep(1)
# --------------------------------------------------------'''.format(profile)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    # Tab Keyboard
    def get_key(self):
        key = listen_key()
        self.ui.lineEdit_83.setText(key)
    def add_key(self):
        key = self.ui.lineEdit_83.text()
        code_python = '''# --------------------- ADD KEY {key} ---------------------
import pyautogui
pyautogui.press('{key}')
import time
time.sleep(1)
# --------------------------------------------------------'''.format(key=key)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_text_keyboard(self):
        text = self.ui.lineEdit_72.text()
        code_python = f'''# --------------------- ADD TEXT KEYBOARD {text} ---------------------
import pyautogui
import time
import random
for s in '{text}':
    pyautogui.typewrite(s, interval=random.randint(1,10)/50)
time.sleep(1)
# --------------------------------------------------------'''.format(text=text)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def get_key_multi(self):
        key = listen_key()
        # lấy key hiện tại trong lineedit
        key_current = self.ui.lineEdit_87.text().split(" ")
        key_current = [key for key in key_current if key != ""]
        key_current.append(key)
        self.ui.lineEdit_87.setText(" ".join(key_current))
    def add_key_multi(self):
        key = self.ui.lineEdit_87.text()
        keys = key.split(" ")
        keys_formatted = "', '".join(keys)
        code_python = '''# --------------------- ADD KEY MULTI {keys} ---------------------
import pyautogui
pyautogui.hotkey('{keys}')
import time
time.sleep(1)
# --------------------------------------------------------'''.format(keys=keys_formatted)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
        
    # Tab Mouse
    def get_boundary(self):
        # Lấy tọa độ từ clipboard
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            x, y, width, height = map(int, text.split(","))
            self.ui.lineEdit_90.setText(str(x))
            self.ui.lineEdit_91.setText(str(y))
            self.ui.lineEdit_89.setText(str(width))
            self.ui.lineEdit_88.setText(str(height))
    def get_base64_image(self):
        # lấy base64 từ clipboard
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if text:
            self.ui.lineEdit_102.setText(text)
    def add_mouse_move_random_image(self):
        base64_image = self.ui.lineEdit_102.text()
        code_python = '''# --------------------- ADD MOUSE MOVE RANDOM IMAGE ---------------------
import pyautogui
import random
import time
import math
import base64
from PIL import Image, ImageGrab
from io import BytesIO
import cv2
import numpy as np
def get_x_y_w_h_from_base64(base64_string):
    screenshot = ImageGrab.grab()
    screenshot.save('1.png')
    with open('2.png', 'wb') as file:
        file.write(base64.b64decode(base64_string))
    image = cv2.imread('1.png')
    template = cv2.imread('2.png')
    w, h = template.shape[1], template.shape[0]
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    threshold = 0.8
    match_locations = np.where(result >= threshold)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    x, y = top_left
    w, h = bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]
    return x, y, w, h
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)
x_start, y_start = pyautogui.position()
x, y, w, h = get_x_y_w_h_from_base64('{base64_image}')
x_end = random.randint(x, x + w)
y_end = random.randint(y, y + h)
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)

# --------------------------------------------------------'''.format(base64_image=base64_image)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_mouse_move_random_in_boundary(self):
        x = self.ui.lineEdit_90.text()
        y = self.ui.lineEdit_91.text()
        width = self.ui.lineEdit_89.text()
        height = self.ui.lineEdit_88.text()
        code_python = '''# --------------------- ADD MOUSE MOVE RANDOM IN BOUNDARY {x}, {y}, {width}, {height} ---------------------
import pyautogui
import random
import time
import math
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)
x_start, y_start = pyautogui.position()
x_end = random.randint({}, {})
y_end = random.randint({}, {})
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)
# --------------------------------------------------------'''.format(int(x), int(x) + int(width), int(y), int(y) + int(height),x=int(x), y=int(y), width=int(width), height=int(height))
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
        
    def add_mouse_move(self):
        x = self.ui.lineEdit_85.text()
        y = self.ui.lineEdit_84.text()
        code_python = '''# --------------------- ADD MOUSE MOVE {x}, {y} ---------------------
import pyautogui
import random
import time
import math
def move_like_human(x_start, y_start, x_end, y_end, duration):
    steps = random.randint(1, 7)  # Giảm số bước để di chuyển nhanh hơn
    sleep_time = duration / steps
    for step in range(steps):
        t = step / (steps - 1)  # Đảm bảo t = 1 ở bước cuối cùng
        ease_t = (math.sin((t - 0.5) * math.pi) + 1) / 2  # Hiệu ứng di chuyển mượt
        x = x_start + (x_end - x_start) * ease_t
        y = y_start + (y_end - y_start) * ease_t
        
        pyautogui.moveTo(x, y)
        time.sleep(sleep_time)  # Thời gian nghỉ giữa mỗi bước
    pyautogui.moveTo(x_end, y_end)
x_start, y_start = pyautogui.position()
x_end = {x}
y_end = {y}
move_like_human(x_start, y_start, x_end, y_end, duration=0.02)
time.sleep(1)
# --------------------------------------------------------'''.format(x=x, y=y)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_mouse_right_click(self):
        code_python = '''# --------------------- ADD MOUSE RIGHT CLICK ---------------------
import pyautogui
pyautogui.rightClick()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_mouse_left_click(self):
        code_python = '''# --------------------- ADD MOUSE LEFT CLICK ---------------------
import pyautogui
pyautogui.leftClick()
import time
time.sleep(1)
# --------------------------------------------------------'''
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    def add_mouse_scroll(self):
        wheel = self.ui.lineEdit_86.text()
        # whell sẽ là số âm nếu muốn cuộn lên, dương nếu muốn cuộn xuống
        code_python = '''# --------------------- ADD MOUSE SCROLL {wheel} ---------------------
import pyautogui
pyautogui.scroll({wheel})
import time
time.sleep(1)
# --------------------------------------------------------'''.format(wheel=wheel)
        self.ui.textEdit_3.append(code_python)
        self.view_flow.print()
    
    def install(self):
        # update pip trước
        subprocess.run(['python.exe', '-m', 'pip', 'install', '--upgrade', 'pip'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        # cài đặt các thư viện cần thiết
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        
        
    def run_test(self):
        # lấy code từ textedit sau đó chạy
        code = self.ui.textEdit_3.toPlainText()
        # lưu code vào file
        with open('temp.py', 'w', encoding='utf-8') as file:
            file.write(code)
        # tạo 1 thread chạy exec code để không block UI
        import threading
        def run_code():
            # cài đặt các thư viện cần thiết
            self.install()
            subprocess.run(['python', 'temp.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        threading.Thread(target=run_code).start()
    def delete_step(self):
        # xóa bước cuối cùng
        text = self.ui.textEdit_3.toPlainText()
        import re
        # Sửa lại biểu thức chính quy để khớp với đoạn văn bản
        pattern = r'# ---------------------.*?# --------------------------------------------------------'
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if matches:
            # xóa bước cuối cùng
            last_match = matches[-1]
            start, end = last_match.span()
            text = text[:start] + text[end:]
            self.ui.textEdit_3.setPlainText(text)
        else:
            self.ui.textEdit_3.setPlainText('')
        self.view_flow.print()
    def delete_all_step(self):
        self.ui.textEdit_3.setPlainText('')
        self.view_flow.print()
    def save_file(self):
        noti = QMessageBox()
        noti.setWindowTitle("Save file")
        noti.setText("Vui lòng nhập tên file để lưu")
        noti.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        noti.setDefaultButton(QMessageBox.StandardButton.Ok)
        lineedit = QLineEdit()
        lineedit.setPlaceholderText("Enter file name")
        noti.layout().addWidget(lineedit)
        ret = noti.exec()
        if ret == QMessageBox.StandardButton.Ok:
            file_name = lineedit.text()
            if file_name:
                with open(f'./scripts/{file_name}.py', 'w', encoding='utf-8') as file:
                    file.write(self.ui.textEdit_3.toPlainText())
        
        self.dashboard.add_item_combobox(self.ui.comboBox)

        
    def connect_button(self):
        self.ui.pushButton_27.clicked.connect(self.add_chrome)
        self.ui.pushButton_28.clicked.connect(self.add_sleep)
        self.ui.pushButton_77.clicked.connect(self.get_key)
        self.ui.pushButton_78.clicked.connect(self.add_key)
        self.ui.pushButton_69.clicked.connect(self.add_text_keyboard)
        self.ui.pushButton_83.clicked.connect(self.get_key_multi)
        self.ui.pushButton_84.clicked.connect(self.add_key_multi)
        self.ui.pushButton_80.clicked.connect(self.add_mouse_move)
        self.ui.pushButton_81.clicked.connect(self.add_mouse_left_click)
        self.ui.pushButton_61.clicked.connect(self.add_mouse_right_click)
        self.ui.pushButton_82.clicked.connect(self.add_mouse_scroll)
        self.ui.pushButton_86.clicked.connect(self.add_mouse_move_random_in_boundary)
        self.ui.pushButton_26.clicked.connect(self.add_chrome_new_undetected_chromedriver)
        self.ui.pushButton_95.clicked.connect(self.add_resize_chrome)
        self.ui.pushButton_94.clicked.connect(self.add_maximize_chrome)
        self.ui.pushButton_97.clicked.connect(self.add_zoom_chrome)
        self.ui.pushButton_100.clicked.connect(self.add_mouse_move_random_image)
        self.ui.pushButton_101.clicked.connect(self.get_base64_image)
        self.ui.pushButton_90.clicked.connect(self.get_boundary)
        self.ui.pushButton_98.clicked.connect(self.add_go_to_url)
        self.ui.pushButton_74.clicked.connect(self.add_chrome_profile)
        
        
        self.ui.pushButton_22.clicked.connect(self.run_test)
        self.ui.pushButton_23.clicked.connect(self.delete_step)
        self.ui.pushButton_24.clicked.connect(self.save_file)
        self.ui.pushButton_25.clicked.connect(self.delete_all_step)
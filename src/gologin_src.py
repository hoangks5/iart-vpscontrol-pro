from PyQt6.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import  QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTableWidgetItem
import requests
import os
import json
    

def get_flag_url(country_code):
    # Đường dẫn lưu trữ cờ quốc gia
    flags_dir = "flags"
    if not os.path.exists(flags_dir):
        os.makedirs(flags_dir)
    
    # Đường dẫn file cờ quốc gia
    flag_path = os.path.join(flags_dir, f"{country_code}.png")
    
    # Kiểm tra xem file cờ quốc gia đã tồn tại chưa
    if os.path.exists(flag_path):
        print(f"Flag for {country_code} already exists. Loading from local.")
        return flag_path
    else:
        print(f"Downloading flag for {country_code}.")
        response = requests.get(f'https://restcountries.com/v3.1/alpha/{country_code}')
        data = response.json()
        flag_url = data[0]['flags']['png']
        
        # Tải ảnh từ URL
        img_data = requests.get(flag_url).content
        with open(flag_path, 'wb') as file:
            file.write(img_data)
        
        return flag_path


def download_image(file_path):
    image = QPixmap()
    image.load(file_path)
    return image


def get_script_name():
    # đọc các file .py trong thư mục scripts
    list_script = []
    for file in os.listdir("scripts"):
        if file.endswith(".py"):
            list_script.append(file)
    return list_script

class GoLogin:
    def __init__(self, ui):
        self.ui = ui
        self.resize_table_widget_3()
        self.connect_button()
        self.load_profile()
        
    def resize_table_widget_3(self):
        self.ui.tableWidget_3.setColumnWidth(0, 30)
        self.ui.tableWidget_3.setColumnWidth(1, 200)
        self.ui.tableWidget_3.setColumnWidth(2, 150)
        self.ui.tableWidget_3.setColumnWidth(3, 200)
        
    def get_script_name():
    # đọc các file .py trong thư mục scripts
        list_script = []
        for file in os.listdir("scripts"):
            if file.endswith(".py"):
                list_script.append(file)
        return list_script
    def add_item_combobox(self, combobox):
        # xóa item cũ
        combobox.clear()
        list_script = get_script_name()
        combobox.addItems(list_script)
    def connection_login(self):
        api_key = self.ui.lineEdit_2.text()
        url = "https://api.gologin.com/browser/v2"
        payload = {}
        headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            # lưu response vào file json
            import json
            with open("src/json/gologin_profile.json", "w") as f:
                f.write(json.dumps(response.json()))
        else:
            QMessageBox.critical(None, "Error", "API Key is invalid")
    def load_select(self):
        for i in range(self.ui.tableWidget_3.rowCount()):
            checkbox = QCheckBox()
            checkbox.setChecked(False)  # Initially unchecked
            checkbox_layout = QWidget()
            checkbox_layout.setLayout(QHBoxLayout())
            checkbox_layout.layout().addWidget(checkbox)
            checkbox_layout.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.tableWidget_3.setCellWidget(i, 0, checkbox_layout)
    def load_profile(self):
        # kiểm tra file json có tồn tại không
        if not os.path.exists("src/json/gologin_profile.json"):
            return
        else:
            with open("src/json/gologin_profile.json", "r", encoding="utf-8") as f:
                data = f.read()
                data = json.loads(data)
                data = data["profiles"]
                # lấy thông tin profile
                self.ui.tableWidget_3.setRowCount(len(data))
                for i, profile in enumerate(data):
                    self.ui.tableWidget_3.setItem(i, 1, QTableWidgetItem(profile["name"]))
                    self.combobox = QComboBox(parent=self.ui.widget_4)
                    self.combobox.setStyleSheet("QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
                    self.add_item_combobox(self.combobox)
                    self.combobox.setCurrentText(self.ui.comboBox.currentText())
                    self.ui.tableWidget_3.setCellWidget(i, 2, self.combobox)
                    if 'host' in profile["proxy"]:
                        self.ui.tableWidget_3.setItem(i, 3, QTableWidgetItem(profile["proxy"]["host"]))
        self.load_select()
    def connect_button(self):
        self.ui.pushButton_17.clicked.connect(self.connection_login)

        
    
        
    

    
    
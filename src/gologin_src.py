from PyQt6.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QPushButton, QComboBox, QProgressBar
from PyQt6.QtCore import  QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QTableWidgetItem
import requests
import os
import json
from src.check_score_profile_gologin import *


class ThreadCheckScoreProfile(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self, api_key, parent=None):
        super(ThreadCheckScoreProfile, self).__init__(parent)
        self.api_key = api_key
        self.list_profile_id = list_profile_id(api_key)
        print(self.list_profile_id)
    def run(self):
        for profile_id in self.list_profile_id:
            get_score(profile_id, self.api_key)
            self.finished.emit()
        
        


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

def check_info_profil_id(profile_id):
    # kiểm tra file json có tồn tại không
    if not os.path.exists(f"src/json/score/{profile_id}.json"):
        return False
    else:
        with open(f"src/json/score/{profile_id}.json", "r", encoding="utf-8") as f:
            data = f.read()
            data = json.loads(data)
            return data

def get_script_name():
    # đọc các file .py trong thư mục scripts
    list_script = []
    for file in os.listdir("scripts"):
        if file.endswith(".py"):
            list_script.append(file)
    return list_script

def set_progress_color(progress_bar, value):
    if value <= 20:
        color = "red"
    elif value <= 40:
        color = "orange"
    elif value <= 60:
        color = "yellow"
    elif value <= 80:
        color = "lightgreen"
    else:
        color = "green"
    
    # Sử dụng stylesheet để đổi màu thanh progress bar
    progress_bar.setStyleSheet("""
        QProgressBar::chunk {
            background-color: """ + color + """;
        }
        QProgressBar {
    border: 2px solid #555;  /* Đường viền xung quanh */
    border-radius: 10px;  /* Bo góc thanh tiến trình */
    background-color: #f0f0f0;  /* Màu nền của thanh */
    text-align: center;
    color: black;  /* Màu chữ của số phần trăm */
    font-weight: bold;  /* Chữ đậm */
}
QProgressBar::chunk {
    background-color: {color};  /* Sử dụng màu sắc từ hàm set color */
    border-radius: 10px;  /* Bo góc của phần đã tải */
    margin: 0 1px;  /* Tạo khoảng cách giữa các phần */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);  /* Hiệu ứng bóng */
}

    """)

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
    def get_row_selected(self):
        selected_rows = []
        for i in range(self.ui.tableWidget_3.rowCount()):
            checkbox = self.ui.tableWidget_3.cellWidget(i, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                selected_rows.append(i)
        return selected_rows
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
            self.load_profile()
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
        # xóa dữ liệu cũ
        self.ui.tableWidget_3.setRowCount(0)
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
                    
                    profile_id = profile["id"]
                    data = check_info_profil_id(profile_id)
                    if data != False:
                        if 'country' in data:
                            country_code = data["country"].lower()
                            flag_url = get_flag_url(country_code)
                            flag_image = download_image(flag_url)
                            flag_icon = QIcon(flag_image)
                            flag_item = QTableWidgetItem(data["ip_address"])
                            flag_item.setIcon(flag_icon)
                            self.ui.tableWidget_3.setItem(i, 3, flag_item)
                        
                        progress_proxy = QProgressBar()
                        progress_proxy.setValue(data["score_proxy"])
                        set_progress_color(progress_proxy, data["score_proxy"])
                        self.ui.tableWidget_3.setCellWidget(i, 4, progress_proxy)
                        progress_browser = QProgressBar()
                        progress_browser.setValue(data["score_browser"])
                        set_progress_color(progress_browser, data["score_browser"])
                        self.ui.tableWidget_3.setCellWidget(i, 5, progress_browser)
                        
                        
        self.load_select()
    def push_select_all(self, tableWidget):
        # kiểm tra xem tất cả row đã được chọn chưa
        is_all_checked = True
        for i in range(tableWidget.rowCount()):
            checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
            if not checkbox.isChecked():
                is_all_checked = False
        # nếu tất cả row đã được chọn thì bỏ chọn tất cả
        if is_all_checked:
            for i in range(tableWidget.rowCount()):
                checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
                checkbox.setChecked(False)
        else:
            for i in range(tableWidget.rowCount()):
                checkbox = tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
                checkbox.setChecked(True)
                
    def get_row_selected(self):
        selected_rows = []
        for i in range(self.ui.tableWidget_3.rowCount()):
            checkbox = self.ui.tableWidget_3.cellWidget(i, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                selected_rows.append(i)
        return selected_rows
    
    def scan_profile(self):
        api_key = self.ui.lineEdit_2.text()
        if api_key == "":
            QMessageBox.critical(None, "Error", "API Key is invalid")
            return
        self.connection_login()
        self.thread = ThreadCheckScoreProfile(api_key)
        self.thread.finished.connect(self.load_profile)
        self.thread.start()
        
    
    def connect_button(self):
        self.ui.pushButton_17.clicked.connect(self.connection_login)
        self.ui.pushButton_18.clicked.connect(lambda: self.push_select_all(self.ui.tableWidget_3))
        self.ui.pushButton_29.clicked.connect(self.scan_profile)
        
    
        
    

    
    
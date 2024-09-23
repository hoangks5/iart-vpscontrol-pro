from PyQt6.QtWidgets import QTableWidgetItem, QCheckBox, QWidget, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import  QTimer, Qt
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6 import QtCore
import requests
import os
import datetime
import random
import json
import socket
import redis

def send_file_to_redis(file_path, redis_key):
    r = redis.Redis(host='3.18.29.6', port=6379, db=0)
    r.set(redis_key, open(file_path, 'rb').read())
    r.save()
    

def send_command(ip, port, file_path, client):
    # gửi dữ liệu đến redis
    redis_key = f"{ip}:{port}:{random.randint(1000, 9999)}:{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
    send_file_to_redis(file_path, redis_key)
    
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (ip, int(port))
    client_socket.connect(server_address)
    command = {
        'cmd': 'python',
        'clients': client,
        'redis_key': redis_key,  
    }
    print('Sending redis_key to server:', redis_key)
    client_socket.sendall(json.dumps(command).encode())
    

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

class Dashboard:
    def __init__(self, ui):
        self.ui = ui
        self.resize_table()
        self.add_item_combobox(self.ui.comboBox)

    def get_row_selected(self):
        selected_rows = []
        for i in range(self.ui.tableWidget.rowCount()):
            checkbox = self.ui.tableWidget.cellWidget(i, 0).layout().itemAt(0).widget()
            if checkbox.isChecked():
                selected_rows.append(i)
        return selected_rows
    
    def setup_script(self):
        # lấy script từ combobox
        script_name_now = self.ui.comboBox.currentText()
        # lấy row được chọn
        selected_rows = self.get_row_selected()
        for row in selected_rows:
            # đổi combobox thành script đã chọn
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
            self.combobox.setCurrentText(script_name_now)
            self.ui.tableWidget.setCellWidget(row, 4, self.combobox)
            # thêm log
            self.add_log_cmd(f"📜 [{self.get_current_time()}] [{self.ui.tableWidget.item(row, 2).text()}] Script {script_name_now} has been added to client {self.ui.tableWidget.item(row, 1).text()}")
           
            
    def add_log_cmd(self, message):
        self.ui.textEdit.append(message)  # Append the message to QTextEdit
    def resize_table(self):
        # thiết lập kích thước cột cho tableWidget reponsive với kích thuớc cửa sổ tính theo %
        table_width = self.ui.tableWidget.width()
        self.ui.tableWidget.setColumnWidth(0, int(table_width * 0.01))
        self.ui.tableWidget.setColumnWidth(1, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(2, int(table_width * 0.3))
        self.ui.tableWidget.setColumnWidth(3, int(table_width * 0.35))
        self.ui.tableWidget.setColumnWidth(4, int(table_width * 0.2))
        self.ui.tableWidget.setColumnWidth(5, int(table_width * 0.25))
        self.ui.tableWidget.setColumnWidth(6, int(table_width * 0.15))
        self.ui.tableWidget.setColumnWidth(7, int(table_width * 0.15))
        
    
        
    
    def add_item_combobox(self, combobox):
        # xóa item cũ
        combobox.clear()
        list_script = get_script_name()
        combobox.addItems(list_script)
    
    def update_clients(self, clients):
        print(clients)
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setRowCount(len(clients))
        for i, client in enumerate(clients):
            # cột 0 là ô checkbox
            self.ui.tableWidget.setItem(i, 0, QTableWidgetItem())
            self.ui.tableWidget.setItem(i, 1, QTableWidgetItem(client['hostname']))
            ip = QTableWidgetItem(client['ip'])
            ip.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 2, ip)
            country_code = client['country']
            flag_url = get_flag_url(country_code)
            flag_image = download_image(flag_url)
            # Create QIcon from QPixmap and set it to QTableWidgetItem
            flag_icon = QIcon(flag_image)
            flag_item = QTableWidgetItem(f"{client['city']} - {client['country']} | {client['lat']}, {client['lon']}")
            #flag_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            flag_item.setIcon(flag_icon)
            self.ui.tableWidget.setItem(i, 3, flag_item)
            
            # tạo status có icon online trong text
            status = QTableWidgetItem("🟢 Online")
            status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.tableWidget.setItem(i, 5, status)
            
            view_screen = QPushButton("🖥️")
            view_screen.setStyleSheet("QPushButton{\n"
"border-radius:5px;\n"
"border: 2px solid #23074d;\n"
"background-color: #cc5333;\n"
"color:#FFB6C1;\n"
"height: 40px;\n"
"width: 120px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #009fff ;\n"
"    background-color:#23074d;\n"
"            }\n"
"QPushButton:pressed {\n"
"                background-color: #5650de; /* Màu nền khi nhấn */\n"
"            }\n"
"\n"
"QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            view_screen.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)       
            self.ui.tableWidget.setCellWidget(i, 6, view_screen)

            button_setting = QPushButton("⚙️")
            button_setting.setStyleSheet("QPushButton{\n"
"border-radius:5px;\n"
"border: 2px solid #23074d;\n"
"background-color: #cc5333;\n"
"color:#FFB6C1;\n"
"height: 40px;\n"
"width: 120px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 2px solid #009fff ;\n"
"    background-color:#23074d;\n"
"            }\n"
"QPushButton:pressed {\n"
"                background-color: #5650de; /* Màu nền khi nhấn */\n"
"            }\n"
"\n"
"QComboBox{\n"
"background-color: rgb(85, 255, 127);\n"
"border-radius: 5px;\n"
"border: 2px solid #23074d;\n"
"height:40px;\n"
"width: 105px;\n"
"}\n"
"")
            button_setting.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            self.ui.tableWidget.setCellWidget(i, 7, button_setting)
            
            # nhúng combobox vào tablewidget
            # copy self.ui.comboBox 
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
            self.ui.tableWidget.setCellWidget(i, 4, self.combobox)
            
        
            
        self.load_select()
    
    
    
    
    def load_select(self):
        for i in range(self.ui.tableWidget.rowCount()):
            checkbox = QCheckBox()
            checkbox.setChecked(False)  # Initially unchecked
            checkbox_layout = QWidget()
            checkbox_layout.setLayout(QHBoxLayout())
            checkbox_layout.layout().addWidget(checkbox)
            checkbox_layout.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            checkbox_layout.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.tableWidget.setCellWidget(i, 0, checkbox_layout)
            
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
    
    
    
    
    def get_current_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        
    def run_script(self, ip, port):
        # lấy row được chọn
        selected_rows = self.get_row_selected()

        for row in selected_rows:
            # lấy script từ combobox
            script_name_now = self.ui.tableWidget.cellWidget(row, 4).currentText()
            # thêm log
            self.add_log_cmd(f"📜 [{self.get_current_time()}] [{self.ui.tableWidget.item(row, 2).text()}] Script {script_name_now} is running")
            client = f"{self.ui.tableWidget.item(row, 2).text()}:{self.ui.tableWidget.item(row, 1).text()}"
            # gửi lệnh đến server
            send_command(ip, port, f"scripts/{script_name_now}", [client])
            
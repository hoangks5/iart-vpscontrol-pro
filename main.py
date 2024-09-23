from mainui_v2 import Ui_MainWindow
from login import Ui_MainWindow as Ui_Login
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QVBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QSize
import sys
from connect_socket import *
from src.dashboard import Dashboard
from src.load_clients_thread import LoadClientsThread
from src.scripts import Scripts
import sys
from src.get_boundary_screen import ScreenCapture
from src.get_image_screen import ScreenCapture as ScreenCapture2
from src.taskbar import TaskBar
import redis
from pynput import mouse
from src.tool_tip_groupbox import DescriptionGroupBox
from src.schedule import Schedule
from src.gologin_src import GoLogin


        

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.load_config()
        
    def check_server_redis(self, ip, port):
        try:
            r = redis.Redis(host=ip, port=port, db=0)
            r.set('foo', 'bar')
            if r.get('foo') == b'bar':
                return True
            else:
                return False
        except Exception as e:
            return False
    def load_config(self):
        # kiểm tra file config
        try:
            with open("src/config.json", "r") as f:
                config = json.loads(f.read())
                self.ui.lineEdit.setText(config["ip_socket"] + ":" + config["port_socket"])
                self.ui.lineEdit_2.setText(config["ip_redis"])
        except Exception as e:
            pass
    def connect_button(self):
        self.ui.pushButton.clicked.connect(self.login)
    def check_socket(self):
        if self.ui.lineEdit.text() == "" or self.ui.lineEdit_2.text() == "":
            QMessageBox.critical(None, "Error", "Vui lòng nhập đầy đủ thông tin")
            return False
       
        socket_address = self.ui.lineEdit.text().split(":")
        if len(socket_address) == 2:
            ip, port = socket_address
            status = check_server_socket(ip, int(port))
            if status == False:
                QMessageBox.critical(None, "Error", "Không thể kết nối đến server socket")
                return False
            else:
                # kiểm tra địa chỉ redis
                redis_address = self.ui.lineEdit_2.text()
                if len(redis_address.split(":")) == 2:
                    ip, port = redis_address.split(":")
                    status = self.check_server_redis(ip, int(port))
                    if status == False:
                        QMessageBox.critical(None, "Error", "Không thể kết nối đến server redis")
                        return False
                    else:
                        return True
                else:
                    QMessageBox.critical(None, "Error", "Địa chỉ redis không hợp lệ")
                    return False
        else:
            QMessageBox.critical(None, "Error", "Địa chỉ socket không hợp lệ")
            return False
        
    
    def login(self):
        if self.check_socket() == True:
            self.ip_socket = self.ui.lineEdit.text().split(":")[0]
            self.port_socket = self.ui.lineEdit.text().split(":")[1]
            # lưu thông tin vào file config
            with open("src/config.json", "w") as f:
                f.write(json.dumps({
                    "ip_socket": self.ip_socket,
                    "port_socket": self.port_socket,
                    "ip_redis": self.ui.lineEdit_2.text()
                }))
                
            self.main_window = MainWindow(self.ip_socket, self.port_socket)
            self.main_window.show()
            self.main_window.connect_button()
            self.close()
        else:
            QMessageBox.critical(None, "Error", "Không thể kết nối đến server")
            
    
    def show(self):
        super().show()
        self.connect_button()
        
 
    
class MainWindow(QMainWindow):
    def __init__(self, ip_socket, port_socket):
        super().__init__()
        self.ip_socket = ip_socket
        self.port_socket = port_socket
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()
      
        
        
        self.taskbar = TaskBar(self.ui)
        self.dashboard = Dashboard(self.ui)
        self.scipts = Scripts(self.ui, self.dashboard)
        self.schedule = Schedule(self.ui)
        self.gologin = GoLogin(self.ui)
        self.description_groupbox = DescriptionGroupBox(self.ui)
        
        self.load_clients_thread = LoadClientsThread(self.ip_socket, self.port_socket)
        self.load_clients_thread.clients.connect(self.dashboard.update_clients)
        self.load_clients_thread.start()
    
        
    
    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()
        # disconnect thread
        self.load_clients_thread.terminate()
        
    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Chuột được nhấn tại vị trí: ({x}, {y})")
            self.ui.lineEdit_85.setText(str(x))
            self.ui.lineEdit_84.setText(str(y))
            # Sau khi lấy tọa độ, bạn có thể ngừng lắng nghe
            return False
        
    def get_mouse_boundary(self):
        self._original_geometry = self.geometry()
        self._original_state = self.windowState()
        self._original_pos = self.pos()
        self._original_size = self.size()
        self.hide()
        time.sleep(1)
        window = ScreenCapture(self)
        window.setParent(self)
        self.setMouseTracking(True)
        self.showFullScreen()

        window.finished.connect(self.restore_window)
    
    def get_base64_image_screen(self):
        self._original_geometry = self.geometry()
        self._original_state = self.windowState()
        self._original_pos = self.pos()
        self._original_size = self.size()
        self.hide()
        time.sleep(1)
        window = ScreenCapture2(self)   
        window.setParent(self)
        self.setMouseTracking(True)
        self.showFullScreen()
        window.finished.connect(self.restore_window)
    
        
        
    def restore_window(self):
        # Khôi phục trạng thái và kích thước ban đầu của cửa sổ chính
        self.setGeometry(self._original_geometry)
        self.setWindowState(self._original_state)
        self.move(self._original_pos)
        self.resize(self._original_size)
        self.show()
        
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
    
        
        
    def get_mouse_position(self):
        self.hide()
        time.sleep(0.5)
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        self.show()
    def connect_button(self):
        self.ui.pushButton_10.clicked.connect(self.logout)
        self.ui.pushButton_11.clicked.connect(lambda: self.dashboard.push_select_all(self.ui.tableWidget))
        self.ui.pushButton_12.clicked.connect(self.dashboard.setup_script)
        self.ui.pushButton_14.clicked.connect(lambda : self.dashboard.run_script(self.ip_socket, self.port_socket))
        #appflow
        self.ui.pushButton_85.clicked.connect(self.get_mouse_boundary)
        self.ui.pushButton_79.clicked.connect(self.get_mouse_position)
        self.ui.pushButton_99.clicked.connect(self.get_base64_image_screen)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
        
        
        
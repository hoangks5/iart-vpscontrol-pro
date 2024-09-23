import sys
import psutil
import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout


class SystemMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập giao diện
        self.setWindowTitle("Real-Time System Monitor")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()

        # Tạo đồ thị CPU
        self.cpu_plot = pg.PlotWidget(title="CPU Usage (%)")
        self.cpu_plot.setYRange(0, 100)
        self.cpu_curve = self.cpu_plot.plot(pen=pg.mkPen('r', width=2))

        # Tạo đồ thị RAM
        self.ram_plot = pg.PlotWidget(title="RAM Usage (%)")
        self.ram_plot.setYRange(0, 100)
        self.ram_curve = self.ram_plot.plot(pen=pg.mkPen('b', width=2))

        # Tạo đồ thị Disk
        self.disk_plot = pg.PlotWidget(title="Disk Usage (%)")
        self.disk_plot.setYRange(0, 100)
        self.disk_curve = self.disk_plot.plot(pen=pg.mkPen('g', width=2))

        # Tạo đồ thị Network
        self.network_plot = pg.PlotWidget(title="Network Usage (MB/s)")
        self.network_plot.setYRange(0, 10)
        self.network_curve = self.network_plot.plot(pen=pg.mkPen('m', width=2))

        # Thêm các đồ thị vào giao diện
        layout.addWidget(self.cpu_plot)
        layout.addWidget(self.ram_plot)
        layout.addWidget(self.disk_plot)
        layout.addWidget(self.network_plot)

        self.setLayout(layout)

        # Dữ liệu ban đầu
        self.cpu_data = [0] * 100
        self.ram_data = [0] * 100
        self.disk_data = [0] * 100
        self.network_data = [0] * 100

        # Thiết lập timer để cập nhật dữ liệu theo thời gian thực
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Cập nhật mỗi giây

    def update_data(self):
        # Lấy thông tin CPU, RAM, Disk, và Network
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent

        # Network
        net_io = psutil.net_io_counters()
        network_usage = (net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024  # MB/s

        # Cập nhật dữ liệu
        self.cpu_data = self.cpu_data[1:] + [cpu_percent]
        self.ram_data = self.ram_data[1:] + [ram_percent]
        self.disk_data = self.disk_data[1:] + [disk_percent]
        self.network_data = self.network_data[1:] + [network_usage]

        # Cập nhật đồ thị
        self.cpu_curve.setData(self.cpu_data)
        self.ram_curve.setData(self.ram_data)
        self.disk_curve.setData(self.disk_data)
        self.network_curve.setData(self.network_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec())

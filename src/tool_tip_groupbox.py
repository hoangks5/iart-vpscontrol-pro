class DescriptionGroupBox:
    def __init__(self, ui):
        """Initialize the DescriptionGroupBox with a UI reference."""
        super().__init__()
        self.ui = ui
        self.set_tooltips()

    def set_tooltips(self):
        """Set tooltips for various UI elements in the application with HTML formatting."""
        # General Section
        self.ui.chrome_8.setToolTip("Thêm thời gian chờ random , ví dụ <b>10 +- 2</b> khoảng thời gian chờ từ 8 đến 12 giây")
        self.ui.chrome_7.setToolTip("Mở một <b>URL</b> trong trong trình duyệt mặc định")
        # Browser Section
        self.ui.chrome_6.setToolTip("Khởi tạo <b>Chrome</b> mới")
        self.ui.click_13.setToolTip("Khởi tạo <b>Chrome Profile</b> mới, nếu chưa có sẽ tạo mới với đường dẫn <i>Profile Xpath</i>")
        self.ui.click_25.setToolTip("Resize <b>Chrome</b> với kích thước <b>width</b>, <b>height</b>, click <b>Full</b> để lấy kích thước toàn màn hình")
        self.ui.click_27.setToolTip("Truy cập tới <b>URL</b>")
        self.ui.click_26.setToolTip("Phóng to hoặc thu nhỏ Page , giá trị mặc định là <b>100</b> tương đương giá trị măc định của trình duyệt")
        # Keyboard Section
        self.ui.click_15.setToolTip("Gõ một đoạn văn bản như một <b>người dùng</b>")
        self.ui.click_16.setToolTip(
            "Thực hiện một phím bấm<br>"
            "Nhập phím vào ô text hoặc bấm nút <b>Get</b> để chọn phím"
        )
        self.ui.click_19.setToolTip(
            "Thực hiện chuỗi phím bấm<br>"
            "Nhập chuỗi phím vào ô text, mỗi phím cách nhau bởi dấu cách<br>"
            "Bấm nút <b>Get</b> để chọn chuỗi phím cần bấm"
        )

        # Mouse Section
        self.ui.click_17.setToolTip(
            "Di chuyển chuột đến một tọa độ (x, y)<br>"
            "Nhập tọa độ <b>x</b>, <b>y</b> hoặc bấm <b>Get</b> để chọn điểm di chuyển và click để lấy tọa độ"
        )
        self.ui.click_20.setToolTip(
            "Di chuyển chuột đến một điểm ngẫu nhiên trong vùng<br>"
            "Nhập tọa độ <b>x</b>, <b>y</b>, <b>width</b>, <b>height</b> hoặc bấm <b>Get</b> để chọn vùng di chuyển"
        )
        self.ui.sleep_14.setToolTip(
            "Click chuột <b>trái</b> hoặc <b>phải</b><br>"
            "H.Left hoặc H.Right để giữ và click chuột <b>trái</b> hoặc <b>phải</b>"
        )
        self.ui.click_18.setToolTip("Scroll chuột lên hoặc xuống")

        # AI Section
        self.ui.click_24.setToolTip(
            "Nhận diện hình ảnh và di chuyển chuột đến vị trí hình ảnh<br>"
            "Bấm <b>Crop</b> để cắt hình ảnh<br>"
            "Bấm <b>Paste</b> để dán mã base64 của hình ảnh vào ô text"
        )

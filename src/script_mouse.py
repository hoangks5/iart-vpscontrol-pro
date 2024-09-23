from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Chuột được nhấn tại vị trí: ({x}, {y})")
        # Sau khi lấy tọa độ, bạn có thể ngừng lắng nghe
        return False

def get_mouse_position():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
get_mouse_position()
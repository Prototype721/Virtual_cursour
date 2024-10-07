import ctypes
import logging


logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def move_mouse(x, y):
    try:
        ctypes.windll.user32.SetCursorPos(x, y)
        return True
    except Exception as e:
        logging.exception("Failed to move mouse")
        return False

def click_mouse():
    try:
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        return True
    except Exception as e:
        logging.exception("Failed to click mouse")
        return False
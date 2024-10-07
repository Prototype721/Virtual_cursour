import ctypes


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def move_mouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)



def click_mouse():
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


move_mouse(100, 200)

click_mouse()
import win32gui
import ppadb
from ppadb.client import Client as AdbClient
import time

class Android_device:
    def __init__(self, device: ppadb.device.Device) -> None:
        pass
        self.device = device
        self.snum = device.get_serial_no()

        if self.snum == 'ce10171ab2312a0d04':
            self.window_text = 'SM-G950N'  # G8
        elif self.snum == 'ce071717d4035622047e':
            self.window_text = 'SM-N950N'  # Note8

        self.set_hwnd(self.window_text)
        print(f"Deviced {self.window_text} is connedted\nHwnd: {self.hwnd} ")

    def find_hwnd_by_text(self, hwnd, window_text: str):
        if win32gui.IsWindowVisible(hwnd) and (window_text == win32gui.GetWindowText(hwnd)):
            # print(f"Found hwnd: {hwnd}")
            self.hwnd = hwnd


    def set_hwnd(self, window_text: str):
        win32gui.EnumWindows(self.find_hwnd_by_text, window_text)

    # 안드로이드 공통 함수
    # 홈버튼 누르기
    def press_home(self):
        cmd = 'input keyevent KEYCODE_HOME'
        self.device.shell(cmd)
        time.sleep(0.8)

    # 뒤로가기 누르기
    def press_back(self):
        cmd = 'input keyevent KEYCODE_BACK'
        print(cmd)
        self.device.shell(cmd)
        time.sleep(0.8)

    def tap_xy(self, x: int, y: int):
        cmd = f'input touchscreen tap {x} {y}'
        print(cmd)
        self.device.shell(cmd)
        time.sleep(0.8)

    def swipe_xy_xy(self, xSrc, ySrc, xDes, yDes, duration=200):
        cmd = f'input swipe {xSrc} {ySrc} {xDes} {yDes} {duration}'
        print(cmd)
        self.device.shell(cmd)
        time.sleep(0.8)

    def swipe_down(self, rep=1, dy=1500, duration=200):
        xSrc = 1000
        ySrc = 1900
        yDes = ySrc - dy
        for i in range(rep):
            self.swipe_xy_xy(xSrc, ySrc, xSrc, yDes)

    def swipe_up(self, rep=1, dy=1500, duration=200):
        xSrc = 1000
        ySrc = 200
        yDes = ySrc + dy
        for i in range(rep):
            self.swipe_xy_xy(xSrc, ySrc, xSrc, yDes)

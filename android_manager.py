import win32gui
import win32api
import win32con
import ppadb
from ppadb.client import Client as AdbClient
import pyautogui
import time
import os
from pathlib import Path

def tuple_plus(a:tuple, b:tuple):
    result = tuple([a[i]+b[i] for i in range(len(a))])
    return result
def tuple_minus(a:tuple, b:tuple):
    result = tuple([a[i]-b[i] for i in range(len(a))])
    return result
class Android_device:
    def __init__(self, device: ppadb.device.Device, order_of_device=1) -> None:
        pass
        self.device = device
        self.snum = device.get_serial_no()
        self.prev_sleeping_time = 0.5
        self.sleeping_time = 0.5
        self.width = 492
        self.height = 1020
        self.confidence = 0.9
        self.waiting_time = 3
        self.status = 'initial'
        self.order_of_device = order_of_device

        if self.snum == 'ce10171ab2312a0d04':
            self.window_text = 'SM-G950N'  # G8
            self.set_hwnd(self.window_text)
            self.resize(self.order_of_device)

        elif self.snum == 'ce071717d4035622047e':
            self.window_text = 'SM-N950N'  # Note8
            self.set_hwnd(self.window_text)
            self.resize(self.order_of_device)
            # if pyautogui.size()[0] > 1920:
            #     self.move_window_by_xyxy(2886+492, 1002)
            # else:
            #     self.move_window_by_xyxy(960+476, 20)
        print(f"Deviced {self.window_text} is connedted\nHwnd: {self.hwnd}")

    def find_hwnd_by_text(self, hwnd, window_text: str):
        if win32gui.IsWindowVisible(hwnd) and (window_text == win32gui.GetWindowText(hwnd)):
            # print(f"Found hwnd: {hwnd}")
            self.hwnd = hwnd
    def set_hwnd(self, window_text: str):
        win32gui.EnumWindows(self.find_hwnd_by_text, window_text)
    # 안드로이드 공통 함수
    def locate_center(self, img:str):
        """
        윈도우상에서 특정 그림을 찾는 함수
        :param img:그림파일명(확장자제외)
        :return: (x,y) location on window
        """
        xy = pyautogui.locateCenterOnScreen(self.get_image_path(img), region=self.get_region(), confidence=self.confidence)
        # print(img, xy)
        return xy
    def resize(self, order_of_device:int):
        title_bar_height = win32api.GetSystemMetrics(win32con.SM_CYCAPTION)
        border_width = win32api.GetSystemMetrics(win32con.SM_CXSIZEFRAME)
        border_height = win32api.GetSystemMetrics(win32con.SM_CYSIZEFRAME)
        # 윈도우 상의 frame_size 정확히 계산해야 함. caption에서 border가 붙는지 어떤지.
        # self.frame_size = (border_width * 2, border_height + title_bar_height)
        self.frame_size = (border_width * 2, title_bar_height)
        #실제 디바이스 표현 픽셀
        self.device_size = tuple(self.shell('wm size').split()[-1].split('x'))
        self.size_coef = 3
        #body_size = 윈도우 화면상의 사이즈
        self.body_size = tuple([int(float(s)/self.size_coef) for s in self.device_size])
        # self.window_size = tuple([self.frame_size[i] + self.body_size[i] for i in range(2)])
        self.window_size = tuple_plus(self.frame_size, self.body_size)
        #모니터 화면 크기 구하기
        self.monitor_xy = (win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
        # 디바이스 하나일 경우, 시작점 xy = 화면 사이즈 - 윈도우 사이즈 - (0, 윈도우 작업표시줄 높이)
        # 디바이스 두개일 경우, 시작점 xy = 화면 사이즈 - 윈도우 사이즈 - (윈도우 x 사이즈, 윈도우 작업표시줄 높이)
        self.window_xy0 = tuple_plus(tuple_minus(tuple_minus(self.monitor_xy, self.window_size), (self.window_size[0] * (order_of_device-1), 40)), ((self.order_of_device-1)*2*border_width, 0))
        print(self.window_xy0)
        # body_xy_0(기준점): window xy(좌측위) + (border w, border h + titlebar h)
        self.body_xy0 = tuple_plus(self.window_xy0, (border_width, border_height + title_bar_height))
        # self.body_xy0 = self.window_xy0 + (border_width, border_height + title_bar_height)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, self.window_xy0[0], self.window_xy0[1], self.window_size[0], self.window_size[1], win32con.WM_SHOWWINDOW)
        # win32gui.MoveWindow(self.hwnd, self.window_xy0[0], self.window_xy0[1], self.window_size[0], self.window_size[1], True)
    def get_region(self):
        """
        윈도우의 (left, top, width, height) 리턴
        pyautogui에 region을 넘겨주기 위한 함수
        :return: (left, top, width, height)
        """
        (left, top, right, bottom) = win32gui.GetWindowRect(self.hwnd)
        width = right - left
        height = bottom - top
        region = (left, top, width, height)
        return region

    # def move_window(self):
    #     #해상도 체크. 필요시 사이즈를 절반으로.
    #     (w, h) = pyautogui.size()
    #     if w == 3840: #UHD. size 반으로 줄여서 이동시키기(집 컴터)
    #         if self.window_text == 'SM-G950N':
    #             #placement: (-2165, 825, -1673, 1845)
    #             win32gui.MoveWindow(self.hwnd, -2165, 825+240, -1673+2165, 1845-825, True)
    #         elif self.window_text == 'SM-N950N':
    #             #placement: (-1697, 828, -1205, 1848)
    #             win32gui.MoveWindow(self.hwnd, -1697, 828+240, -1673+2165, 1845-825, True)
    #     elif w == 1920: #FHD. 위치만 옮기는 것으로.. 나중에 작성.
    #         pass
    def move_window_by_xyxy(self, *args):
        xyxy = args
        if len(xyxy) > 2:
            width = xyxy[2]-xyxy[0]
            height = xyxy[3]-xyxy[1]
        else:
            width = self.window_size[0]
            height = self.window_size[1]
        win32gui.MoveWindow(self.hwnd, xyxy[0], xyxy[1], width, height, True)

    #문자열을 입력 받아서 연관 이미지 탭
    def get_image_path(self, img:str)->str:
        return str(os.path.dirname(os.path.abspath(__file__))) + '/images/' + img.lower() + '.png'
    def tap_image(self, img:str):
        return self.tap_image_by_path(self.get_image_path(img))
    def tap_image_or_wait(self, img:str, sec=0):
        if sec == 0:
            sec = self.waiting_time
        for iter_num in range(sec):
            if self.tap_image(img):
                return True
            else:
                time.sleep(1)
        return False
    def tap_image_by_path(self, img_path:str):
        xy = pyautogui.locateCenterOnScreen(img_path, region=self.get_region(), confidence=self.confidence)
        if xy != None:
            pyautogui.click(xy)
        else:
            return False
        return True

    # 홈버튼 누르기
    def press_home(self):
        cmd = 'input keyevent KEYCODE_HOME'
        self.device.shell(cmd)
        time.sleep(self.sleeping_time)

    # 뒤로가기 누르기
    def press_back(self):
        cmd = 'input keyevent KEYCODE_BACK'
        # print(cmd)
        self.device.shell(cmd)
        time.sleep(self.sleeping_time)

    def tap_xy(self, x: int, y: int):
        cmd = f'input touchscreen tap {x} {y}'
        # print(cmd)
        self.device.shell(cmd)
        time.sleep(self.sleeping_time)
        # print(f"{self.window_text}'s sleeping time: {self.sleeping_time}")
    def click_xy(self, xy:tuple, is_device_xy:bool=False):
        """
        window화면상의 좌표를 받아서 device상의 tap으로 연결시켜 주는 함수.
        :param xy: 윈도우 화면상의 클릭할 곳의 좌표. Tuple로 준다.
        """
        #디바이스 기준 좌표인지 확인.
        if is_device_xy == True:
            self.tap_xy(xy[0], xy[1])
        else:
            #디바이스 기준 좌표로 변경
            # (x, y, _, _) = self.get_region()
            # self.tap_xy(xy[0]-x, xy[1]-y)
            pyautogui.moveTo(xy[0], xy[1])
            pyautogui.click(xy[0], xy[1])
    def swipe_xy_xy(self, xSrc, ySrc, xDes, yDes, duration=200):
        cmd = f'input swipe {xSrc} {ySrc} {xDes} {yDes} {duration}'
        # print(cmd)
        self.device.shell(cmd)
        time.sleep(self.sleeping_time)

    def swipe_down(self, rep=1, dy=1500, duration=200):
        xSrc = 1000
        ySrc = 1900
        yDes = ySrc - dy
        for i in range(rep):
            self.swipe_xy_xy(xSrc, ySrc, xSrc, yDes, duration=duration)

    def swipe_up(self, rep=1, dy=1500, duration=200):
        xSrc = 1000
        ySrc = 200
        yDes = ySrc + dy
        for i in range(rep):
            self.swipe_xy_xy(xSrc, ySrc, xSrc, yDes, duration=duration)
    def shell(self, cmd:str):
        return self.device.shell(cmd)
    def set_sleeping_time(self, sleeping_time):
        self.sleeping_time = sleeping_time
    def automation_by_image(self, search_img, device_xy:tuple=None, iter_num=1, target_img=None, cur_status=None, new_status=None, no_click=False):
        """
        이미지를 통해서 자동화실행하는 함수. 화면에 원하는 이미지가 있는지를 확인 후, 이미지가 있으면
        1. 해당 이미지를 클릭, 2. 다른 이미지를 클릭, 3. 좌표를 클릭. 4. 새로운 status 설정.
        단, 현재 status가 만족할 경우에만.
        :param search_img: 찾을 이미지
        :param iter_num: 반복횟수
        :param target_img: 클릭할 이미지. 없으면 찾은 이미지를 클릭
        :param device_xy: 클릭할 좌표(디바이스 기준 좌표)
        :param cur_status: 자동화를 수행하기 위한 현재 상태. 기본족으로 만족해야 함.
        :param new_status: 이미지를 찾았을 경우, 새로 수정할 상태.
        :param no_click: 클릭하지 않고, 상태만 바꾸고자 할 경우 True로 설정. Target_img가 설정된 경우, Target_img도 찾아야지 성공함.
        :return: True for 찾아서 성공했으면. False 실패시.
        """
        # 상태가 만족할 경우에만 검색 수행
        if (cur_status == None) or (cur_status == self.status):
            click_xy = None
            is_tap_xy = False
            for n in range(iter_num):
                # 찾는 이미지가 있는지 검색
                search_xy = self.locate_center(search_img)
                if search_xy is not None:
                    # 이미지를 찾은 경우
                    print(f"Found {search_img} at {search_xy}")
                    if (target_img is None) and (device_xy is None):
                        #찾은 이미지를 클릭
                        click_xy = search_xy
                        break
                    elif target_img is None and device_xy is not None:
                        click_xy = device_xy
                        is_tap_xy = True
                        break
                    elif target_img is not None and device_xy is None:
                        click_xy = self.locate_center(target_img)
                        break
                    else:
                        #taret_img와 좌표 모두 존재하는 경우
                        click_xy = self.locate_center(target_img)
                        if click_xy is None:
                            #target이미지를 찾지 못한 경우
                            click_xy = device_xy
                            is_tap_xy = True
                time.sleep(self.sleeping_time)
            if click_xy is not None:
                if no_click == False:
                    #성공한 경우 클릭을 한 후, 새로운 상태를 설정해 준다.
                    print(f"Img: {search_img}, T_img: {target_img}\n"
                          f"Click: {click_xy}(is_tap_xy: {is_tap_xy})")
                    self.click_xy(click_xy, is_device_xy=is_tap_xy)
                if new_status is not None:
                    print(f'prev status: {self.status}, new status:{new_status}')
                    self.status = new_status
                return True
        return False
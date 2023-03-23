import win32gui
import ppadb
from ppadb.client import Client as AdbClient
import time
from android_manager import Android_device

class Poke_device(Android_device):
    def __init__(self, device: ppadb.device.Device) -> None:
        super().__init__(device)
        self.default_sleeping_time = 0.7
        self.sleeping_time = self.default_sleeping_time

    # 포케몬 기초 함수
    def click_bottom_center(self):
        # 아래중앙 클릭
        self.tap_xy(545, 1900)

    def click_config(self):
        # 설정 클릭
        self.tap_xy(1000, 200)

    def click_store(self):
        # 상점클릭
        self.tap_xy(534, 1447)

    def click_profile(self):
        # 프로필 클릭
        self.tap_xy(120, 1910)

    def click_friend(self):
        # 프렌드 클릭
        self.tap_xy(736, 127)

    def sort_reset(self):
        # 이름순으로 리셋
        # 소팅 클릭
        self.tap_xy(918, 1934)
        # 이름순 클릭
        self.tap_xy(945, 966)

    def sort_get_present(self):
        # 소팅리셋
        self.sort_reset()
        # 소팅 클릭
        self.tap_xy(918, 1934)
        # 선물받기순 클릭
        self.tap_xy(928, 1536)

    def sort_send_present(self):
        # 소팅리셋
        self.sort_reset()
        # 소팅 클릭
        self.tap_xy(918, 1934)
        # 선물보내기순 클릭
        self.tap_xy(940, 1738)

    def first_profile_click(self):
        self.tap_xy(378, 839)

    # 포케몬 전용 함수
    def log_out(self):
        self.click_bottom_center()
        self.click_config()
        self.swipe_down()
        # 로그아웃 클릭
        self.tap_xy(453, 1563)
        # yes 클릭
        self.tap_xy(557, 1032)

    def log_in(self, id, password):
        # 다시로그인 클릭
        self.tap_xy(561, 1230)
        # 구글로그인
        self.tap_xy(478, 1071)
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()
        # self.tap_xy()

    # 상점 안에서 100 금화 구매
    def buy_100(self, iter_num: int = 5):
        """100골드를 사는 함수
        iter_num = 5 / 반복횟수
        """
        # 중앙볼/취소 클릭
        self.tap_xy(545, 1900)
        # 상점클릭
        self.tap_xy(534, 1447)
        time.sleep(0.8)
        # 상점 맨 아래로 내려가기
        for n in range(4):
            self.swipe_down()
            time.sleep(0.8)

        # 반복구매하기
        for n in range(iter_num):
            self.tap_xy(180, 300)
            time.sleep(4)
            self.tap_xy(550, 2000)
            time.sleep(13)
            print(f'100골 {n + 1}개 구매함. 남은 선물: {iter_num - n}')
        self.click_bottom_center()

    # 선물 열기
    def open_present(self, iter_num: int = 1):
        # 프로필 클릭
        self.click_profile()
        # 프렌드 클릭
        self.click_friend()

        for n in range(iter_num):
            # 선물받기 소팅
            self.sort_get_present()
            # 위에서 첫번째 받을 선물 클릭
            self.first_profile_click()
            # 선물클릭 클릭
            self.tap_xy(554, 1493)
            # 연다 클릭
            self.tap_xy(540, 1693)
            # 취소 3 연타
            time.sleep(15)
            self.click_bottom_center()
        self.click_bottom_center()

    # 선물 보내기
    def send_present(self, iter_num: int = 1):
        # 프로필 클릭
        self.click_profile()
        # 프렌드 클릭
        self.click_friend()

        for n in range(iter_num):
            # 선물보내기 소팅
            self.sort_send_present()
            # 위에서 첫번째 보낼 프로필 클릭
            self.first_profile_click()
            # 선물보내기 클릭
            self.tap_xy(199, 1630)
            # 첫번째 엽서 클릭
            self.tap_xy(588, 687)
            # 보내기 클릭
            self.tap_xy(546, 1740)
            time.sleep(2)
            self.click_bottom_center()
        self.click_bottom_center()

    #포케몬 교환하기
    def exchange(self, device: ppadb.device.Device, iter_num=1):
        """다른 하나의 Device를 받아와서 교환을 진행한다.
        교환창이 열려져 있는 상태에서 시작
        :param device: 교환을 진행할 다른 디바이스 클래스
        :return: None
        """
        # 대기시간 0으로 설정
        self.sleeping_time = 0
        # 한글 입력을 위한 키보드 설정
        dev_s8.device.shell("ime set com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME")

        for i in range(iter_num):
            # 첫번째 몬스터 클릭
            self.tap_xy(198, 734)
            device.tap_xy(198, 734)
            time.sleep(1)
            # NEXT
            self.tap_xy(540, 1700)
            device.tap_xy(540, 1700)
            time.sleep(5)
            # Confirm
            self.tap_xy(99, 1068)
            device.tap_xy(99, 1068)
            time.sleep(20)
            # 교환완료 후 다시 교환준비
            self.click_bottom_center()
            device.click_bottom_center()
            time.sleep(5)
            # 교환클릭
            self.tap_xy(904, 1604)
            device.tap_xy(904, 1604)
            time.sleep(5)
            print(f'{i+1}회 교환완료')
        #대기시간 원래대로
        self.sleeping_time = self.default_sleeping_time
        #본래 키보드로 변경
        # dev_s8.device.shell("ime set com.sec.android.inputmethod.beta/com.sec.android.inputmethod.SamsungKeypad")
# * QTabWidget 탭에 다양한 위젯 추가
import numpy as np
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import QIcon, QFont       #아이콘
from PyQt5.QtCore import Qt, QThread

import sys

sys.path.append('C:/my_games/my_server/data_server/mymodule')
import os
import time
from datetime import datetime
from datetime import datetime
from datetime import date, timedelta
import random
import os.path
import re
import git

import cv2
# print(cv2.__version__)
# import matplotlib.pyplot as plt
from PIL import Image

import numpy
# 패키지 다운 필요
import pytesseract
# from pytesseract import image_to_string #
import pyautogui
import pydirectinput
import clipboard
# import keyboard
# 패키지 다운 불필요
import tkinter
import webbrowser
import colorthief

# 나의 모듈
import requests
from ftplib import FTP
import os
import pandas as pd



sys.setrecursionlimit(10 ** 7)
# pyqt5 관련###################################################
#global
clicked_game = "none"
clicked_user = "none"
ftp_username = 'gamer'
ftp_password = 'coobccocco'
data_list = []  # data_list 변수를 전역 변수로 초기화



# 기존 오토모드 관련##############################################


pyautogui.FAILSAFE = False
####################################################################################################################
# pytesseract.pytesseract.tesseract_cmd = R'E:\workspace\pythonProject\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = R'C:\Program Files\Tesseract-OCR\tesseract'


####################################################################################################################
####################################################################################################################
####################################################################################################################
#######pyqt5 관련####################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################


class MyApp(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint)

        self.initUI()

    def initUI(self):
        tabs = QTabWidget()
        tabs.addTab(server_Tab(), '재화 엑셀로 다운 받기')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        start_ready = game_Playing_Ready(self)
        start_ready.start()

        self.my_title()

        # 풀버젼
        # pyinstaller --hidden-import PyQt5 --hidden-import pyserial --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\my_server\\data_server;./data_server" --name property -i="property.ico" --add-data="property.ico;./" --icon="property.ico" --paths "C:\Users\1_S_3\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2" main.py
        # 업데이트버젼
        # pyinstaller --hidden-import PyQt5 --hidden-import pyserial --hidden-import requests --hidden-import chardet --add-data="C:\\my_games\\moonlight\\data_moon;./data_moon" --name moonlight -i="moonlight_macro.ico" --add-data="moonlight_macro.ico;./" --icon="moonlight_macro.ico" --paths "C:\Users\1_S_3\AppData\Local\Programs\Python\Python311\Lib\site-packages\cv2" main.py

        # self.setGeometry(1000 + 960 + 960, 300, 900, 600)
        self.setGeometry(20 + 960, 200, 300, 300)
        self.show()
    def my_title(self):
        self.setWindowTitle("서버 및 재화정리")

class server_Tab(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.set_rand_int()

    def initUI(self):
        print("hi server_Tab")

        # 캐릭터 아이디
        self.propery_group = QGroupBox('검색 후 엑셀 다운 받기')

        game_select = QComboBox()
        list_game = ['게임 종류', '나이트크로우', '롬', '아레스', '제노니아', '아스달', '레이븐2', '로드나인']
        game_select.addItems(list_game)

        user_select = QComboBox()
        list_user = ['유저 보기', '쿱', '꼬꼬']
        user_select.addItems(list_user)

        excel_down = QPushButton('엑셀 다운')
        excel_down.clicked.connect(self.excel_download_folder)

        # 레이아웃

        # 박스 레이아웃
        select_box = QVBoxLayout()
        select_box.addWidget(game_select)
        select_box.addWidget(user_select)
        self.propery_group.setLayout(select_box)

        propery_group_v_layout = QVBoxLayout()
        propery_group_v_layout.addWidget(self.propery_group)


        # 위아래
        h_box1 = QHBoxLayout()
        h_box1.addLayout(propery_group_v_layout)

        confirm_btn = QHBoxLayout()
        confirm_btn.addWidget(excel_down)

        vbox = QVBoxLayout()
        vbox.addLayout(h_box1)
        vbox.addLayout(confirm_btn)

        self.setLayout(vbox)

        # 박스 클릭 선택시 글로벌 변환하기
        game_select.activated[str].connect(self.onActivated_game_select)  # 요건 함수
        user_select.activated[str].connect(self.onActivated_user_select)  # 요건 함수
        # sub_h.activated[str].connect(self.onActivated_slelect_spot)  # 요건 함수

#######################################


    def onActivated_game_select(self, text):
        global clicked_game
        if text != "none" and text != '게임 선택':
            clicked_game = text
            print('clicked_game', clicked_game)
        else:
            print("게임을 선택해 주세요.")

    def onActivated_user_select(self, text):
        global clicked_user
        if text != "none" and text != '유저 선택':
            clicked_user = text
            print('clicked_user', clicked_user)
        else:
            print("유저를 선택해 주세요.")

    def ftp_ip_get(self):
        try:
            url = "https://raw.githubusercontent.com/rntkdgnl932/server/master/server_ip.txt"

            response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            # response = requests.get(url, headers={'Cache-Control': 'no-cache'})
            data = response.text

            print("ftp_ip_get", data)
            return data
        except Exception as e:
            print(e)
            return 0

    # 함수를 정의하여 파일을 다운로드하고 처리
    def download_and_process_file(self, ftp, remote_file, data_list):
        file_name, _ = os.path.splitext(remote_file)
        content = ''

        def handle_binary(data):
            nonlocal content
            content += data.decode('utf-8')

        ftp.retrbinary('RETR ' + remote_file, callback=handle_binary)
        data_list.append(f'{content}:{file_name}')

    def excel_download_folder(self):
        remote_directories = [
            '/rom/coob',
            '/rom/ccocco',
            '/nightcrow/coob',
            '/nightcrow/ccocco',
            '/ares/coob',
            '/ares/ccocco',
            '/zenonia/coob',
            '/zenonia/ccocco',
            '/arthdal/coob',
            '/raven2/coob',
            '/lordnine/coob',
            '/lordnine/ccocco'
        ]
        # FTP 연결
        try:
            ftp_server = self.ftp_ip_get()
            data_list = []

            with FTP(ftp_server) as ftp:
                ftp.login(ftp_username, ftp_password)

                for remote_directory in remote_directories:
                    try:
                        # 원격 디렉토리로 이동
                        ftp.cwd(remote_directory)

                        # 원격 디렉토리 내 파일 목록 얻기
                        file_list = ftp.nlst()

                        # 각 파일을 다운로드하고 데이터 처리
                        for remote_file in file_list:
                            if self.download_and_process_file(ftp, remote_file, data_list) is not None:
                                self.download_and_process_file(ftp, remote_file, data_list)

                    except Exception as e:
                        print(f'폴더 무시: {remote_directory}, 오류 발생: {e}')

                # 결과 출력
                new_list = [s.replace('\ufeff', '') for s in data_list]
                print("last result", new_list)

                # 엑셀 저장 날짜 및 시간을 엑셀 파일명으로...
                nowDay_ = datetime.today().strftime("%Y%m%d%H%M%S")
                year = datetime.today().strftime("%Y")
                month = datetime.today().strftime("%m")
                day = datetime.today().strftime("%d")
                hour = datetime.today().strftime("%H")
                minute = datetime.today().strftime("%M")
                last = str(day) + "d_" + str(hour) + "h" + str(minute) + "m"
                nowDay = str(nowDay_)

                # data_list의 데이터를 데이터프레임으로 변환
                data = [row.split(":") for row in new_list]
                df = pd.DataFrame(data, columns=["사용자", "게임", "서버", "다이아", "골드", "컴퓨터번호"])

                dir_path = "C:/my_games/property/" + str(year) + "/" + str(month) + "/"
                if not os.path.isdir(dir_path):
                    os.makedirs(dir_path)

                # 데이터프레임을 엑셀 파일로 저장
                excel_file_name = dir_path + last + ".xlsx"
                df.to_excel(excel_file_name, index=False)

                btn = pyautogui.alert(button='오냐', text='엑셀 파일로 저장했습니다. 꼬꼬님', title='엑셀로 저장')
                print(btn)

        except Exception as e:
            print(f'파일 다운로드 및 처리 중 오류 발생: {e}')

class game_Playing_Ready(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def run(self):
        try:
            # v_.now_cla = 'none' <= 최초 부를때 자동으로 불러옴. 또는 실행하여 바꿀수 있음. 오딘은 그냥 설정해줘야함.

            # self.m_ = Monitoring_one()
            # self.m_.start()

            self.x_ = game_Playing()
            self.x_.start()
        except Exception as e:
            print(e)
            return 0




# 실제 게임 플레이 부분 #################################################################
################################################
################################################


class game_Playing(QThread):

    def __init__(self):
        super().__init__()
        # self.parent = parent

        self.isCheck = True

    def run(self):

        try:
            print("moonlight go")





        except Exception as e:
            print(e)
            os.system("pause")
            return 0

####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
####################################################################################################################
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)


# if __name__ == '__main__':
#     try:
#         app = QApplication(sys.argv)
#         ex = MyApp()
#
#         # Back up the reference to the exceptionhook
#         sys._excepthook = sys.excepthook
#
#         # Set the exception hook to our wrapping function
#         sys.excepthook = my_exception_hook
#
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(e)
#         print("프로그램 꺼지기전 정지")
#         os.system("pause")

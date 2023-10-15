# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# FTP 서버 정보
ftp_server = '122.36.80.50'
ftp_username = 'gamer'
ftp_password = 'coobccocco'

import requests
from ftplib import FTP
import os
import pandas

data_list = []  # data_list 변수를 전역 변수로 초기화

def print_hi2(name):
    token = "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"
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




    # 로컬 파일 경로 (절대 경로 사용)
    local_file_path = 'C:/my_games/test.txt'

    # 원격 파일 경로 (FTP 서버 내)
    remote_file_path = '/moonlight/test_oner.txt'

    # FTP 연결 및 파일 업로드
    try:
        with FTP(ftp_server) as ftp:
            ftp.login(ftp_username, ftp_password)
            with open(local_file_path, 'rb') as file:
                ftp.storbinary('STOR ' + remote_file_path, file)
            print(f'로컬 파일 {local_file_path}을 FTP 서버의 {remote_file_path}로 업로드했습니다.')
    except Exception as e:
        print(f'파일 업로드 실패: {e}')


# 함수를 정의하여 파일을 다운로드하고 처리
def download_and_process_file(ftp, remote_file):
    file_name, _ = os.path.splitext(remote_file)
    content = ''
    def handle_binary(data):
        nonlocal content
        content += data.decode('utf-8')
    ftp.retrbinary('RETR ' + remote_file, callback=handle_binary)
    data_list.append(f'{file_name}:{content}')



def print_hi(name):
    token = "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"
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.



    # 원격 파일 디렉토리 경로
    remote_directory = '/moonlight'


    # FTP 연결
    try:
        with FTP(ftp_server) as ftp:
            ftp.login(ftp_username, ftp_password)

            # 원격 디렉토리로 이동
            ftp.cwd(remote_directory)

            # 원격 디렉토리 내 파일 목록 얻기
            file_list = ftp.nlst()

            # 각 파일을 다운로드하고 데이터 처리
            for remote_file in file_list:
                download_and_process_file(ftp, remote_file)

            # 결과 출력
            print(data_list)

            # data_list의 데이터를 데이터프레임으로 변환
            data = [row.split(":") for row in data_list]
            df = pandas.DataFrame(data, columns=["텍스트제목", "내용"])

            # 데이터프레임을 엑셀 파일로 저장
            excel_file_name = "C:/my_games/test.xlsx"
            df.to_excel(excel_file_name, index=False)

    except Exception as e:
        print(f'파일 다운로드 및 처리 중 오류 발생: {e}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

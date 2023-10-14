# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    tokken = "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"
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    import requests

    # GitHub API 엔드포인트 및 토큰 설정
    base_url = 'https://api.github.com'
    repo_owner = 'rntkdgnl932'
    repo_name = 'server'
    folder_path = 'path/to/test'  # 폴더 경로
    api_token = 'your_github_api_token'

    # 폴더 내 파일 목록 가져오기
    response = requests.get(f'{base_url}/repos/{repo_owner}/{repo_name}/contents/{folder_path}',
                            headers={'Authorization': f'token {api_token}'})
    folder_contents = response.json()

    # 파일 내용을 담을 배열 초기화
    file_contents = []

    # 각 파일의 내용 가져오기
    for file_info in folder_contents:
        if file_info['type'] == 'file':
            # 파일의 URL을 통해 내용 가져오기
            file_response = requests.get(file_info['download_url'], headers={'Authorization': f'token {api_token}'})
            file_data = file_response.text
            file_contents.append({
                '폴더명': folder_path,
                '텍스트 파일 제목': file_info['name'],
                '텍스트 파일의 내용': file_data
            })

    # 결과 출력
    for file_content in file_contents:
        print(file_content)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

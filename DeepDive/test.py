import os
import requests
from bs4 import BeautifulSoup

file_path = 'C:\\Users\\dlckd\\Desktop\\2024-1학기\\캡스톤디자인\\Phishing_Detection\DeepDive'


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def download_js(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        js_files = [script['src']
                    for script in soup.find_all('script') if 'src' in script.attrs]
        js_contents = []
        for js_file in js_files:
            js_response = requests.get(js_file)
            if js_response.status_code == 200:
                js_contents.append((js_file, js_response.text))
        return js_contents
    else:
        return None


def save_file(content, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


def exec(url):
    html_content = download_html(url)
    if html_content:
        save_file(html_content, os.path.join(file_path, 'index.html'))
        # save_file(html_content, 'index.html')

    js_contents = download_js(url)
    if js_contents:
        # os.makedirs('js_files', exist_ok=True)
        counter = 1  # 파일 이름에 붙일 숫자를 세기 위한 카운터
        for js_content in js_contents:
            filename = f'script{counter}.js'
            save_file(js_content, os.path.join(file_path, filename))
            # save_file(js_content, os.path.join('js_files', filename))
            counter += 1  # 다음 파일을 위해 카운터 증가

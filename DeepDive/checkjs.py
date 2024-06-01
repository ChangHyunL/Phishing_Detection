from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin



def download_js(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            js_files = [urljoin(url, script['src'])
                        for script in soup.find_all('script') if 'src' in script.attrs]
            js_contents = []
            for js_file in js_files:
                try:
                    js_response = requests.get(js_file)
                    if js_response.status_code == 200:
                        js_contents.append((js_file, js_response.text))
                except requests.RequestException as e:
                    print(f"Error downloading {js_file}: {e}")
            return js_contents
    except requests.RequestException as e:
        print(f"Error loading page {url}: {e}")
    return None


def check_drive_by_download(js_content):
    # 드라이브 바이 다운로드와 관련된 의심스러운 코드 패턴 검색
    drive_by_download_patterns = [
        r'download\s*=\s*".*\.exe"',
        r'href\s*=\s*".*\.zip"',
        r'document\.createElement\("iframe"\)\.src\s*=\s*".*malicious-site\.com"',
        r'window\.location\s*=\s*".*malicious-site\.com"',
        r'script\s*src\s*=\s*".*malicious-site\.com"',
        r'eval\s*\(.*document\.getElementById\("malicious"\)\.innerHTML'
    ]

    suspicious_lines = []
    for pattern in drive_by_download_patterns:
        matches = re.findall(pattern, js_content)
        if matches:
            suspicious_lines.extend(matches)

    if suspicious_lines:
        print("드라이브 바이 다운로드와 관련된 의심스러운 코드가 발견되었습니다.")
        for line in suspicious_lines:
            print(f"의심스러운 코드: {line}")
        return 1
    else:
        print("드라이브 바이 다운로드와 관련된 의심스러운 코드가 발견되지 않았습니다.")
        return 0


def analyze_javascript(js_content):
    check_drive_by_download(js_content)

def exec(url):
    js_contents = download_js(url)
    if js_contents:
        for _, js_content in js_contents:
            analyze_javascript(js_content)

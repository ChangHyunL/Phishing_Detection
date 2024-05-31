from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse


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


def is_external_domain(src, url):
    src_domain = urlparse(src).netloc
    base_domain = urlparse(url).netloc
    return src_domain != base_domain

# def check_iframe(js_content):
#     # iframe 사용 여부 확인
#     iframe_pattern = r'document\.createElement\("iframe"\)'
#     if re.search(iframe_pattern, js_content):
#         print("iframe이 사용되었습니다.")
#         return 1
#     else:
#         print("iframe이 사용되지 않았습니다.")
#         return 0


def check_iframe(js_content, url):
    iframe_pattern = r'document\.createElement\("iframe"\)'
    external_iframe_pattern = r'document\.createElement\("iframe"\)\.src\s*=\s*["\'](.*?)["\']'
    hidden_iframe_pattern = r'<iframe.*?(display\s*:\s*none|visibility\s*:\s*hidden|width\s*=\s*["\']?0["\']?|height\s*=\s*["\']?0["\']?).*?>'

    hidden_iframes = []
    external_iframes = []

    if re.search(iframe_pattern, js_content):
        print("iframe이 사용되었습니다.")

        external_matches = re.findall(external_iframe_pattern, js_content)
        hidden_matches = re.findall(
            hidden_iframe_pattern, js_content, re.IGNORECASE)

        for match in external_matches:
            src = match
            if src and is_external_domain(src, url):
                external_iframes.append(src)

        if hidden_matches:
            hidden_iframes.extend(hidden_matches)

        if external_iframes:
            print("외부 도메인으로부터의 iframe이 발견되었습니다.")
            for line in external_iframes:
                print(f"의심스러운 iframe: {line}")
            return 1
        elif hidden_iframes:
            print("숨겨진 iframe이 발견되었습니다.")
            for line in hidden_iframes:
                print(f"의심스러운 iframe: {line}")
            return 1
        else:
            print("의심스러운 iframe이 사용되지 않았습니다.")
            return 0
    else:
        print("iframe이 사용되지 않았습니다.")
        return 0


def check_redirection(js_content):
    # JavaScript 리디렉션 확인
    redirection_patterns = [
        r'window\.location\s*=\s*".*"',
        r'window\.location\.href\s*=\s*".*"',
        r'window\.location\.replace\s*=\s*".*"',
        r'document\.location\s*=\s*".*"'
    ]

    suspicious_lines = []
    for pattern in redirection_patterns:
        matches = re.findall(pattern, js_content)
        if matches:
            suspicious_lines.extend(matches)

    if suspicious_lines:
        print("JavaScript 리디렉션 코드가 발견되었습니다:")
        for line in suspicious_lines:
            print(f"의심스러운 코드: {line}")
        return 1
    else:
        print("JavaScript 리디렉션 코드가 발견되지 않았습니다.")
        return 0


def check_external_scripts(js_content):
    # 외부 스크립트 로드 확인
    external_script_pattern = r'<script\s+src\s*=\s*"https?://[^"]+"'
    if re.search(external_script_pattern, js_content):
        print("외부 스크립트가 로드되었습니다.")
        return 1
    else:
        print("외부 스크립트가 로드되지 않았습니다.")
        return 0


def check_dynamic_forms(js_content):
    dynamic_form_patterns = [
        re.compile(r'document\.createElement\(["\']form["\']'),
        re.compile(r'innerHTML\s*=\s*["\'].*<form'),
        re.compile(r'appendChild\(.*document\.createElement\(["\']form["\']')
    ]
    dynamic_forms = []

    for pattern in dynamic_form_patterns:
        if pattern.search(js_content):
            dynamic_forms.append(pattern.pattern)

    if dynamic_forms:
        print("동적으로 삽입된 폼이 발견되었습니다.")
        return 1
    else:
        print("동적으로 삽입된 폼이 발견되지 않았습니다.")
        return 0


def check_external_data_transfer(js_content):
    external_transfer_patterns = [
        re.compile(r'fetch\(["\']https?://'),
        re.compile(r'XMLHttpRequest\(\).open\(["\']POST', re.IGNORECASE),
        re.compile(r'XMLHttpRequest\(\).open\(["\']GET', re.IGNORECASE)
    ]
    external_transfers = []

    for pattern in external_transfer_patterns:
        if pattern.search(js_content):
            external_transfers.append(pattern.pattern)

    if external_transfers:
        print("사용자 입력을 외부 서버로 전송하는 코드가 발견되었습니다.")
        return 1
    else:
        print("사용자 입력을 외부 서버로 전송하는 코드가 발견되지 않았습니다.")
        return 0


def analyze_javascript(js_content):
    results = []
    analysis_functions = [
        check_drive_by_download,
        lambda content: check_iframe(content, url),
        check_redirection,
        check_external_scripts,
        check_dynamic_forms,
        check_external_data_transfer
    ]
    for func in analysis_functions:
        result = 0
        result += func(js_content)
        if result > 0:
            result = 1
        results.append(result)

    return results


def exec(url):
    js_contents = download_js(url)
    count = 0
    if js_contents:
        for _, js_content in js_contents:
            result = analyze_javascript(js_content)
            count += 1
        print(result)
        return (result)


url = 'https://os.korea.ac.kr/research/'
exec(url)

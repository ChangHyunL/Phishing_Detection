from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse

global_url = None


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
        re.compile(r"window\.location\.href\s*=\s*'([^']+?\.(?:exe|zip))'"),
        re.compile(r"window\.location\s*=\s*'([^']+?\.(?:exe|zip))'"),
        re.compile(r"window\.open\('([^']+?\.(?:exe|zip))'\)")
    ]

    suspicious_lines = []
    for pattern in drive_by_download_patterns:
        if pattern.search(js_content):
            suspicious_lines.extend(pattern.pattern)

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


def check_iframe(js_content, url):
    iframe_pattern = r'document\.createElement\("iframe"\)'
    external_iframe_pattern = r'document\.createElement\("iframe"\)\.src\s*=\s*["\'](.*?)["\']'
    hidden_iframe_pattern = r'\.style\.(display|visibility)\s*=\s*[\'"](none|hidden)[\'"]'

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


def check_dynamic_script_load(js_content):
    # 동적으로 외부 스크립트를 로드하는 패턴 확인
    dynamic_script_pattern = r'document\.createElement\(\s*[\'"]script[\'"]\s*\)'
    if re.search(dynamic_script_pattern, js_content):
        print("동적으로 외부 스크립트를 로드하는 코드가 있습니다.")
        return 1
    else:
        print("동적으로 외부 스크립트를 로드하는 코드가 없습니다.")
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
    results = [0, 0, 0, 0, 0, 0]
    analysis_functions = [
        check_drive_by_download,
        lambda content: check_iframe(content, global_url),
        check_redirection,
        check_dynamic_script_load,
        check_dynamic_forms,
        check_external_data_transfer
    ]
    for i, func in enumerate(analysis_functions):
        results[i] += func(js_content)
    return results


def exec(url):
    global global_url
    global_url = url
    js_contents = download_js(url)
    final_results = [0, 0, 0, 0, 0, 0]

    if js_contents:
        for _, js_content in js_contents:
            results = analyze_javascript(js_content)
            final_results = [1 if x > 0 else 0 for x in [
                sum(x) for x in zip(final_results, results)]]

    print(final_results)
    return final_results

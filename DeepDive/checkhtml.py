from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def is_external_domain(url, base_url):
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(url).netloc
    return base_domain != target_domain and target_domain != ''


def isFavicon(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 파비콘 외부 도메인 확인
    icon_link = soup.find('link', rel='icon')
    if icon_link and is_external_domain(icon_link['href'], url):
        print("파비콘이 외부 도메인으로부터 제공됩니다.")
        return 1
    else:
        print("파비콘이 외부 도메인으로부터 제공되지 않습니다.")
        return 0


def isURL_of_Anchor(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    # 외부 도메인 링크 비율 확인
    anchors = soup.find_all('a', href=True)
    external_links = [a['href']
                      for a in anchors if is_external_domain(a['href'], url)]
    total_links = len(anchors)
    external_link_ratio = len(external_links) / \
        total_links if total_links > 0 else 0

    print(f"전체 링크 수: {total_links}")
    print(f"외부 도메인 링크 수: {len(external_links)}")
    print(f"외부 도메인 링크 비율: {external_link_ratio:.2f}")

    if external_link_ratio > 0.61:
        return 1
    else:
        return 0


def is_iframe(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    iframes = soup.find_all('iframe')

    hidden_iframes = []
    external_iframes = []

    for iframe in iframes:
        src = iframe.get('src')
        style = iframe.get('style')
        width = iframe.get('width')
        height = iframe.get('height')

        # 숨겨진 iframe 검사
        if style and ('display:none' in style or 'visibility:hidden' in style):
            hidden_iframes.append(src)
        if (width and width == '0') or (height and height == '0'):
            hidden_iframes.append(src)

        # 외부 도메인 iframe 검사
        if src and is_external_domain(src, url):
            external_iframes.append(src)

    if hidden_iframes:
        print("숨겨진 iframe이 발견되었습니다:")
        return 1

    if external_iframes:
        print("외부 도메인으로부터의 iframe이 발견되었습니다:")
        return 1

    return 0


def analyze_html(html_content, url):
    results = []  # 결과를 저장할 배열 생성
    results.append(isFavicon(html_content, url))  # 파비콘 결과 추가
    results.append(isURL_of_Anchor(html_content, url))  # 앵커 URL 결과 추가
    results.append(is_iframe(html_content, url))
    return results  # 결과 배열 반환


def exec(url):
    html_content = download_html(url)
    if html_content:
        result = analyze_html(html_content, url)
        print(result)
        return result


url = 'https://www.naver.com'
exec(url)

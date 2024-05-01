import re
import Levenshtein
from urllib.parse import urlparse
import requests
import ssl
import socket
from datetime import datetime
import whois
from bs4 import BeautifulSoup

# trusted_cas = ["GeoTrust", "GoDaddy", "Network Solutions",
#                "Thawte", "Comode", "Doster", "VeriSign",
#                "Let's Encrypt", "DigiCert", "GlobalSign",
#                "Symantec", "RapidSSL", "Entrust", "Comodo CA",
#                "Google Trust Services LLC", "Sectigo"]

well_known_hostname = "www.google.com"
filepath = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/non_phishing.csv"
# url = "https://greekaa....aasaasharifa.github.io/%EC%@A0%95%EA%B7%9C%ED%91-usage-03-basic/"
url = "https://url.kr/y8f759"
# url = "https://url.kr/zdq426"   # 가짜 단축 url


def is_redirection(url):    # 만약 url이 redirection한다면 redirection하는 url을 반환해서 그 url을 분석
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except:
        return print(f"{url}은 url이 아닙니다.")


def long_url(url):
    print('long_url')
    if len(url) > 75:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def having_ip(url):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    pattern += r'|((?:0x[0-9a-fA-F]{1,2}\.){3}0x[0-9a-fA-F]{1,2})'
    pattern += r'|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}'

    print('having_ip')
    if re.match(pattern, url):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def having_at(url):
    print('having_at')
    if re.search('@', url):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def having_dash(url):
    print('having_dash')
    if re.search('-', urlparse(url).netloc):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def having_underbar(url):
    print('having_underbar')
    if re.search('_', urlparse(url).netloc):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def having_redirection(url):
    print('having_redirection')
    start = url.find("://") + 3
    url_check = url[start:]
    if re.search('//', url_check):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def sub_domains(url):
    print('sub_domains')
    if url.count(".") > 5:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def long_hostname(url):
    print('long_hostname')
    hostname = urlparse(url).netloc
    if len(hostname) > 30:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def similar_url(url, filepath, threshold=2):
    hostname = urlparse(url).netloc

    # 파일에서 well_known_hostname 목록을 읽어온다.
    with open(filepath, 'r') as file:
        well_known_hostnames = [
            urlparse(line).netloc for line in file.read().splitlines()]

    for well_known_hostname in well_known_hostnames:
        distance = Levenshtein.distance(hostname, well_known_hostname)

        # hostname과 well_known_hostname이 일치하지 않는 경우만 거리를 계산
        if hostname != well_known_hostname:
            if distance <= threshold:
                return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
        else:
            return print(f"{url}은 유효한 url 주소입니다. ✅")
    return print(f"{url}은 유효한 url 주소입니다. ✅")


# def similar_url(url, well_known_hostname, threshold=2):
#     hostname = urlparse(url).netloc
#     distance = Levenshtein.distance(hostname, well_known_hostname)
#     if hostname != well_known_hostname:
#         if distance <= threshold:
#             return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
#         else:
#             return print(f"{url}은 유효한 url 주소입니다. ✅")
#     else:
#         return print(f"{url}은 유효한 url 주소입니다. ✅")


def non_standard_port(url):
    print('non_standard_port')
    parsed_url = urlparse(url)
    port = parsed_url.port
    if port is None:
        print("포트 번호가 지정되어 있지 않습니다.")
    elif port == 80:
        print("표준 HTTP 포트 (80)가 사용되었습니다.")
    elif port == 443:
        print("표준 HTTPS 포트 (443)가 사용되었습니다.")
    else:
        print(f"비표준 포트 ({port})가 사용되었습니다.")


# def is_trusted_cert(url):
#     trusted_cas = get_trusted_issuer()
#     print('is_trusted_cert')
#     try:
#         hostname = urlparse(url).netloc
#         context = ssl.create_default_context()
#         conn = context.wrap_socket(socket.socket(
#             socket.AF_INET), server_hostname=hostname)
#         conn.connect((hostname, 443))
#         cert = conn.getpeercert()
#         issuer = dict(x[0] for x in cert['issuer'])
#         issuer_name = issuer.get('organizationName', '')
#         print(f"Issuer: {issuer_name}")
#         for trusted_ca in trusted_cas:
#             if trusted_ca in issuer_name:
#                 return print(f"{url}의 인증기관은 신뢰받는 기관입니다. ✅")
#         return print(f"{url}의 인증기관은 신뢰받지 못하는 기관입니다. ❌")
#     except Exception as e:
#         print(f"Error while checking url {url}: {e}")
#         return False
def is_trusted_cert(url):
    try:
        hostname = urlparse(url).netloc
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(
            socket.AF_INET), server_hostname=hostname)
        conn.connect((hostname, 443))
        cert = conn.getpeercert()
        issuer = dict(x[0] for x in cert['issuer'])
        issuer_name = issuer.get('organizationName', '')
        print(f"Issuer: {issuer_name}")
        with open('IncludedCACertificateReportForMSFT.csv', 'r', encoding='utf-8') as f:
            trusted_issuer = f.read()
        for trusted_ca in trusted_issuer:
            if trusted_ca in issuer_name:
                return 0
        return 1
    except Exception as e:
        print(f"Error while checking url {url}: {e}")
        return 1


def is_https(url):
    print('is_https')
    if urlparse(url).scheme == 'https':
        return print(f"{url}은 유효한 url 주소입니다. ✅")
    else:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")


def get_creation_date(url):
    print('get_creation_date')
    try:
        domain = whois.whois(url)
        creation_date = domain.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        today = datetime.now()
        age = today - creation_date
    except Exception as e:
        print(f"Error: {e}")
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    if age.days < 180:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def get_expiration_date(url):
    print('get_expiration_date')
    try:
        domain = whois.whois(url)
        expiration_date = domain.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        today = datetime.now()
        age = expiration_date - today
        print(age.days)
    except Exception as e:
        print(f"Error: {e}")
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    if age.days < 365:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")

    try:
        # Get the HTML content of the webpage
        response = requests.get(url)
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the favicon link tag
        favicon_tag = soup.find("link", rel="icon")

        # Extract the href attribute value of the favicon tag
        if favicon_tag:
            favicon_url = favicon_tag.get("href")

            # Check if the favicon URL is from an external domain
            parsed_favicon_url = urlparse(favicon_url)
            parsed_url = urlparse(url)
            return parsed_favicon_url.netloc != parsed_url.netloc
        else:
            return False

    except requests.exceptions.RequestException as e:
        print("Error fetching webpage:", e)
        return False


# def get_trusted_issuer():
#     with open('IncludedCACertificateReportForMSFT.csv', 'r', encoding='utf-8') as f:
#         trusted_issuer = f.read()
#     return trusted_issuer


url = is_redirection(url)
if url:
    long_url(url)
    having_ip(url)
    having_at(url)
    having_dash(url)
    having_underbar(url)
    having_redirection(url)
    sub_domains(url)
    long_hostname(url)
    non_standard_port(url)
    is_https(url)
    get_creation_date(url)
    url = 'https://www.google.com'
    is_trusted_cert(url)
    get_expiration_date(url)
    url = 'https://www.kissmeaaaaaaaaaaatrics.com'
    similar_url(url, filepath)

# html 코드 분석이 필요함

# Favicon { 1,-1 }
# Rule: {If Favicon Loaded From External Domain → Phishing, Otherwise → Legitimate}
# 파비콘이 외부 도메인으로부터 오는지를 확인하여 피싱 여붑 판단
# Request_URL { 1,-1 }
# Rule: {If % of Request URL <22% → Legitimate, Else if % of Request URL≥22% and 61% → Suspicious, Otherwise → Phishing}
# 웹 페이지가 로드될 때 발생하는 요청 중에서 외부 도메인의 비율을 기준으로 피싱 여부를 판단
# URL_of_Anchor { -1,0,1 }
# Rule: {If % of URL Of Anchor <31% → Legitimate, Else if% of URL Of Anchor ≥31% And≤67% → Suspicious Otherwise → Phishing}
# 페이지의 앵커(링크) 태그 내에서 외부 도메인을 가리키는 링크의 비율을 기준으로 피싱 여부를 판단
# Links_in_tags { 1,-1,0 }
# Rule: {If % of Links in "", "<Script>" and ""<17% → Legitimate, Else if % of Links in ", "<Script>" and "" ≥17% And≤81% → Suspicious, Otherwise → Phishing}
# 페이지의 태그(예: <script>) 내에서 외부 도메인을 가리키는 링크의 비율을 기준으로 피싱 여부를 판단
# SFH { -1,1,0 }
# Rule: {If SFH is "about: blank" Or Is Empty → Phishing, Else if SFH Refers To A Different Domain → Suspicious, Otherwise → Legitimate}
# SFH는 폼(form) 제출 후에 사용자를 이동시킬 페이지를 가리킴
# SFH가 비어있거나 "about:blank"이면 제출된 데이터가 악의적으로 사용될 수 있으므로 피싱
# Submitting_to_email { -1,1 }
# Rule: {If Using "mail()" or "mailto:" Function to Submit User Information → Phishing, Otherwise → Legitimate}
# Redirect { 0,1 }
# Rule: {If #ofRedirect Page≤1 → Legitimate, Else if #of Redirect Page≥2 And<4 → Suspicious, Otherwise → Phishing}
# 페이지가 너무 많은 리다이렉트를 포함하는 경우 사용자를 다른 곳으로 유도할 수 있으므로 피싱으로 분류
# on_mouseover { 1,-1 }
# Rule: {If onMouseOver Changes Status Bar → Phishing, Else if It Does't Change Status Bar → Legitimate}
# onMouseOver 이벤트가 상태 표시줄을 변경하는 경우 사용자를 속일 수 있으므로 피싱으로 판단
# RightClick { 1,-1 }
# Rule: {If Right Click Disabled → Phishing, Otherwise → Legitimate}
# 우클릭을 비활성화하는 것은 사용자의 편의를 해치는 것이며, 이는 피싱 사이트의 특징일 수 있으므로 피싱으로 분류 -> 복사를 막는 경우가 많은데?
# popUpWidnow { 1,-1 }
# Rule: {If Popoup Window Contains Text Fields→ Phishing, Otherwise → Legitimate}
# 팝업 창이 텍스트 필드를 포함한다면, 사용자로부터 민감한 정보를 요구하는 피싱 시도일 수 있으므로 피싱으로 간주
# Iframe { 1,-1 }
# Rule: {If Using iframe → Phishing, Otherwise → Legitimate}
# 피싱 사이트는 다른 사이트의 컨텐츠를 iframe으로 가져와 사용자를 속임


# api를 발급받아야 하므로 단순 detection보다 더 심화된 내용 -> 추가적인 detectiondl 필요할 때 사용할 예정

# web_traffic { -1,0,1 }
# Rule: {If Website Rank<100,000 → Legitimate, Else if Website Rank>100,000 → Suspicious, Otherwise → Phishing}
# similarweb api 를 사용하여 순위에 없는경우 피싱

# Google_Index { 1,-1 }
# Rule: {If Webpage Indexed by Google → Legitimate, Otherwise → Phishing}
# Links_pointing_to_page { 1,0,-1 }
# Rule: {If # of Link Pointing to The Webpage=0 → Phishing, Else if #Of Link Pointing to The Webpage>0 and≤2 → Suspicious, Otherwise → Legitimate}
# google search console을 이용하여 확인 구글 인덱스에 없는 경우 피싱, 링크 데이터 확인

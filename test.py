import re
import Levenshtein
from urllib.parse import urlparse
import requests

well_known_domain = "www.google.com"
# url = "https://greekaa....aasaasharifa.github.io/%EC%@A0%95%EA%B7%9C%ED%91-usage-03-basic/"
# url = "https://url.kr/y8f759"
url = "https://url.kr/zdq426"   # 가짜 단축 url


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
    url = url[start:]
    if re.search('//', url):
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def sub_domains(url):
    print('sub_domains')
    if url.count(".") > 5:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def long_domain(url):
    print('long_domain')
    domain = urlparse(url).netloc
    if len(domain) > 30:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def similar_url(url, well_known_domain, threshold=2):
    domain = urlparse(url).netloc
    distance = Levenshtein.distance(domain, well_known_domain)
    if distance <= threshold:
        return print(f"{url}은 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}은 유효한 url 주소입니다. ✅")


def non_standard_port(url):
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


url = is_redirection(url)
if url:
    long_url(url)
    having_ip(url)
    having_at(url)
    having_dash(url)
    having_underbar(url)
    having_redirection(url)
    sub_domains(url)
    long_domain(url)
    url = 'https://www.g00gle.com'
    similar_url(url, well_known_domain)
    non_standard_port(url)

# having_IP_Address { -1,1 }

# Rule: {If the Domain Part has an IP Address → Phishing, Otherwise→ Legitimate}
# URL_Length { 1,0,-1 }

# Rule: {If URL length <54 → Legitimate, else if URL length 54 and 75 → Suspicious, Otherwise → Phishing}
# Shortining_Service { 1,-1 }

# Rule: {TinyURL → Phishing, Otherwise → Legitimate}
# having_At_Symbol { 1,-1 }

# Rule: {If Url Having @ Symbol → Phishing, Otherwise → Legitimate}
# double_slash_redirecting { -1,1 }

# Rule: {If the Position of the Last Occurrence of "//" in the URL > 7→ Phishing, Otherwise→ Legitimate}
# Prefix_Suffix { -1,1 }

# Rule: {If Domain Name Part Includes (-) Symbol → Phishing. Otherwise → Legitimate}
# having_Sub_Domain { -1,0,1 }

# Rule: {If Domain Name Part Includes (-) Symbol → Phishing, Otherwise → Legitimate}
# SSLfinal_State { -1,1,0 }

# Rule: {If Use https and Issuer Is Trusted and Age of Certificate 1 Years → Legitimate, Else If Using https and Issuer is not Trusted → Suspicious, Otherwise → Phishing}
# Domain_registeration_length { -1,1 }

# Rule: {If Domains Expires on 1 years → Phishing, Otherwise → Legitimate}
# Favicon { 1,-1 }

# Rule: {If Favicon Loaded From External Domain → Phishing, Otherwise → Legitimate}
# port { 1,-1 }

# Rule: {If Port # is of the Preffered Status → Phishing, Otherwise → Legitimate}
# HTTPS_token { -1,1 }

# Rule: {If Using HTTP Token in Domain Part of The URL → Phishing, Otherwise → Legitimate}
# Request_URL { 1,-1 }

# Rule: {If % of Request URL <22% → Legitimate, Else if % of Request URL≥22% and 61% → Suspicious, Otherwise → Phishing}
# URL_of_Anchor { -1,0,1 }

# Rule: {If % of URL Of Anchor <31% → Legitimate, Else if% of URL Of Anchor ≥31% And≤67% → Suspicious Otherwise → Phishing}
# Links_in_tags { 1,-1,0 }

# Rule: {If % of Links in "", "<Script>" and ""<17% → Legitimate, Else if % of Links in ", "<Script>" and "" ≥17% And≤81% → Suspicious, Otherwise → Phishing}
# SFH { -1,1,0 }

# Rule: {If SFH is "about: blank" Or Is Empty → Phishing, Else if SFH Refers To A Different Domain → Suspicious, Otherwise → Legitimate}
# Submitting_to_email { -1,1 }

# Rule: {If Using "mail()" or "mailto:" Function to Submit User Information → Phishing, Otherwise → Legitimate}
# Abnormal_URL { -1,1 }

# Rule: {If The Host Name Is Not Included In URL → Phishing, Otherwise → Legitimate}
# Redirect { 0,1 }

# Rule: {If #ofRedirect Page≤1 → Legitimate, Else if #of Redirect Page≥2 And<4 → Suspicious, Otherwise → Phishing}
# on_mouseover { 1,-1 }

# Rule: {If onMouseOver Changes Status Bar → Phishing, Else if It Does't Change Status Bar → Legitimate}
# RightClick { 1,-1 }

# Rule: {If Right Click Disabled → Phishing, Otherwise → Legitimate}
# popUpWidnow { 1,-1 }

# Rule: {If Popoup Window Contains Text Fields→ Phishing, Otherwise → Legitimate}
# Iframe { 1,-1 }

# Rule: {If Using iframe → Phishing, Otherwise → Legitimate}
# age_of_domain { -1,1 }

# Rule: {If Age Of Domain≥6 months → Legitimate, Otherwise → Phishing}
# DNSRecord { -1,1 }

# Rule: {If no DNS Record For The Domain → Phishing, Otherwise → Legitimate}
# web_traffic { -1,0,1 }

# Rule: {If Website Rank<100,000 → Legitimate, Else if Website Rank>100,000 → Suspicious, Otherwise → Phishing}
# Page_Rank { -1,1 }

# Rule: {If PageRank<0.2 → Phishing, Otherwise → Legitimate}
# Google_Index { 1,-1 }

# Rule: {If Webpage Indexed by Google → Legitimate, Otherwise → Phishing}
# Links_pointing_to_page { 1,0,-1 }

# Rule: {If # of Link Pointing to The Webpage=0 → Phishing, Else if #Of Link Pointing to The Webpage>0 and≤2 → Suspicious, Otherwise → Legitimate}
# Statistical_report { -1,1 }

# Rule: {If Host Belongs to Top Phishing IPs or Top Phishing Domains → Phishing, Otherwise → Legitimate}
# Result { 0,1 }

# Rule: {If 0 → Phishing, Else If 1 → Legitimate}

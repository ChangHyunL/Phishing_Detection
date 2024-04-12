# 1. url의 길이가 75자보다 긴 경우                                  o
#  -> 이를 피하기 위해 단축 url을 사용하는 경우
# 2. ip주소를 사용하는 경우                                         o
# 3. @,//,-,_, 또는 비표준 포트가 포함된 경우                       o
# 4. host의 길이가 30자보다 길거나 ‘.’이 5개 이상 포함된 경우        o
# 5. 유명 사이트와 유사한 url의 경우                                o
# 6. 트레픽이 현저히 낮은 경우
# 7. 구글 인덱스에 없는 경우
# 8. http를 사용하는 경우
# 9. 도메인이 1년이내에 만료되는 경우
# 10. 파비콘이 외부 도메인에서 오는 경우
# 11. 호스트 네임이 url에 없는 경우 (abnormal domain)
# 12. 도메인이 6개월 이내에 생성된 경우
import re
import Levenshtein
from urllib.parse import urlparse


def long_url(url):  # url의 길이가 75자 보다 큰 경우 비정상
    if len(url) > 75:
        return 1
    else:
        return 0


def having_ip(url):  # url의 형태가 ip주소 형태인 경우 비정상
    # 000.000.000.000
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    pattern += r'|((?:0x[0-9a-fA-F]{1,2}\.){3}0x[0-9a-fA-F]{1,2})'  # 16진수 ip형태
    pattern += r'|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}'  # ipv6

    if re.match(pattern, url):
        return 1
    else:
        return 0


def having_at(url):  # url에 악의적으로 사용될 가능성이 있는 문자가 사용된 경우 비정상
    if re.search('@', url):
        return 1
    else:
        return 0


def having_dash(url):
    if re.search('-', urlparse(url).netloc):
        return 1
    else:
        return 0


def having_underbar(url):
    if re.search('_', urlparse(url).netloc):
        return 1
    else:
        return 0


def having_redirection(url):
    start = url.find("://") + 3
    url = url[start:]
    if re.search('//', url):
        return 1
    else:
        return 0


def sub_domains(url):   # url에 .이 5개 이상 있는 경우 비정상
    if url.count(".") > 5:
        return 1
    else:
        return 0


def long_domain(url):  # url의 호스트 이름이 30글자보다 큰 경우 비정상
    domain = urlparse(url).netloc
    if len(domain) > 30:
        return 1
    else:
        return 0


# url의 도메인이 잘 알려진 url의 도메인과 비슷하게 생긴 경우 비정상
def similar_url(url, well_known_domain, threshold=2):
    domain = urlparse(url).netloc
    distance = Levenshtein.distance(domain, well_known_domain)
    if distance <= threshold:
        return 1
    else:
        return 0


def non_standard_port(url):
    parsed_url = urlparse(url)
    port = parsed_url.port
    if port is None:
        return 0
    elif port == 80:    # http 포트
        return 0
    elif port == 443:   # https 포트
        return 0
    else:
        return 1

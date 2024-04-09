# 1. url의 길이가 75자보다 긴 경우 -> 이를 피하기 위해 단축 url을 사용하는 경우
# 2. ip주소를 사용하는 경우
# 3. @,//,-,_, 또는 비표준 포트가 포함된 경우
# 4. host의 길이가 30자보다 길거나 ‘.’이 5개 이상 포함된 경우
# 5. 유명 사이트와 유사한 url의 경우
# 6. 웹사이트가 google 인덱스에 없는 경우
import re
import Levenshtein


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


def having_symbol(url):  # url에 악의적으로 사용될 가능성이 있는 문자가 사용된 경우 비정상
    pattern = r'[@\-_]|(//)'
    if re.search(pattern, url):
        return 1
    else:
        return 0


def sub_domains(url):   # url에 .이 5개 이상 있는 경우 비정상
    if url.count(".") > 5:
        return 1
    else:
        return 0


def long_host(url):  # url의 호스트 이름이 30글자보다 큰 경우 비정상
    start = url.find("://")
    end = url.find("/", start)
    if end == -1:
        hostname = url[start:]
    else:
        hostname = url[start:end]

    if len(hostname) > 30:
        return 1
    else:
        return 0


# url이 잘 알려진 url과 비슷하게 생긴 경우 비정상 -> hostname 비교
def similar_url(url, well_known_url, threshold=2):
    print('similar_url')
    start = url.find("://") + 3

    end = url.find("/", start)
    if end == -1:
        hostname = url[start:]
    else:
        hostname = url[start:end]

    distance = Levenshtein.distance(hostname, well_known_url)
    if distance <= threshold:
        return 1
    else:
        return 0


def google_index(url):
    pass

# 1. url의 길이가 75자보다 긴 경우 -> 이를 피하기 위해 단축 url을 사용하는 경우
# 2. ip주소를 사용하는 경우
# 3. @,//,-,_, 또는 비표준 포트가 포함된 경우
# 4. host의 길이가 30자보다 길거나 ‘.’이 5개 이상 포함된 경우
# 5. 유명 사이트와 유사한 url의 경우
# 6. 웹사이트가 google 인덱스에 없는 경우
import re


def long_url(url):
    if len(url) > 75:
        return 1
    else:
        return 0


def having_ip(url):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    pattern += r'|((?:0x[0-9a-fA-F]{1,2}\.){3}0x[0-9a-fA-F]{1,2})'
    pattern += r'|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}'

    if re.match(pattern, url):
        return 1
    else:
        return 0


def having_symbol(url):
    pattern = r'[@\-_]|(//)'
    if re.search(pattern, url):
        return 1
    else:
        return 0


def sub_domains(url):
    pass


def long_host(url):
    pass


def similar_url(url):
    pass


def google_index(url):
    pass

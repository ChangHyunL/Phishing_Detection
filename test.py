import re

url = "https://greeksharifa.github.io/%EC%@A0%95%EA%B7%9C%ED%91-usage-03-basic/"


def long_url(url):
    print('long_url')
    if len(url) > 75:
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


def having_ip(url):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    pattern += r'|((?:0x[0-9a-fA-F]{1,2}\.){3}0x[0-9a-fA-F]{1,2})'
    pattern += r'|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}'

    print('having_ip')
    if re.match(pattern, url):
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


def having_symbol(url):
    pattern = r'[@\-_]|(//)'
    print('having_symbol')
    if re.search(pattern, url):
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


long_url(url)
having_ip(url)
having_symbol(url)

import re
import Levenshtein
import requests

well_known_hostname = "www.google.com"
url = "https://greekaa....aasaasharifa.github.io/%EC%@A0%95%EA%B7%9C%ED%91-usage-03-basic/"


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


def sub_domains(url):
    print('sub_domains')
    if url.count(".") > 5:
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


def long_host(url):
    print('long_host')
    start = url.find("://")+3
    end = url.find("/", start)
    if end == -1:
        hostname = url[start:]
    else:
        hostname = url[start:end]
    if len(hostname) > 30:
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


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
        return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
    else:
        return print(f"{url}는 유효한 url 주소입니다. ✅")


# def google_index(url):
#     google_search_url = f"https://www.google.com/search?q=site:{url}"
#     response = requests.get(google_search_url)
#     print(response.text)
#     if response.status_code == 200:
#         if "did not match any documents" in response.text:
#             return print(f"{url}는 유효하지 않은 url 주소입니다. ❌")
#         else:
#             return print(f"{url}는 유효한 url 주소입니다. ✅")
#     else:
#         return None  # Unable to determine


long_url(url)
having_ip(url)
having_symbol(url)
sub_domains(url)
long_host(url)
url = 'https://www.g00gle.com'
similar_url(url, well_known_hostname)
# url = "1209bfasjkdiouiuoakljklaajkl;sd;!@#41o023409820171$@!#$!@#$"
# url = 'https://www.naver.com'
# google_index(url)

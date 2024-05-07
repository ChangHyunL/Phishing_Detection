# url이 블랙리스트에 있는지 확인하는 코드 필요 -> 이 코드는 학습을 위한 코드이므로 일단 빼둠 마지막에 DB구성 후 추가할 예정
from dateutil import parser
from datetime import datetime
import re
import Levenshtein
from urllib.parse import urlparse
import requests
import ssl
import socket
import whois
import pandas as pd

filepath = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/rawdata/non_phishing.csv"
ca_filepath = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/RuleDetection/trusted_ca.csv"
input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/normal_url.csv'
output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_normal_url.csv'

df = pd.read_csv(input_file_path, header=None, names=['is_redirection'])
# df = pd.read_csv(input_file_path, header=None, names=['url'])


# def is_redirection(url):    # 만약 url이 redirection한다면 redirection하는 url을 반환해서 그 url을 분석
#     try:
#         response = requests.head(url, allow_redirects=True)
#         if response.url == url:
#             return 0
#         else:
#             return 1
#     except:
#         print(f"{url}은 url이 아닙니다.")
#         return 1


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
    url_check = url[start:]
    if re.search('//', url_check):
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

def read_well_known_hostnames(filepath):
    with open(filepath, 'r') as file:
        well_known_hostnames = [
            urlparse(line).netloc for line in file.read().splitlines()]
    return well_known_hostnames


def similar_url(url, well_known_hostnames, threshold=2):
    hostname = urlparse(url).netloc

    # 파일에서 well_known_hostname 목록을 읽어온다.
    # with open(filepath, 'r') as file:
    #     well_known_hostnames = [
    #         urlparse(line).netloc for line in file.read().splitlines()]

    for well_known_hostname in well_known_hostnames:
        distance = Levenshtein.distance(hostname, well_known_hostname)

        # hostname과 well_known_hostname이 일치하지 않는 경우만 거리를 계산
        if hostname != well_known_hostname:
            if distance <= threshold:
                return 1
        else:
            return 0
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


def is_https(url):
    if urlparse(url).scheme == 'https':
        return 0
    else:
        return 1

# 네트워크가 필요함

# 신뢰받는 인증기관인지, 인증서의 수명도 확인하려했으나 실제로 신뢰받는 사이트의 인증서의 수명이 길지않음 -> 불필요한 것 같음
# 구글, 마이크로소프트, 애플의 인증서의 수명이 1년이 안됨


def read_trusted_ca(ca_filepath):
    with open(ca_filepath, 'r', encoding='utf-8') as f:
        trusted_issuer = f.read()
    print(trusted_issuer)
    return trusted_issuer


def is_trusted_cert(url, trusted_issuer):
    try:
        hostname = urlparse(url).netloc
        context = ssl.create_default_context()
        conn = context.wrap_socket(socket.socket(
            socket.AF_INET), server_hostname=hostname)
        conn.connect((hostname, 443))
        cert = conn.getpeercert()
        issuer = dict(x[0] for x in cert['issuer'])
        issuer_name = issuer.get('organizationName', '')
        # with open('IncludedCACertificateReportForMSFT.csv', 'r', encoding='utf-8') as f:
        #     trusted_issuer = f.read()
        for trusted_ca in trusted_issuer:
            if trusted_ca in issuer_name:
                return 0
        return 1
    except Exception as e:
        print(f"Error while checking url {url}: {e}")
        return 1


def get_creation_date(url):
    url = urlparse(url).netloc
    try:
        domain = whois.whois(url)
        print(domain.creation_date)
        creation_date = domain.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if not isinstance(creation_date, datetime):
            try:
                creation_date = parser.parse(str(creation_date))
            except ValueError:
                print("Creation date format is not supported.")
                return 1
        today = datetime.now()
        age = today - creation_date
        if age.days < 180:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def get_expiration_date(url):
    try:
        domain = whois.whois(url)
        expiration_date = domain.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        if not isinstance(creation_date, datetime):
            try:
                creation_date = parser.parse(str(creation_date))
            except ValueError:
                print("Creation date format is not supported.")
                return 1
        today = datetime.now()
        age = expiration_date - today
        if age.days < 365:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


# df['is_redirection'] = df['url'].apply(is_redirection)

df['long_url'] = df['is_redirection'].apply(long_url)
df['having_ip'] = df['is_redirection'].apply(having_ip)
df['having_at'] = df['is_redirection'].apply(having_at)
df['having_dash'] = df['is_redirection'].apply(having_dash)
df['having_underbar'] = df['is_redirection'].apply(having_underbar)
df['having_redirection'] = df['is_redirection'].apply(having_redirection)
df['sub_domains'] = df['is_redirection'].apply(sub_domains)
df['long_domain'] = df['is_redirection'].apply(long_domain)
df.to_csv(output_file_path, index=False)
well_known_hostnames = read_well_known_hostnames(filepath)
df['similar_url'] = df['is_redirection'].apply(
    lambda x: similar_url(x, well_known_hostnames, threshold=2))
df.to_csv(output_file_path, index=False)
df['non_standard_port'] = df['is_redirection'].apply(non_standard_port)
df['is_https'] = df['is_redirection'].apply(is_https)
df.to_csv(output_file_path, index=False)
trusted_issuer = read_trusted_ca(ca_filepath)
df['is_trusted_cert'] = df['is_redirection'].apply(
    lambda x: is_trusted_cert(x, trusted_issuer))
df.to_csv(output_file_path, index=False)
df['get_creation_date'] = df['is_redirection'].apply(get_creation_date)
df.to_csv(output_file_path, index=False)
df['get_expiration_date'] = df['is_redirection'].apply(get_expiration_date)
df.to_csv(output_file_path, index=False)

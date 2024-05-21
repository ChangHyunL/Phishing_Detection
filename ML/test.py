import joblib
import pandas as pd
import requests
from datetime import datetime
import re
import Levenshtein
import whois
import ssl
import socket
from urllib.parse import urlparse
from tensorflow.keras.models import load_model


# 모델과 벡터라이저 로드 (이미 학습된 상태라고 가정)
# model = load_model(
#     'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Models/adam_phishing_detection_model.keras')
model = joblib.load(
    'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Models/isolation_forest_model.pkl')

# 테스트할 URL
# test_url = "https://portal.dankook.ac.kr/p/S01/"
# test_url = "https://www.naver.com/"
test_url = 'https://domain.autopay.electricfarmgates.com/?SMdY280YU=45VQD11D...'

filepath = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/rawdata/non_phishing.csv"
ca_filepath = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/RuleDetection/trusted_ca.csv"


def is_redirection(url):    # 만약 url이 redirection한다면 redirection하는 url을 반환해서 그 url을 분석
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except:
        print(f"{url}은 url이 아닙니다.")
        return 1


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


def read_trusted_ca(ca_filepath):
    with open(ca_filepath, 'r', encoding='utf-8') as f:
        trusted_issuer = f.read()
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
        for trusted_ca in trusted_issuer:
            if trusted_ca in issuer_name:
                return 0
        return 1
    except Exception as e:
        print(f"Error while checking url {url}: {e}")
        return 1


def get_creation_date(url):
    try:
        domain = whois.whois(url)
        creation_date = domain.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        print(
            f'{url}: type: {type(creation_date)}, {creation_date}')
        today = datetime.now()
        age = today - creation_date
        if age.days < 180:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"{url}, Error: {e}")
        return 1


def get_expiration_date(url):
    try:
        domain = whois.whois(url)
        expiration_date = domain.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
        print(
            f'{url}: type: {type(expiration_date)}, {expiration_date}, {expiration_date.year}')
        today = datetime.now()
        age = expiration_date - today
        if age.days < 180:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1


def prepare_input(url):
    well_known_hostnames = read_well_known_hostnames(filepath)
    trusted_issuer = read_trusted_ca(ca_filepath)
    modified_url = is_redirection(url)
    # print(modified_url)
    data = {
        'url': [is_redirection(url)],
        'long_url': [long_url(modified_url)],
        'having_ip': [having_ip(modified_url)],
        'having_at': [having_at(modified_url)],
        'having_dash': [having_dash(modified_url)],
        'having_underbar': [having_underbar(modified_url)],
        'having_redirection': [having_redirection(modified_url)],
        'sub_domains': [sub_domains(modified_url)],
        'long_domain': [long_domain(modified_url)],
        'similar_url': [similar_url(modified_url, well_known_hostnames)],
        'non_standard_port': [non_standard_port(modified_url)],
        'is_https': [is_https(modified_url)],
        'is_trusted_cert': [is_trusted_cert(modified_url, trusted_issuer)],
        'get_creation_date': [get_creation_date(modified_url)],
        'get_expiration_date': [get_expiration_date(modified_url)]
    }
    df = pd.DataFrame(data)
    X_input = df.drop('url', axis=1)  # URL 열은 피처로 사용하지 않음
    return X_input


# 모델로 예측
X_input = prepare_input(test_url)
# 전송해야하는 값
X_input.to_csv('x_input.csv', index=False)


def load_input_data(filepath):
    df = pd.read_csv(filepath)
    return df


input_data = load_input_data(
    'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/x_input.csv')
prediction = model.predict(input_data)
# print(input_data.values[0])
# print(prediction)
# prediction = model.predict(X_input)

# # 예측 결과 해석 (0: 정상, 1: 피싱)
# result = "Phishing" if prediction[0] == 1 else "Not Phishing"
# print(f'The URL {test_url} is {result}.')

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

model = joblib.load('./ML/Models/best_rf_model.pkl')
filepath = "./ML/Datasets/rawdata/non_phishing.csv"
ca_filepath = "./RuleDetection/trusted_ca.csv"


def is_redirection(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response.url
    except:
        print(f"{url}은 url이 아닙니다.")
        return 1


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


def having_at(url):
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


def sub_domains(url):
    if url.count(".") > 5:
        return 1
    else:
        return 0


def long_domain(url):
    domain = urlparse(url).netloc
    if len(domain) > 30:
        return 1
    else:
        return 0


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
    elif port == 80:
        return 0
    elif port == 443:
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
        today = datetime.now()
        age = today - creation_date
        if age.days < 180:
            return 1
        else:
            return 0
    except Exception as e:
        # print(f"{url}, Error: {e}")
        return 1


def get_expiration_date(url):
    try:
        domain = whois.whois(url)
        expiration_date = domain.expiration_date
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]
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
    if modified_url == 1:
        data = {
            'url': [1],
            'long_url': [1],
            'having_ip': [1],
            'having_at': [1],
            'having_dash': [1],
            'having_underbar': [1],
            'having_redirection': [1],
            'sub_domains': [1],
            'long_domain': [1],
            'similar_url': [1],
            'non_standard_port': [1],
            'is_https': [1],
            'is_trusted_cert': [1],
            'get_creation_date': [1],
            'get_expiration_date': [1]
        }
    else:
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
    X_input = df.drop('url', axis=1)
    return X_input

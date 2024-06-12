from dateutil import parser
from datetime import datetime
import re
import Levenshtein
from urllib.parse import urlparse
import requests
import ssl
import socket
import whois

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
        if hostname == well_known_hostname:
            break
        distance = Levenshtein.distance(hostname, well_known_hostname)
        if distance <= threshold:
            print(well_known_hostname)
            return 1
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
                print('pass')
                return 0
        print(issuer_name)
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


url = 'https://www.deepl.com/ko/translator'
similar_url(url, read_well_known_hostnames(filepath), threshold=2)
is_trusted_cert(url, read_trusted_ca(ca_filepath))

# df['is_redirection'] = df['url'].apply(is_redirection)

# df['long_url'] = df['is_redirection'].apply(long_url)
# df['having_ip'] = df['is_redirection'].apply(having_ip)
# df['having_at'] = df['is_redirection'].apply(having_at)
# df['having_dash'] = df['is_redirection'].apply(having_dash)
# df['having_underbar'] = df['is_redirection'].apply(having_underbar)
# df['having_redirection'] = df['is_redirection'].apply(having_redirection)
# df['sub_domains'] = df['is_redirection'].apply(sub_domains)
# df['long_domain'] = df['is_redirection'].apply(long_domain)
# df.to_csv(output_file_path, index=False)
# well_known_hostnames = read_well_known_hostnames(filepath)
# df['similar_url'] = df['is_redirection'].apply(
#     lambda x: similar_url(x, well_known_hostnames, threshold=2))
# df.to_csv(output_file_path, index=False)
# df['non_standard_port'] = df['is_redirection'].apply(non_standard_port)
# df['is_https'] = df['is_redirection'].apply(is_https)
# df.to_csv(output_file_path, index=False)
# trusted_issuer = read_trusted_ca(ca_filepath)
# df['is_trusted_cert'] = df['is_redirection'].apply(
#     lambda x: is_trusted_cert(x, trusted_issuer))
# df.to_csv(output_file_path, index=False)
# df['get_creation_date'] = df['is_redirection'].apply(get_creation_date)
# df.to_csv(output_file_path, index=False)
# df['get_expiration_date'] = df['is_redirection'].apply(get_expiration_date)
# df.to_csv(output_file_path, index=False)

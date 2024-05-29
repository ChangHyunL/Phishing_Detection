import requests
from bs4 import BeautifulSoup


def download_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None


def download_js(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        js_files = [script['src']
                    for script in soup.find_all('script') if 'src' in script.attrs]
        js_contents = []
        for js_file in js_files:
            js_response = requests.get(js_file)
            if js_response.status_code == 200:
                js_contents.append(js_response.text)
        return js_contents
    else:
        return None


url = 'http://example.com'
html_content = download_html(url)
js_contents = download_js(url)

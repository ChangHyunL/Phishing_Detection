import requests
import pandas as pd

input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/non_phishing.csv'
output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/normal_url.csv'
df = pd.read_csv(input_file_path, header=None,
                 names=['url'], usecols=[0])


def is_redirection(url):    # 만약 url이 redirection한다면 redirection하는 url을 반환해서 그 url을 분석
    try:
        response = requests.head(url, allow_redirects=True, timeout=1)
        print(response)
        return response.url
    except:
        print(f"{url}은 url이 아닙니다.")
        return None


df['is_redirection'] = df['url'].apply(is_redirection)
df.dropna(subset=['is_redirection'], inplace=True)
df.to_csv(output_file_path, index=False)

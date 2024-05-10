# import csv
# import os

# # 현재 작업 디렉토리 확인
# print("현재 디렉토리:", os.getcwd())

# # 입력 파일(txt)과 출력 파일(csv) 경로 설정
# input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/top50K.csv'
# output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/non_phishing.csv'

# # txt 파일에서 각 줄을 읽어와서 "https://www."를 추가한 후 csv 파일에 쓰기
# with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
#     # csv_writer = csv.writer(output_file)
#     # for line in input_file:
#     #     # 각 줄의 앞에 "https://www."를 추가하여 쓰기
#     #     csv_writer.writerow(['https://www.' + line[0].strip()])

#     csv_reader = csv.reader(input_file)
#     csv_writer = csv.writer(output_file)

#     for row in csv_reader:
#         # 첫 번째 열에 "https://www."를 추가
#         if row:  # 비어있지 않은 행만 처리
#             modified_url = 'https://www.' + row[0].strip()
#             # 한 항목만 포함된 리스트로 쓰기
#             csv_writer.writerow([modified_url])

# print(f"CSV 파일이 생성되었습니다: {output_file_path}")

# import pandas as pd
# input_file_path = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/RuleDetection/IncludedCACertificateReportForMSFT.csv"
# output_file_path = "C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/RuleDetection/trusted_ca.csv"
# # 원본 CSV 파일 읽기
# df = pd.read_csv(input_file_path, encoding='utf-8')

# # 2번째 열의 데이터 선택 및 중복 제거
# unique_data = df.iloc[:, 1].drop_duplicates()

# # 결과 데이터를 새로운 CSV 파일에 저장
# unique_data.to_csv(output_file_path, index=False, encoding='utf-8')


# import csv

# # 입력 파일(csv)과 출력 파일(csv) 경로 설정
# input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/phishtank.csv'
# output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/phishing.csv'

# # 2번째 열의 정보만 추출하여 새로운 csv 파일에 쓰기
# with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
#     csv_reader = csv.reader(input_file)
#     csv_writer = csv.writer(output_file)
#     for row in csv_reader:
#         if len(row) > 1:  # 최소한 2개의 열이 있을 때
#             csv_writer.writerow([row[1]])  # 2번째 열의 정보만 쓰기

# print(f"CSV 파일이 생성되었습니다: {output_file_path}")


# import pandas as pd

# # CSV 파일 읽기

# input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/non_phishing.csv'
# output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_non_phishing_urls.csv'
# df = pd.read_csv(input_file_path, header=None, names=['url'])

# # long_url 규칙 함수 정의


# def long_url(url):
#     if len(url) > 75:
#         return 1
#     else:
#         return 0

# # 여기에 추가 규칙 함수를 정의할 수 있습니다.


# # 규칙 적용
# df['long_url'] = df['url'].apply(long_url)

# # 추가 규칙 적용 예시: df['rule2'] = df['url'].apply(rule2)

# # 결과를 새로운 CSV 파일로 저장
# df.to_csv(output_file_path, index=False)


# import csv

# # 원본 CSV 파일 이름
# input_file_name = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/normal_url.csv'
# # 수정된 데이터를 저장할 새 CSV 파일 이름
# output_file_name = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/modified.csv'

# with open(input_file_name, mode='r', encoding='utf-8') as infile, open(output_file_name, mode='w', newline='', encoding='utf-8') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)

#     for row in reader:
#         modified_row = []
#         for cell in row:
#             # 데이터의 길이가 1보다 클 때만 수정 과정을 진행
#             if len(cell) > 1:
#                 # 마지막 글자가 '.'인 경우
#                 if cell[-1] == '.':
#                     cell = cell[:-1]
#                 # 마지막에서 두 번째 글자가 '.'이고 마지막 글자가 아닌 경우 (단어가 3글자 이상일 때만 해당)
#                 elif cell[-2] == '.' and len(cell) > 2:
#                     cell = cell[:-2] + cell[-1]
#             modified_row.append(cell)
#         writer.writerow(modified_row)


import pandas as pd
# import csv
# from urllib.parse import urlparse, urlunparse

# # 원본 CSV 파일 이름
# input_file_name = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/normal_url.csv'
# # 수정된 데이터를 저장할 새 CSV 파일 이름
# output_file_name = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/modified.csv'


# def remove_dot_from_hostname(url):
#     parsed_url = urlparse(url)
#     hostname = parsed_url.netloc
#     # hostname의 마지막 글자가 점인 경우 제거
#     if hostname.endswith('.'):
#         hostname = hostname[:-1]
#     # 수정된 hostname으로 새로운 URL 구성
#     # 변경된 netloc을 사용하여 새로운 URL 생성
#     modified_url = urlunparse(parsed_url._replace(netloc=hostname))
#     return modified_url


# with open(input_file_name, mode='r', encoding='utf-8') as infile, open(output_file_name, mode='w', newline='', encoding='utf-8') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)

#     for row in reader:
#         modified_row = []
#         for cell in row:
#             # cell이 URL 형태인지 확인 (http:// 또는 https://로 시작하는지)
#             if cell.startswith('http://') or cell.startswith('https://'):
#                 cell = remove_dot_from_hostname(cell)
#             modified_row.append(cell)
#         writer.writerow(modified_row)

# 데이터 셋 삭제 및 병합하기


file = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_malicious_url.csv'
# file = 'merged2.csv'
file1 = 'processed_malicious_url1.csv'
# file = 'merged.csv'
# file1 = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_malicious_url2_7.csv'
# file1 = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_normal_url14.csv'

df = pd.read_csv(file)
add = pd.read_csv(file1)

# df.drop([df.columns[13], df.columns[14]], axis=1, inplace=True)
# df.drop(df.columns[0], axis=1, inplace=True)

# df.to_csv('merged3.csv', index=False)

merged_dataframe = pd.concat([df, add], axis=1)
# merged_dataframe = pd.concat([df, add])

# 결과 저장
# merged_dataframe.to_csv('merged1.csv', index=False)
# merged_dataframe.to_csv('merged.csv', index=False)
merged_dataframe.to_csv('processed_malicious_url2.csv', index=False)

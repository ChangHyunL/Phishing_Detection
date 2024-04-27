import csv
import os

# # 현재 작업 디렉토리 확인
# print("현재 디렉토리:", os.getcwd())

# # 입력 파일(txt)과 출력 파일(csv) 경로 설정
# input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/non_phishing.txt'
# output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/non_phishing.csv'

# # txt 파일에서 각 줄을 읽어와서 "https://www."를 추가한 후 csv 파일에 쓰기
# with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
#     csv_writer = csv.writer(output_file)
#     for line in input_file:
#         # 각 줄의 앞에 "https://www."를 추가하여 쓰기
#         csv_writer.writerow(['https://www.' + line.strip()])

# print(f"CSV 파일이 생성되었습니다: {output_file_path}")


import csv

# 입력 파일(csv)과 출력 파일(csv) 경로 설정
input_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/phishtank.csv'
output_file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/phishing.csv'

# 2번째 열의 정보만 추출하여 새로운 csv 파일에 쓰기
with open(input_file_path, 'r', newline='', encoding='utf-8') as input_file, open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)
    for row in csv_reader:
        if len(row) > 1:  # 최소한 2개의 열이 있을 때
            csv_writer.writerow([row[1]])  # 2번째 열의 정보만 쓰기

print(f"CSV 파일이 생성되었습니다: {output_file_path}")

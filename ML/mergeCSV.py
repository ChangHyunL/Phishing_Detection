import csv
import pandas as pd

file = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/2nd/2nd_processed_malicious_url.csv'
file1 = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/2nd/2nd_processed_malicious_url1.csv'
# CSV 파일 읽기
df = pd.read_csv(file)

# 중복된 행 제거
df = df.drop_duplicates(subset=df.columns[0])

# 결과를 새로운 CSV 파일로 저장
df.to_csv(file1, index=False)


# 입력 파일과 출력 파일 경로
# input_file = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_malicious_url.csv'
# output_file = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/processed_malicious_url1.csv'

# df = pd.read_csv(input_file)

# df['isphishing'] = 1
# df.to_csv(output_file, index=False)

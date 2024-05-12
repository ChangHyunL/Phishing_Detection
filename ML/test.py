import pandas as pd

# 파일 경로
# file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/2nd/2nd_processed_malicious_url.csv'
file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/testDataset/merged.csv'

# CSV 파일을 데이터프레임으로 읽어옴
df = pd.read_csv(file_path)

# 각 열의 데이터 값의 갯수 출력
for col in df.columns:
    value_counts = df[col].value_counts()
    print(f"Column: {col}")
    print(value_counts)
    print("\n")

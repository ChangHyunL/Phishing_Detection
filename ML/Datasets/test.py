import pandas as pd

# CSV 파일 경로
file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/3rd/normal.csv'

# CSV 파일 읽기
data = pd.read_csv(file_path)

# 각 열별로 0과 1의 개수 출력
for column in data.columns:
    counts = data[column].value_counts()
    print(f"Column '{column}':")
    if 0 in counts.index:
        print(f"  - 0의 개수: {counts[0]}")
    else:
        print("  - 0의 개수: 0")
    if 1 in counts.index:
        print(f"  - 1의 개수: {counts[1]}")
    else:
        print("  - 1의 개수: 0")

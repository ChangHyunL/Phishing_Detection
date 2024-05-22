import pandas as pd

# CSV 파일 경로
file_path = 'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/3rd/normal.csv'
merge_file_path = 'random_filtered_data.csv'

# CSV 파일 읽기
df = pd.read_csv(file_path)

# # 각 열별로 0과 1의 개수 출력
# for column in data.columns:
#     counts = data[column].value_counts()
#     print(f"Column '{column}':")
#     if 0 in counts.index:
#         print(f"  - 0의 개수: {counts[0]}")
#     else:
#         print("  - 0의 개수: 0")
#     if 1 in counts.index:
#         print(f"  - 1의 개수: {counts[1]}")
#     else:
#         print("  - 1의 개수: 0")

# 'your_column_name' 열에서 'your_specific_value' 값을 가진 데이터 필터링
# filtered_data = df[df.iloc[:, 13] == 1]

# 필터링된 데이터에서 랜덤하게 1000개 선택
# min 함수를 사용하여 조건을 만족하는 데이터 수와 1000 중 더 작은 값을 sample 메소드에 전달
result_data = df.sample(
    n=min(len(df), 8746), random_state=1)

result_data.to_csv('2.csv', index=False)

# try:
#     merge_df = pd.read_csv('merged.csv')
# except FileNotFoundError:
#     merge_df = pd.DataFrame()

# merged_data = pd.concat([merge_df, result_data], ignore_index=True)
# merged_data.to_csv('merged.csv', index=False)
# # 결과 확인
print(result_data)
# print(merged_data)

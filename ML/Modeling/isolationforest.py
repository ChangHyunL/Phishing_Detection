from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib

# 데이터 로드 (이전에 사용한 데이터와 동일)
df = pd.read_csv(
    'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phising_Detection/ML/Datasets/testDataset/2nd_merged.csv')

# 특성과 레이블 분리
X = df.drop('isphishing', axis=1)  # features
y = df['isphishing']  # target value
# 정상 데이터만 추출
normal_data = df[df['isphishing'] == 0].drop('isphishing', axis=1)

# Isolation Forest 모델 생성 및 학습
iso_forest = IsolationForest(
    n_estimators=100, max_samples='auto', contamination='auto', random_state=42)
iso_forest.fit(normal_data)

# 모델 저장
joblib.dump(iso_forest, 'isolation_forest_model.pkl')
model_loaded = joblib.load('isolation_forest_model.pkl')

# 전체 데이터로 예측
predictions = model_loaded.predict(X)
df['prediction'] = predictions
df['prediction'] = df['prediction'].apply(
    lambda x: 1 if x == -1 else 0)  # -1을 피싱(이상치)으로 1로 변환, 1을 정상으로 0으로 변환

print("Isolation Forest Predictions: ")
print(df[['isphishing', 'prediction']])

# 분류 보고서 및 정확도 출력
print("Classification Report: ")
print(classification_report(y, df['prediction']))
print(f"Accuracy: {accuracy_score(y, df['prediction']) * 100:.2f}%")

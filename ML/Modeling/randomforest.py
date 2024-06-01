import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
import joblib

# 데이터 로드
data = pd.read_csv(
    'C:/Users/dlckd/Desktop/2024-1학기/캡스톤디자인/Phishing_Detection/ML/Datasets/testDataset/4th_merged.csv')
X = data.drop('isphishing', axis=1)  # 특성 데이터
y = data['isphishing']  # 타겟 레이블

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# SMOTE 적용
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# 랜덤 포레스트 모델 생성
random_forest_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 모델 훈련
random_forest_model.fit(X_train_resampled, y_train_resampled)

# 모델 저장
joblib.dump(random_forest_model, 'random_forest_model.pkl')

# 모델 로드
model_loaded = joblib.load('random_forest_model.pkl')

# 예측 및 성능 평가
predictions = model_loaded.predict(X_test)
print("Classification Report: ")
print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 데이터 로드
data = pd.read_csv('train_set.csv')
X = data.drop('label', axis=1)  # 특성 데이터
y = data['label']  # 타겟 레이블

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 모델 생성
random_forest_model = RandomForestClassifier(n_estimators=100, random_state=42)

# 모델 훈련
random_forest_model.fit(X_train, y_train)

joblib.dump(random_forest_model, 'random_forest_model.pkl')
model_loaded = joblib.load('random_forest_model.pkl')

# 예측 및 성능 평가
predictions = model_loaded.predict(X_test)
print("Accuracy: ", accuracy_score(y_test, predictions))
print("Classification Report: \n", classification_report(y_test, predictions))

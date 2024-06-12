from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import joblib

# 'merged.csv'가 다음과 같은 구조를 가진다고 가정
# "url", "feature1", "feature2", ..., "feature14", "isphishing"
# 0은 정상 1은 피싱, "isphishing"은 실제 url이 피싱인지 아닌지를 나타냄

df = pd.read_csv('./ML/Datasets/testDataset/4th_merged.csv')

# 특성과 레이블 분리
X = df.drop('isphishing', axis=1)    # features
y = df['isphishing']  # target value

# 데이터셋 분할: 학습 세트와 테스트 세트
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 로지스틱 회귀 모델 생성 및 학습
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)

joblib.dump(logistic_model, 'logistic_model.pkl')
model_loaded = joblib.load('logistic_model.pkl')

# 테스트 데이터로 모델 성능 평가
predictions = model_loaded.predict(X_test)

# 분류 보고서 및 정확도 출력
print("Classification Report: ")
print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")

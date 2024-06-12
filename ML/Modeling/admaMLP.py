import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
from sklearn.metrics import precision_score, recall_score, f1_score
from tensorflow.keras.metrics import Precision, Recall

# 데이터 로드
df = pd.read_csv('./ML/Datasets/testDataset/4th_merged.csv')

# 특성과 레이블 분리
X = df.drop('isphishing', axis=1)    # features
y = df['isphishing']  # target value

# 데이터 정규화
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 데이터셋 분할: 학습 세트와 테스트 세트
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 모델 정의
model = Sequential()
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Adam 옵티마이저 정의
adam_optimizer = Adam(learning_rate=0.01)

# 모델 컴파일 - Precision과 Recall 메트릭 추가
model.compile(loss='binary_crossentropy',
              optimizer=adam_optimizer,
              metrics=['accuracy', Precision(), Recall()])

# 학습률 스케줄링 함수 정의


def scheduler(epoch, lr):
    if epoch < 10:
        return lr
    else:
        return float(lr * tf.math.exp(-0.1).numpy())  # 이 부분을 수정


# 학습률 스케줄러 콜백 정의
lr_scheduler = LearningRateScheduler(scheduler)

# 얼리 스토핑 콜백 정의
early_stopping = EarlyStopping(
    monitor='val_loss', patience=10, restore_best_weights=True)

# 모델 학습
model.fit(X_train, y_train, epochs=50, batch_size=10,
          validation_data=(X_test, y_test), callbacks=[early_stopping, lr_scheduler])

# 모델 평가
loss, accuracy, precision, recall = model.evaluate(X_test, y_test)
f1 = 2 * (precision * recall) / (precision + recall)
print(f"Test Accuracy: {accuracy * 100:.2f}%")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# 모델 저장
model.save('./ML/Models/adam_phishing_detection_model.keras')

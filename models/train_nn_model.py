import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ===== 1. Load dataset =====
df = pd.read_csv("app/data/loan_data.csv")

# ===== 2. Basic cleaning =====
df.drop_duplicates(inplace=True)
df.fillna(df.median(numeric_only=True), inplace=True)
for col in df.select_dtypes(include=['object']):
    df[col] = df[col].fillna(df[col].mode()[0])

# ===== 3. Feature Engineering =====
df["income_to_loan_ratio"] = df["person_income"] / (df["loan_amnt"] + 1)
df["risk_factor"] = df["loan_int_rate"] * df["loan_percent_income"]

# Encode categorical features
cat_cols = ['person_gender', 'person_education', 'person_home_ownership',
            'loan_intent', 'previous_loan_defaults_on_file']

le = LabelEncoder()
for col in cat_cols:
    df[col] = le.fit_transform(df[col])

# ===== 4. Prepare X, y =====
X = df.drop(columns=["loan_status"])
y = df["loan_status"]  # 1 = Default, 0 = Non-default

# ===== 5. Scale =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===== 6. Train-test split =====
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ===== 7. Build NN =====
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# ===== 8. Train model =====
history = model.fit(X_train, y_train, epochs=25, batch_size=32, validation_split=0.2, verbose=1)

# ===== 9. Evaluate =====
loss, acc = model.evaluate(X_test, y_test)
print(f"✅ Model trained | Accuracy: {acc:.4f}")

# ===== 10. Save model =====
model.save("app/models/pd_model_nn.h5")
print("💾 Model saved at: app/models/pd_model_nn.h5")

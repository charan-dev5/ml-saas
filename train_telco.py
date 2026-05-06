import pandas as pd
import joblib

df = pd.read_excel("C:/saas/Telco_customer_churn.xlsx")
df.to_csv("C:/saas/telco_data.csv", index=False)
df.columns = df.columns.str.strip()
print(df.columns)
df = df.dropna(subset=["Tenure Months", "Monthly Charges", "Total Charges", "Contract", "Internet Service", "Payment Method", "Churn Label"])
print(df.shape)

X = df[["Tenure Months", "Monthly Charges", "Total Charges", "Contract", "Internet Service", "Payment Method"]]
X = pd.get_dummies(X)
y = df["Churn Label"]
print(df["Churn Label"].unique())
y = (y == "Yes").astype(int)
print(y.value_counts())

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test, predictions))

joblib.dump(model, "telco_model.pkl")
joblib.dump(X.columns.tolist(), "telco_columns.pkl")
# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VDcEQoCJH4iGoRwRUXMmYdwec1J4bhU3
"""

import pandas as pd

# Load the dataset
file_path = 'creditcard.csv'
data = pd.read_csv(file_path)

# Explore the dataset
print(data.head())

from sklearn.preprocessing import StandardScaler
from sklearn.utils import resample

# Check for missing values
print(data.isnull().sum())

# Standardize the 'Amount' and 'Time' columns
scaler = StandardScaler()
data['Amount'] = scaler.fit_transform(data['Amount'].values.reshape(-1, 1))
data['Time'] = scaler.fit_transform(data['Time'].values.reshape(-1, 1))

# Address class imbalance by upsampling the minority class
fraud = data[data['Class'] == 1]
legit = data[data['Class'] == 0]

fraud_upsampled = resample(fraud,
                           replace=True,  # sample with replacement
                           n_samples=len(legit),  # match number in majority class
                           random_state=42)  # reproducible results

data_upsampled = pd.concat([legit, fraud_upsampled])

# Shuffle the dataset
data_upsampled = data_upsampled.sample(frac=1, random_state=42).reset_index(drop=True)

# Separate features and target
X = data_upsampled.drop('Class', axis=1)
y = data_upsampled['Class']

from sklearn.model_selection import train_test_split

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Train Logistic Regression
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)

# Train Decision Tree
dt_model = DecisionTreeClassifier()
dt_model.fit(X_train, y_train)

# Train Random Forest
rf_model = RandomForestClassifier()
rf_model.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# Function to evaluate the model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
    print(f"Precision: {precision_score(y_test, y_pred)}")
    print(f"Recall: {recall_score(y_test, y_pred)}")
    print(f"F1 Score: {f1_score(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))

print("Logistic Regression:")
evaluate_model(lr_model, X_test, y_test)

print("\nDecision Tree:")
evaluate_model(dt_model, X_test, y_test)

print("\nRandom Forest:")
evaluate_model(rf_model, X_test, y_test)

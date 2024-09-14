# -*- coding: utf-8 -*-
"""Alzheimers.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1W0FKTE805p65bpxLLQ7GFEAAo7Pv8P5S

# Project Content
1. [Connection to Kaggle](#1)
2. [Download Dataset](#2)
3. [Import Libraries & Dataset](#3)
4. [Dataset Basic Analysis](#4)
    * 4.1 [Getting to Know the Variables](#4.1)
    * 4.2 [Datatypes](#4.2)
        * 4.2.1 [Drop DoctorInCharge](#4.2.1)
    * 4.3 [Missing Values & Duplicates](#4.3)
    * 4.4 [Statistical Summary](#4.4)
    * 4.5 [Analyze On Diagnosis](#4.5)
5. [EDA](#5)
    * 5.1 [Seperating Variables](#5.1)
    * 5.2 [Countplot](#5.2)
    * 5.3 [Distribution](#5.3)
    * 5.4 [Boxplot](#5.4)
    * 5.5 [Heatmap](#5.5)
6. [Prepare Data For Modelling](#5)
    * 6.1 [Splitting Dependent/Independent Variables](#6.1)
    * 6.2 [PCA & Splitting Train/Test Sets](#6.2)
    * 6.3 [Scaling](#6.3)
7. [Model Definition](#7)
    * 7.1 [XGBoostClassifier](#7.1)
    * 7.2 [RandomForestClassifier](#7l.2)
    * 7.3 [Neural Networks](#7.3)
        * 7.3.1 [Model Development](#7.3.1)
        * 7.3.2 [Save Model](#7.3.2)

# 1. Connection to Kaggle
"""

from google.colab import userdata
import os

os.environ["KAGGLE_PASS"] = userdata.get('KAGGLE_PASS')
os.environ["KAGGLE_USERNAME"] = userdata.get('KAGGLE_USERNAME')

"""# 2. Downloading Dataset <a id=2></a>"""

!kaggle datasets download -d rabieelkharoua/alzheimers-disease-dataset

!unzip alzheimers-disease-dataset.zip

"""# 3. Import Libraries & Dataset <a id=3></a>"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# Import dataset
df = pd.read_csv("/content/alzheimers_disease_data.csv")

"""# 4. Dataset Basic Analysis <a id=4></a>

## 4.1 Getting to Know the Variables <a id=4.1></a>
"""

df.info()

"""| **Table of Contents**                  | **Details**                                                                                                                                                                |
|----------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Patient Information**                |                                                                                                                                                                             |
| Patient ID                             |                                                                                                                                                                             |
| **Demographic Details**                |                                                                                                                                                                             |
| Patient ID                             | PatientID: A unique identifier assigned to each patient (4751 to 6900).                                                                                                     |
| Age                                    | The age of the patients ranges from 60 to 90 years.                                                                                                                         |
| Gender                                 | Gender of the patients, where 0 represents Male and 1 represents Female.                                                                                                    |
| Ethnicity                              | The ethnicity of the patients, coded as follows:<br>0: Caucasian<br>1: African American<br>2: Asian<br>3: Other                                                             |
| EducationLevel                         | The education level of the patients, coded as follows:<br>0: None<br>1: High School<br>2: Bachelor's<br>3: Higher                                                           |
| **Lifestyle Factors**                  |                                                                                                                                                                             |
| BMI                                    | Body Mass Index of the patients, ranging from 15 to 40.                                                                                                                     |
| Smoking                                | Smoking status, where 0 indicates No and 1 indicates Yes.                                                                                                                   |
| AlcoholConsumption                     | Weekly alcohol consumption in units, ranging from 0 to 20.                                                                                                                  |
| PhysicalActivity                       | Weekly physical activity in hours, ranging from 0 to 10.                                                                                                                    |
| DietQuality                            | Diet quality score, ranging from 0 to 10.                                                                                                                                   |
| SleepQuality                           | Sleep quality score, ranging from 4 to 10.                                                                                                                                  |
| **Medical History**                    |                                                                                                                                                                             |
| FamilyHistoryAlzheimers                | Family history of Alzheimer's Disease, where 0 indicates No and 1 indicates Yes.                                                                                            |
| CardiovascularDisease                  | Presence of cardiovascular disease, where 0 indicates No and 1 indicates Yes.                                                                                               |
| Diabetes                               | Presence of diabetes, where 0 indicates No and 1 indicates Yes.                                                                                                             |
| Depression                             | Presence of depression, where 0 indicates No and 1 indicates Yes.                                                                                                           |
| HeadInjury                             | History of head injury, where 0 indicates No and 1 indicates Yes.                                                                                                           |
| Hypertension                           | Presence of hypertension, where 0 indicates No and 1 indicates Yes.                                                                                                         |
| **Clinical Measurements**              |                                                                                                                                                                             |
| SystolicBP                             | Systolic blood pressure, ranging from 90 to 180 mmHg.                                                                                                                       |
| DiastolicBP                            | Diastolic blood pressure, ranging from 60 to 120 mmHg.                                                                                                                      |
| CholesterolTotal                       | Total cholesterol levels, ranging from 150 to 300 mg/dL.                                                                                                                    |
| CholesterolLDL                         | Low-density lipoprotein cholesterol levels, ranging from 50 to 200 mg/dL.                                                                                                   |
| CholesterolHDL                         | High-density lipoprotein cholesterol levels, ranging from 20 to 100 mg/dL.                                                                                                  |
| CholesterolTriglycerides               | Triglycerides levels, ranging from 50 to 400 mg/dL.                                                                                                                         |
| **Cognitive and Functional Assessments**|                                                                                                                                                                             |
| MMSE                                   | Mini-Mental State Examination score, ranging from 0 to 30. Lower scores indicate cognitive impairment.                                                                      |
| FunctionalAssessment                   | Functional assessment score, ranging from 0 to 10. Lower scores indicate greater impairment.                                                                                |
| MemoryComplaints                       | Presence of memory complaints, where 0 indicates No and 1 indicates Yes.                                                                                                    |
| BehavioralProblems                     | Presence of behavioral problems, where 0 indicates No and 1 indicates Yes.                                                                                                  |
| ADL                                    | Activities of Daily Living score, ranging from 0 to 10. Lower scores indicate greater impairment.                                                                           |
| **Symptoms**                           |                                                                                                                                                                             |
| Confusion                              | Presence of confusion, where 0 indicates No and 1 indicates Yes.                                                                                                            |
| Disorientation                         | Presence of disorientation, where 0 indicates No and 1 indicates Yes.                                                                                                       |
| PersonalityChanges                     | Presence of personality changes, where 0 indicates No and 1 indicates Yes.                                                                                                  |
| DifficultyCompletingTasks              | Presence of difficulty completing tasks, where 0 indicates No and 1 indicates Yes.                                                                                          |
| Forgetfulness                          | Presence of forgetfulness, where 0 indicates No and 1 indicates Yes.                                                                                                        |
| **Diagnosis Information**              |                                                                                                                                                                             |
| Diagnosis                              | Diagnosis status for Alzheimer's Disease, where 0 indicates No and 1 indicates Yes.                                                                                         |
| **Confidential Information**           |                                                                                                                                                                             |
| DoctorInCharge                         | This column contains confidential information about the doctor in charge, with "XXXConfid" as the value for all patients.                                                   |

## 4.2 Datatypes <a id=4.2></a>
"""

df.dtypes

# Numeric Features
print(f"Number of Numeric Features: {len(df.select_dtypes(include=['int', 'float']).columns)}")
print("-"*50)
print(f"Numeric Feature's Name: \n{df.select_dtypes(include=['int', 'float']).columns}")

# Categorical Features
print(f"Number of Categorical Features: {len(df.select_dtypes(include=['object']).columns)}")
print("-"*50)
print(f"Categorical Feature's Name: \n{df.select_dtypes(include=['object']).columns}")

"""### 4.2.1 Drop DoctorInCharge <a id=4.2.1></a>"""

# As it is obiviously clear that DoctorInCharge variable does not provide
# Any insightful information, we can drop this variable.
df = df.drop(columns=['DoctorInCharge'], axis=1)
df.head()

"""### **NOTE**:
**There is only 1 Categorical feature with label of object in this dataset, but with further analysis we can simply understand that we ham some other categorical features , but their datatypes are "int". Such as "Gender", "Ethnicity", "Smoking", etc.**
"""

df.nunique()

"""## Missing Values & Duplicates <a id=4.3></a>"""

df.isnull().sum()

df.duplicated().sum()

"""## 4.4 Statistical Analysis <a id=4.4></a>"""

df.describe().T

"""- **PatientID:** Patient IDs range from 4751 to 6900.
- **Age:** Patients are aged between 60 and 90, with an average of 75 years.
- **Gender:** Nearly equal distribution between males and females.
- **Ethnicity:** Most patients are Caucasian, with a few African American, Asian, and other ethnicities.
- **EducationLevel:** Most patients have a high school or bachelor's degree.
- **BMI:** Ranges from 15 to 40, with an average of 27.7.
- **Smoking & AlcoholConsumption:** About 29% smoke; alcohol consumption averages 10 units/week.
- **PhysicalActivity & DietQuality:** Patients average about 5 hours of activity and a diet quality score of 5.
- **SleepQuality:** Average sleep quality score is 7.
- **Medical History:** Family history of Alzheimer's (~25%), cardiovascular disease (~14%), diabetes (~15%), depression (~20%), head injury (~9%), hypertension (~15%).
- **Blood Pressure & Cholesterol:** Average systolic BP is 134 mmHg, diastolic BP is 90 mmHg, total cholesterol is 225 mg/dL.
- **Cognitive/Functional Assessments:** MMSE average is 15; functional assessment averages 5.
- **Symptoms:** Confusion (~20%), memory complaints (~21%), and forgetfulness (~30%) are reported.
- **Diagnosis:** About 35% of patients are diagnosed with Alzheimer's.

## 4.5 Analyze On Diagnosis <a id=4.5></a>
"""

# Group by 'Diagnosis' and get the mean for all columns
mean_stats = df.groupby('Diagnosis').mean()

# Display result
mean_stats.to_csv("stats-by-diagnosis.csv")

"""#### **NOTE**:
**As there are lots of columns=, i have export grouped information to a csv file in order to check and analyze them better**
"""

df.groupby('Diagnosis').agg(['mean']).T

"""# 5. EDA <a id=5></a>

## 5.1 Seperating Variables <a id=5.1></a>
"""

categorical_features = ['Gender', 'Ethnicity', 'EducationLevel', 'Smoking',
'PhysicalActivity', 'DietQuality', 'SleepQuality', 'FamilyHistoryAlzheimers', 'CardiovascularDisease',
'Diabetes', 'Depression', 'HeadInjury', 'Hypertension',
'MemoryComplaints', 'BehavioralProblems', 'ADL', 'Confusion', 'Disorientation',
'PersonalityChanges', 'DifficultyCompletingTasks', 'Forgetfulness', 'Diagnosis']

numeric_features = [col for col in df.columns if col not in categorical_features]

print(f"Numeric Features: {len(numeric_features)}")
print("-"*50)
print(f"Categorical Features: {len(categorical_features)}")

"""## 5.2 Barplot <a id=5.2></a>"""

def countplot(col):
    plt.figure(figsize=(6, 5))
    sns.set_style("darkgrid")
    sns.countplot(data=df,
                x=col,
                palette='dark',
                width=0.5)
    plt.title(f"{col}'s Countplot",
              fontsize=14,
              weight="bold")
    plt.xlabel(col, fontsize=10)
    plt.ylabel("Count", fontsize=10)
    plt.show()

countplot("Gender")

countplot("Ethnicity")

countplot("EducationLevel")

countplot("Smoking")

countplot("FamilyHistoryAlzheimers")

countplot("CardiovascularDisease")

countplot("Diabetes")

countplot("Depression")

countplot("HeadInjury")

countplot("Hypertension")

countplot("MemoryComplaints")

countplot("BehavioralProblems")

countplot("Confusion")

countplot("Disorientation")

countplot("PersonalityChanges")

countplot("DifficultyCompletingTasks")

countplot("Forgetfulness")

countplot("Diagnosis")

"""## 5.3 Distributions <a id=5.3></a>"""

plt.figure(figsize=(15, 15))
sns.set_style('darkgrid')
for i, var in enumerate(numeric_features[1:], 1):
    plt.subplot(4, 3, i)
    sns.histplot(df[var],
                 bins=100,
                 kde=True,
                 color='royalblue',
                 edgecolor='black')
    plt.title(f"{var}'s Distribution",
              fontsize=14,
              weight="bold")
    plt.xlabel(var, fontsize=10)
    plt.ylabel("Density", fontsize=10)
plt.tight_layout()
plt.show()
plt.savefig('distributions.png')

"""## 5.4 Boxplot <a id=5.4></a>"""

plt.figure(figsize=(15, 15))
sns.set_style('darkgrid')
for i, var in enumerate(numeric_features[1:], 1):
    plt.subplot(4, 3, i)
    sns.boxplot(data= df,
                y=var,
                width=0.3)
    plt.title(f"{var}'s Boxplot",
              fontsize=14,
              weight="bold")
plt.tight_layout()
plt.show()

"""## Heatmap <a id=5.5></a>"""

# Calculate the correlation matrix
corr_matrix = df.corr()
# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

plt.figure(figsize=(20, 25))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="cubehelix", linewidths=0.5)
plt.title("Correlation Matrix with Upper Triangle Masked", fontsize=16, weight='bold')
plt.show()

"""# 6. Prepare Data For Modelling <a id=6></a>

# 6.1 Splitting Dependent/Independent Variables <a id=6.1></a>
"""

X = df.drop(['Diagnosis', 'PatientID'], axis=1).values
y = df['Diagnosis'].values

"""## 6.2 PCA & Splitting Train/Test Sets <a id=6.2></a>"""

from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split

pca = PCA(12)
X_pca = pca.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

print(f"X Train :{X_train.shape}")
print(f"X Test :{X_test.shape}")
print(f"y Train :{y_train.shape}")
print(f"y Test :{y_test.shape}")

"""## 6.3 Scaling <a id=6.3></a>"""

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""# 7. Model Definition <a id=7></a>"""

from sklearn.model_selection import cross_val_score, RandomizedSearchCV, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

"""## 7.1 XGBoost <a id=7.1></a>"""

# Model Object
xgb_model = XGBClassifier()

# Define the parameter grid
param_dist = {
    'n_estimators': [100, 200, 300, 400, 500],
    'learning_rate': [0.01, 0.1, 0.2, 0.3],
    'max_depth': [3, 4, 5, 6, 7],
    'min_child_weight': [1, 3, 5],
    'gamma': [0, 0.1, 0.2, 0.3],
    'subsample': [0.6, 0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.6, 0.7, 0.8, 0.9],
    'reg_alpha': [0, 0.01, 0.1, 1],
    'reg_lambda': [0, 0.01, 0.1, 1],
    'scale_pos_weight': [1, 2, 5]
}

# Create the RandomizedSearchCV object
random_search = RandomizedSearchCV(xgb_model,
                                   param_distributions=param_dist,
                                   n_iter=50,
                                   scoring='roc_auc',  # Use AUC-ROC for binary classification
                                   cv=5,
                                   verbose=2,
                                   random_state=42,
                                   n_jobs=-1)

# Fit the randomized search model on your dataset (X, y)
random_search.fit(X_train, y_train)

best_params = random_search.best_params_

# Create the final XGBClassifier model with the best parameters
xgb_tuned = XGBClassifier(**best_params, use_label_encoder=False, eval_metric='logloss')

# Train the final model on the full training data
xgb_tuned.fit(X_train, y_train)

# Make predictions on the test data
y_pred = xgb_tuned.predict(X_test)

# Get predicted probabilities (useful for ROC-AUC)
# y_pred_proba = xgb_tuned.predict_proba(X_test)[:, 1]

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)

"""## 7.2 Random Forest <a id=7.2></a>"""

# Define Model
rf_model = RandomForestClassifier()

# Define params for RandomizedSearch
params = {
    'n_estimators': [50, 100, 200, 300, 400, 500, 1000],
    'criterion': ['gini', 'entropy', 'log_loss'],
    'min_samples_split': [2, 5, 10, 15, 20],
    'min_samples_leaf': [1, 2, 4, 6, 8, 10],
    'min_weight_fraction_leaf': [0.0, 0.1, 0.2, 0.3, 0.4, 0.5],
    'max_features': ['auto', 'sqrt', 'log2', None],
    'max_leaf_nodes': [None, 10, 20, 30, 40, 50],
    'max_samples': [None, 0.5, 0.75, 1.0]}

# Create the RandomizedSearchCV object
rf_random_search = RandomizedSearchCV(rf_model,
                                   param_distributions=params,
                                   n_iter=50,
                                   scoring='roc_auc',
                                   cv=5,
                                   verbose=3,
                                   random_state=42,
                                   n_jobs=-1)

# Fit the randomized search model on your dataset (X, y)
rf_random_search.fit(X_train, y_train)

# Get best params from RandomizedSearch
best_param = rf_random_search.best_params_

# New RandomForest model
rf_tuned = RandomForestClassifier(**best_param)

# Training
rf_tuned.fit(X_train, y_train)

y_pred = rf_tuned.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print the results
print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)
print("Classification Report:")
print(class_report)

"""## 7.3 ANN <a id=7.3></a>"""

import tensorflow as tf

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"X Train :{X_train.shape}")
print(f"X Test :{X_test.shape}")
print(f"y Train :{y_train.shape}")
print(f"y Test :{y_test.shape}")

"""### 7.3.1 Model Definition <a id=7.3.1></a>"""

model = tf.keras.Sequential([
    tf.keras.layers.Dense(1024, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# Define early stop
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                              patience=30,
                                              restore_best_weights=True)

hist = model.fit(
    x = X_train,
    y = y_train,
    validation_data = (X_test, y_test),
    # callbacks = [early_stop],
    epochs = 100,
    batch_size = 64)

plt.plot(hist.history['accuracy'], label='Accuracy')
plt.plot(hist.history['val_accuracy'], label='Validation Accuracy')
plt.legend()

plt.plot(hist.history['loss'], label='Loss')
plt.plot(hist.history['val_loss'], label='Validation Loss')
plt.legend()

# Predict probabilities for the test set
y_pred_prob = model.predict(X_test)

# Convert predicted probabilities to class labels (0 or 1)
y_pred = np.round(y_pred_prob).astype(int)  # Rounding probabilities to get 0 or 1
# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Print the results
conf_matrix = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

class_report = classification_report(y_test, y_pred)
print("Classification Report:")
print(class_report)

"""# 7.3.2 Save Model <a id=7.2.2></a>"""

# Save pickle
import pickle

with open("model.pkl","wb") as file1:
  pickle.dump(model,file1)

# Save h5
model.save('ann.h5')


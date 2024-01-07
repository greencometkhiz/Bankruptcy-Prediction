# -*- coding: utf-8 -*-
"""dmfinalproject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1okoCHq6Cuv7R5qa2uFPQLLxHDxWvyrsz
"""

!pip install dataprep
!pip install imblearn

# Importing libraries required
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# import dataprep.eda as eda # EDA, Cleaning
from dataprep.eda import create_report

import seaborn as sns # Data visualization
import matplotlib.pyplot as plt # Data visualization

# Data analysis and ML Library
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.linear_model import Lasso # Lasso regression
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression # Logistic regression
from sklearn.svm import SVC # Support vector machine classifier
from sklearn.tree import DecisionTreeClassifier # Decision tree classifier
from sklearn.ensemble import RandomForestClassifier # Random forest classifier
from sklearn.naive_bayes import GaussianNB # Gaussian Naive Bayes
from sklearn.neighbors import KNeighborsClassifier# K Nearset Neighbors
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV,RandomizedSearchCV
from sklearn.metrics import roc_curve,roc_auc_score

# Handle Imbalanced dataset
from imblearn.over_sampling import SMOTE

# Print html elements
from IPython.display import Markdown

# Functions

# K-Fold Cross-Validation
# https://www.section.io/engineering-education/how-to-implement-k-fold-cross-validation/

from sklearn.model_selection import cross_validate

def cross_validation(model, _X, _y, _cv=5):
    _scoring = ['accuracy', 'precision', 'recall', 'f1']
    results = cross_validate(estimator=model,X=_X,y=_y,cv=_cv,scoring=_scoring,return_train_score=True)
    return {"Training Accuracy scores": results['train_accuracy'],
              "Mean Training Accuracy": results['train_accuracy'].mean()*100,
              "Training Precision scores": results['train_precision'],
              "Mean Training Precision": results['train_precision'].mean(),
              "Training Recall scores": results['train_recall'],
              "Mean Training Recall": results['train_recall'].mean(),
              "Training F1 scores": results['train_f1'],
              "Mean Training F1 Score": results['train_f1'].mean(),
              "Validation Accuracy scores": results['test_accuracy'],
              "Mean Validation Accuracy": results['test_accuracy'].mean()*100,
              "Validation Precision scores": results['test_precision'],
              "Mean Validation Precision": results['test_precision'].mean(),
              "Validation Recall scores": results['test_recall'],
              "Mean Validation Recall": results['test_recall'].mean(),
              "Validation F1 scores": results['test_f1'],
              "Mean Validation F1 Score": results['test_f1'].mean()
              }

# Print confusion matrix heatmap
def print_confusion_matrix(y_true,y_pred):

    cf_matrix = confusion_matrix(y_true,y_pred)

    group_names = ["True Neg","False Pos","False Neg","True Pos"]
    group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]
    group_percentages = ["{0:.2%}".format(value) for value in cf_matrix.flatten()/np.sum(cf_matrix)]

    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)

    plt.figure(figsize=(5, 5))
    sns.heatmap(cf_matrix, annot=labels, fmt="", cmap='Blues')
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

def plot_auc_roc_curve(model,X_test,y_test):
    pred_prob = model.predict_proba(X_test)

    # roc curve and auc score for model
    fpr, tpr, thresh = roc_curve(y_test, pred_prob[:,1], pos_label=1)
    auc_score = roc_auc_score(y_test, pred_prob[:,1])

    # roc curve for tpr = fpr (AUC = 0.5)
    random_probs = [0 for i in range(len(y_test))]
    p_fpr, p_tpr, _ = roc_curve(y_test, random_probs, pos_label=1)

    plt.rcParams["figure.figsize"] = (5,5)

    ax = plt.subplots()
    ax = sns.lineplot(x=p_fpr, y=p_tpr, color='r')
    ax = sns.lineplot(x=fpr, y=tpr, color='b',linestyle='dashed')
    ax.set(xlabel="False Positive Rate", ylabel="True Positive Rate")
    plt.text(0.5, -0.17, 'AUC Score : '+ str(round(auc_score,2)) , transform=plt.gca().transAxes, ha='center')
    plt.show()

# Print confusion matrix and performance metrics
def print_model_performance(model_name,model,X_test,y_test):

    display(Markdown("<h2> "+model_name+" </h2>"))
    y_pred = model.predict(X_test)

    display(Markdown("<h3> Classification report : </h3>"))
    print(classification_report(y_test,y_pred))

    display(Markdown("<h3> Confusion matrix : </h3>"))
    print_confusion_matrix(y_test,y_pred)

    display(Markdown("<h3> AUC-ROC Curve : </h3>"))
    plot_auc_roc_curve(model,X_test,y_test)

    display(Markdown("<br/>"))

company_df = pd.read_csv("/content/data.csv")

print("Number of Records : ",company_df.shape[0],"\nNumber of Features : ",company_df.shape[1])

company_df.columns = company_df.columns.str.strip()

company_df.head()

company_df.describe()

company_df.info()

duplicate_rows = company_df.duplicated()
print("Number of duplicated records :",len(company_df[duplicate_rows]))

# Lets check for the presence of missing values
missing_value_count = pd.DataFrame(company_df.isna().sum())
missing_value_count.columns = ["Count"]
print("Total number of columns with missing values :",len(missing_value_count[missing_value_count.Count > 0]))

pd.DataFrame(company_df['Net Income Flag'].value_counts()).plot.bar(y='Net Income Flag', rot=0)
plt.title("Net income flag distribution")
plt.show()
print("Net Income Flag Distribution\n")
print(pd.DataFrame(company_df['Net Income Flag'].value_counts()))

pd.DataFrame(company_df['Liability-Assets Flag'].value_counts()).plot.bar(y='Liability-Assets Flag', rot=0)
plt.title("Liability-Assets Flag distribution")
plt.show()
print("Liability-Assets Flag Distribution\n")
print(pd.DataFrame(company_df['Liability-Assets Flag'].value_counts()))

pd.DataFrame(company_df['Bankrupt?'].value_counts()).plot.bar(y='Bankrupt?', rot=0)
plt.title("Bankrupt distribution")
plt.show()
print("Bankrupt Distribution\n")
print(pd.DataFrame(company_df['Bankrupt?'].value_counts()))

# Observations on categorical data distribution:

# Net income flag value - Activated for 100% companies, so this column can be removed from EDA and Modelling steps
# Liability assets flag - Activated for 0.1% companies of total dataset
# Bankruptcy flag - This is our target variable, from the distribution we can observe the class imbalance (Needs to be treated before modelling)

# Too many columns to perform EDA
# In the bankruptcy data we have has 90+ columns. Carrying out EDA/Modelling on 90+ columns is a time and resource consuming process.
# The curse of dimensionality is like trying to find a single sock in a mountain of laundry. As the number of dimensions (socks) increases,
#  the chances of finding a match (meaningful patterns) become increasingly elusive and your search turns into a chaotic mess
# Lets narrow down our analysis to limited columns, so we will use pearson correlation to narrow down the number of columns based on linear relationships

# Columns with Linear relationship with Target variable
company_corr = pd.DataFrame(company_df.corr(numeric_only=True))
company_corr = pd.DataFrame(company_corr['Bankrupt?'])

# Remove specific indices, all 3 are categorical
indices_to_remove = ['Liability-Assets Flag', 'Net Income Flag','Bankrupt?']
company_corr = company_corr.drop(indices_to_remove)

plt.figure(figsize=(8, 17))
sns.barplot(y=company_corr.index,x=company_corr['Bankrupt?'])
plt.title("Pearson correllation with Bankruptcy")
plt.show()

# Lets see what features has weak correlation to strong correlation (>|0.10|)
temp_corr = company_corr
temp_corr[['Bankrupt?']] = abs(temp_corr[['Bankrupt?']])
print("\nColumns with correlation (>|0.10|) :\n")
for i in temp_corr[(temp_corr["Bankrupt?"] > 0.10)].index:
    print("* "+i+"\t")

# Select above mentioned features to find correlation between each other
correlated_features = list(temp_corr[(temp_corr["Bankrupt?"] > 0.10)].index)+["Bankrupt?"]
corr_test = company_df[correlated_features]

plt.figure(figsize=(15, 15))
corr = corr_test.corr()

sns.heatmap(corr,cmap="crest",annot=True, fmt=".1f")
plt.title("Correlation with Bankruptcy (|>0.10|)")
plt.show()

# Observations :

# Lets remove columns with correlation with other columns = 1.0, which means both the columns convey same information

# Columns selected based on Linear relationship
selected_columns_set_linear = [
 'ROA(A) before interest and % after tax',
 'Net Value Per Share (A)',
 'Debt ratio %',
 'Working Capital to Total Assets',
 'Current Liability to Current Assets',
 "Net Income to Stockholder's Equity",
 'Operating Gross Margin',
 'Bankrupt?']

plt.figure(figsize=(10, 10))
sns.heatmap(company_df[selected_columns_set_linear].corr(),cmap="crest",annot=True, fmt=".2f")
plt.title("Correlation between selected columns")
plt.show()

# We selected columns based on linear relationship with our target variable. In the next step we will use Mutual information to select columns based on Non linear relationship

# Columns with Non-Linear relationship with Target variable

independent_variable = company_df.drop(['Bankrupt?'], axis=1)
target_variable = company_df[['Bankrupt?']]

importances = mutual_info_classif(independent_variable,pd.Series.ravel(target_variable))
importances = pd.Series(importances,independent_variable.columns[0:len(independent_variable.columns)])
importances = pd.DataFrame({'features':importances.index, 'importance':importances.values})

# Mutual information
plt.figure(figsize=(10, 17))
sns.barplot(data = importances,y = "features", x = "importance",order=importances.sort_values('importance').features)
plt.xlabel("Mutual Importance")
plt.title("Mutual Importance of Columns")
plt.show()

# Lets select top 10 columns for EDA and Modelling
selected_columns_set_non_linear = np.array(importances.nlargest(5,'importance').features)

selected_columns = [*selected_columns_set_linear , *selected_columns_set_non_linear]
selected_columns = np.unique(selected_columns)

# Exploratory data analysis

bankruptcy_df = company_df[selected_columns]
bankruptcy_df.head()



bankruptcy_df.describe()

# Observations : All the columns are normalized, when we train our model we directly use the data without any normalization
#create_report(bankruptcy_df)

#All the columns which are selected using linear and non linear relationships are Continous variables
#There is a high correlation (|>0.7|) between columns, lets remove following columns :
#In the upcoming section, lets remove the highly correlated columns and see the distribution of data based Bankruptcy

cols_to_remove = [
    'Net Value Per Share (A)',
    'Net profit before tax/Paid-in capital',
    'Net Income to Stockholder\'s Equity',
    'Persistent EPS in the Last Four Seasons',
    'Per Share Net profit before tax (Yuan ¥)'
]

# Removing highly correlated columns
selected_columns_1 =[x for x in selected_columns if x not in cols_to_remove]
bankruptcy_df = bankruptcy_df[selected_columns_1]

plt.figure(figsize=(10, 10))
sns.heatmap(bankruptcy_df[selected_columns_1].corr(),cmap="crest",annot=True, fmt=".2f")
plt.title("Correlation between selected columns after removal")
plt.show()

# Scatter plot - Relationship between features with Bankruptcy hue
display(Markdown("<h3><center>Pair plot - All selected features<center/></h3><br/>"))
sns.pairplot(bankruptcy_df, hue='Bankrupt?',plot_kws={'alpha': 0.5})
plt.show()

# Box plot
plt.figure(figsize=(7, 7))
sns.boxplot(data=bankruptcy_df)
plt.xticks(rotation=90)
plt.title("Box plot - All columns")
plt.show()

#Fixing Imbalance dataset
# In the categorical data distribution analysis, we came to know that company which are
# bankrupted are very less compared to non bankrupt companies. Our dataset is a imbalanced dataset.


# Distribution of Target variable
class_dist = pd.DataFrame(bankruptcy_df['Bankrupt?'].value_counts())
class_dist['Bankrupt? %'] = round((class_dist['Bankrupt?']/sum(class_dist['Bankrupt?']))*100,2)
class_dist['Bankrupt? %'] = class_dist['Bankrupt? %'].apply(str)
class_dist['Bankrupt? %'] = class_dist['Bankrupt? %'] +"%"

print("Bankruptcy distribution :\n")
print(class_dist)

# Lets split features and target variable into X and y
X = bankruptcy_df.drop(['Bankrupt?'],axis=1)
y = bankruptcy_df['Bankrupt?']

# Lets oversample our dataset using SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)

# Before Oversampling using SMOTE
bankruptcy_df['Bankrupt?'].value_counts().plot(kind="bar")
plt.xlabel("Bankruptcy Flag")
plt.ylabel("Count")
plt.title("Before Oversampling")
plt.show()

# After Oversampling using SMOTE
y_res.value_counts().plot(kind="bar")
plt.xlabel("Bankruptcy Flag")
plt.ylabel("Count")
plt.title("After Oversampling using SMOTE")
plt.show()

bankruptcy_resampled_df = X_res.copy()
bankruptcy_resampled_df['Bankrupt?'] = y_res.copy()

# Scatter plot - Relationship between features with Bankruptcy hue after resampling
display(Markdown("<h3><center>Pair plot - All selected features after resampling<center/></h3><br/>"))
sns.pairplot(bankruptcy_resampled_df, hue='Bankrupt?',plot_kws={'alpha': 0.5})
plt.show()

# Modelling

# Split resampled data set to train and test samples
# 0.30 means 30 percent data will be used
X_train, X_test, y_train, y_test = train_test_split( X_res, y_res, test_size=0.30, random_state=42,stratify=y_res)

# Training following baseline models with default parameters

# Logistic regression
# SVM
# Decision tree
# Random forest
# Gaussian Naive Bayes
# K-Nearest Neighbors

# Creating base models
log_reg_model = LogisticRegression(random_state=42)
svm_model = SVC(random_state=42,probability=True)
decision_tree_model = DecisionTreeClassifier(random_state=42)
random_forest_model = RandomForestClassifier(random_state=42)
gaussian_nb_model = GaussianNB()
knn_model = KNeighborsClassifier()

# Hyperparameters of models




log_reg_params_L1 = {
    "solvers" : ['liblinear','saga'],
    "penalty" : ['l1'],
    "C" : [0.01,0.1,1.0,100,10]
}

log_reg_params_L2 = {
    "solvers" : ['newton-cg','liblinear','newton-cholesky','sag','saga'],
    "penalty" : ['l2'],
    "C" : [0.01,0.1,1.0,100,10]
}



svm_params = {
    'kernel': ['rbf', 'poly', 'sigmoid'],
    'C': [0.01,0.1,1.0,100,10],
    'gamma': [1, 0.1, 0.01, 0.001]
}



decision_tree_params = {
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_leaf': [5, 10, 20, 50, 100],
    'min_samples_split': [2, 5, 10],
    'criterion': ["gini", "entropy"],
    'max_features': ['auto', 'sqrt']
}



random_forest_params = {
    'n_estimators': [25,50,75,100],
    'max_depth': [2, 3, 5, 10, 20],
    'min_samples_leaf': [5, 10, 20, 50, 100],
    'min_samples_split': [2, 5, 10],
    'criterion': ["gini", "entropy"],
    'max_features': ['auto', 'sqrt'],
    'bootstrap': [True, False]
}


guassian_nb_params = {
    'var_smoothing': np.logspace(0,-9, num=100)
}



knn_params = {
    'n_neighbors' : [5,7,9,11,13,15],
    'weights' : ['uniform','distance']
}

# Training baseline models
log_reg_model.fit(X_train,y_train)
svm_model.fit(X_train,y_train)
decision_tree_model.fit(X_train,y_train)
random_forest_model.fit(X_train,y_train)
gaussian_nb_model.fit(X_train,y_train)
knn_model.fit(X_train,y_train)

# Performance of baseline models
display(Markdown("<h1>Performance of baseline models</h1><br/>"))
print_model_performance("1. Logistic regression",log_reg_model,X_test,y_test)
logisticaccuracy=0.86
print_model_performance("2. SVM",svm_model,X_test,y_test)
svmaccuracy=0.86
print_model_performance("3. Decision Tree",decision_tree_model,X_test,y_test)
decisiontreeaccuracy=0.93
print_model_performance("4. Random Forest",random_forest_model,X_test,y_test)
randomforestaccuracy=0.96
print_model_performance("5. Gaussian Naive Bayes",gaussian_nb_model,X_test,y_test)
gnbaccuracy=0.80
print_model_performance("6. K-Nearest Neighbours",knn_model,X_test,y_test)
knearestneighboraccuracy=0.94

#stacking algorithm

estimators = [
    ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
    ('knn', KNeighborsClassifier(n_neighbors=10)),
    ('gnb', GaussianNB()),
    ('dtc',DecisionTreeClassifier()),
    ('svvvc',SVC()),
    ('lreg',LogisticRegression())

]

from sklearn.ensemble import StackingClassifier
clf = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(),
    cv=11
)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy_score(y_test,y_pred)

import numpy as np
import matplotlib.pyplot as plt


# creating the dataset
fg = {'K_Nearest_Neighbor':knearestneighboraccuracy,'Gaussian Naive Bayes':gnbaccuracy,'SVM':svmaccuracy,'Decision_Tree':decisiontreeaccuracy, 'Random_Forest':randomforestaccuracy, 'Logistic_Regression':logisticaccuracy}
models = list(fg.keys())
tascore = list(fg.values())

fig = plt.figure(figsize = (10, 7))

# creating the bar plot
plt.bar(models, tascore, color ='red',
        width = 0.3)

plt.xlabel("Models")
plt.ylabel("Test Accuracy Score")
plt.title("Test Accuracy Score per Model")
plt.show()
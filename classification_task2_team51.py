# -*- coding: utf-8 -*-
"""Classification_Task2_Team51

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JMcfP2q_jtCxO6n8cFxYBJKzEhET0y-l

# Project setup

## Python modules import
"""

#import python modules
import pandas as pd
import numpy

from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest,f_classif,mutual_info_classif


from sklearn.model_selection import StratifiedShuffleSplit,train_test_split,KFold,cross_val_score

from sklearn.naive_bayes import MultinomialNB

from sklearn.svm import SVC


from sklearn.metrics import accuracy_score

# Google Drive
from google.colab import drive

drive.mount("/content/gdrive/", force_remount = True)
print("Established access to Google Drive")
DRIVE_PATH = "/content/gdrive/My Drive/Team51_DM_Task2/"

"""## Reading  CSV Files"""

#reading image file
image_file=pd.read_csv(DRIVE_PATH +"Images.csv",sep=";",skiprows=1,header=None,names=["imageID","imageclass"])
image_file.head()

#reading feature file
columnNames=["imageID"]
featurename="feature_{feature_no}"
for i in range(1,81):
    current_featurename=featurename.format(feature_no=i)
    columnNames.append(current_featurename)

print(columnNames)
feature_file=pd.read_csv(DRIVE_PATH +"EdgeHistogram.csv",sep=";",skiprows=1,header=None,names=columnNames)
feature_file.index = feature_file.index + 1
feature_file.head()

"""## Merging both CSV files data"""

image_and_features_together_df=pd.merge(image_file, feature_file, on='imageID')

#Defining two dataframes X and Y.
# Dataframe X: Contains all features
# Dataframe Y: Conatains all class labels
X=image_and_features_together_df.drop(['imageID','imageclass'],axis=1)
Y=image_and_features_together_df['imageclass']

"""# All Trials without Feature Engineering

## Selecting Best Features for using during Classification
"""

# Selecting 40 best features from 80
fs = SelectKBest(score_func=f_classif, k=40)
X_selected = fs.fit_transform(X,Y)
print(X_selected.shape)

"""## SVM Classifier"""

# Training with 3,5,10,15 samples for each class and with multiple splits from Dataset
model = SVC(kernel="poly")
trial_set=[3,5,10,15]
test_scores=[]
for no in trial_set:
    print("Building models with train sets for each class as ",no)
    sss = StratifiedShuffleSplit(n_splits=5, train_size = 101*no, random_state=0)
    print(sss.get_n_splits(X_selected, Y))
    for train_index, test_index in sss.split(X_selected, Y):
        X_train, X_test = X_selected[train_index], X_selected[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        print(len(Y_train.unique()))
        model.fit(X_train, Y_train)
        y_hat = model.predict(X_test)
        acc = accuracy_score(Y_test, y_hat)
        print('Accuracy: %.3f' % acc)
        print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
        print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))
        print('\n')
        test_scores.append(acc)
print("maximum accuracy for classification was",max(test_scores) )

# Only one split
model = SVC(kernel="poly")
X_train, X_test, Y_train, Y_test = train_test_split(X_selected, Y, stratify=Y)
# print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
# print(len(Y_train.unique()))
model.fit(X_train, Y_train)
y_hat = model.predict(X_test)
acc = accuracy_score(Y_test, y_hat)
print('Accuracy: %.3f' % acc)
print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))

# Training with entire dataset and best 40 features
model2 = SVC(kernel="poly")
model2.fit(X_selected,Y)
print("accuracy",model2.score(X_selected,Y))

# Training with entire dataset and all 80 features
model2 = SVC(kernel="poly")
model2.fit(X,Y)
print("accuracy",model2.score(X,Y))

"""## Naives Bayes Classifier"""

# Training with 3,5,10,15 samples for each class and with multiple splits from Dataset
model = MultinomialNB()
trial_set=[3,5,10,15]
test_scores=[]
for no in trial_set:
    print("Building models with train sets for each class as ",no)
    sss = StratifiedShuffleSplit(n_splits=5, train_size = 101*no, random_state=0)
    print(sss.get_n_splits(X_selected, Y))
    for train_index, test_index in sss.split(X_selected, Y):
        X_train, X_test = X_selected[train_index], X_selected[test_index]
        Y_train, Y_test = Y[train_index], Y[test_index]
        print(len(Y_train.unique()))
        model.fit(X_train, Y_train)
        y_hat = model.predict(X_test)
        acc = accuracy_score(Y_test, y_hat)
        print('Accuracy: %.3f' % acc)
        print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
        print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))
        print('\n')
        test_scores.append(acc)

print("maximum accuracy for classification was",max(test_scores) )

# Only one split
model = MultinomialNB()
X_train, X_test, Y_train, Y_test = train_test_split(X_selected, Y, stratify=Y)
# print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
# print(len(Y_train.unique()))
model.fit(X_train, Y_train)
y_hat = model.predict(X_test)
acc = accuracy_score(Y_test, y_hat)
print('Accuracy: %.3f' % acc)
print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))

# Training with entire dataset and with best 40 features
model = MultinomialNB()
model.fit(X_selected,Y)
print("Accuracy",model.score(X_selected,Y))

# Training with entire dataset along with all 80 features and not best 40features
model = MultinomialNB()
model.fit(X,Y)
print("Accuracy",model.score(X,Y))

"""# Feature Engineering

## function definitions and feature engineering to obtain features
"""

def get_features(list_columnNames,newFeatureColumnName):
    mergedFeatures=image_and_features_together_df[list_columnNames].copy()
    mergedFeatures[newFeatureColumnName]=mergedFeatures.values.tolist()
    mergedFeatures['imageID']=image_and_features_together_df['imageID'].copy()
    return mergedFeatures

def find_max(x):
    return max(x)

i=1
featurename="feature_{feature_no}"
finalFeatures=image_and_features_together_df['imageID']
# print(finalFeatures)
new_feature_no=1
while(i<=80):
    DF_listFeatures=pd.DataFrame()
    columnListToMerge=[featurename.format(feature_no=i),featurename.format(feature_no=i+1),featurename.format(feature_no=i+2),featurename.format(feature_no=i+3),featurename.format(feature_no=i+4)]
    newFeature="mergedFeature_{feature_no}"
    newFeatureColumnName=newFeature.format(feature_no=new_feature_no)
    DF_listFeatures=get_features(columnListToMerge,newFeatureColumnName)
    # print(DF_listFeatures)
    mergedWithOldFeatures=pd.merge(finalFeatures,DF_listFeatures,on='imageID')
    i=i+5
    new_feature_no=new_feature_no+1
    finalFeatures=mergedWithOldFeatures
    finalFeatures.drop(columns=columnListToMerge,axis=1,inplace=True)
    # print(finalFeatures)

print(finalFeatures)

finalFeatures.drop('imageID',axis=1,inplace=True)

for column in finalFeatures:
    finalFeatures[column] = finalFeatures[column].apply(find_max)

print(finalFeatures)

X=finalFeatures
Y=image_and_features_together_df['imageclass']

print("features are:\n")
print(X)
# print("classes are: \n")
# print(Y)

"""## SVM Classifier"""

model = SVC(kernel="poly")
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, stratify=Y)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
print(len(Y_train.unique()))
model.fit(X_train, Y_train)
yhat = model.predict(X_test)
acc = accuracy_score(Y_test, yhat)
print('Accuracy: %.3f' % acc)
print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))

# Training with entire dataset and all 16 features
model = SVC(kernel="poly")
model.fit(X,Y)
print("accuracy",model.score(X,Y))

"""## Naive Bayes Classifier"""

model = MultinomialNB()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, stratify=Y)
print(X_train.shape, X_test.shape, Y_train.shape, Y_test.shape)
print(len(Y_train.unique()))
model.fit(X_train, Y_train)
yhat = model.predict(X_test)
acc = accuracy_score(Y_test, yhat)
print('Accuracy: %.3f' % acc)
print('Training set score: {:.4f}'.format(model.score(X_train, Y_train)))
print('Test set score: {:.4f}'.format(model.score(X_test, Y_test)))

# Training with entire dataset along with all 16 features
model = MultinomialNB()
model.fit(X,Y)
print("Accuracy",model.score(X,Y))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.cross_validation import cross_val_score, cross_val_predict
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

#%% Read files in
data = pd.read_csv('../data/audio_embedding_10s.csv', index_col=0)
labels = pd.read_csv('../data/train.csv', index_col=0)
labels.index = labels.index.str.replace(".wav","") # removing the suffix of the file names. 

#%% transpose data and merging data with labels
data_T = data.transpose()
dataAll = data_T.join(labels, how="left")

X = data_T.values
Y, uniques = pd.factorize(dataAll["label"])
#%% Search for the best model parameter
parameters = {'max_depth':range(3,30)}
clf = GridSearchCV(tree.DecisionTreeClassifier(), parameters, n_jobs=4)
clf.fit(X=X, y=Y)
test_score, std = clf.cv_results_['mean_test_score'], clf.cv_results_['std_test_score']
tree_model = clf.best_estimator_
print (clf.best_score_, clf.best_params_) 

#%% K-fold validation accuracy
acc =[]
for k in range(3,11): 
    scores = cross_val_score(tree_model, X, Y, cv=k)
    print k,"cross Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
    acc.append([scores.mean(),k])
best_k = acc[acc.index(max(acc))][1]
#print best_k
#%% Predict with cross validation model
predictions = cross_val_predict(tree_model, X, Y, cv=best_k)
#%% Plot results
plt.figure()
plt.errorbar(range(3,30), test_score, yerr=std,fmt='o')
plt.title("Accuracy with differnt maximum depth")
plt.figure()
plt.plot(zip(*acc)[1], zip(*acc)[0])
plt.title('Accuracy of k-fold cross validation')
plt.ylim(0.3,0.4)
plt.xlabel("Number of k")
#%%
from sklearn.metrics import confusion_matrix
fused_matrix = confusion_matrix(Y,predictions)

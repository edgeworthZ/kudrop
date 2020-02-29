import numpy as np 
import pandas as pd 
from sklearn import preprocessing
#import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.feature_selection import RFECV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score 
from sklearn.metrics import confusion_matrix, precision_recall_curve, roc_curve, auc, log_loss
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.pipeline import Pipeline

class LogisReg:
    def __init__(self):
        self.train_df = None
        self.test_df = None
        self.final_train = None
        self.final_test = None
        self.X = None
        self.y = None
        self.Selected_features = None
        self.submission = None
        
        #sns.set(style="white") #white background style for seaborn plots
        #sns.set(style="whitegrid", color_codes=True)

        # Read CSV train data file into DataFrame
        #train_df = pd.read_csv("input/train_female_fail.csv")

        # Read CSV test data file into DataFrame
        #test_df = pd.read_csv("input/test.csv")

    def setTrainFile(self, directory):
        self.train_df = pd.read_csv(directory)
        #create categorical variables and drop some variables
        train_data = self.train_df.copy()
        training=pd.get_dummies(train_data, columns=["Sex"])
        training.drop('Sex_female', axis=1, inplace=True)
        self.final_train = training
        self.final_train['IsMinor']=np.where(self.final_train['MidTerm']>=60, 1, 0)

    def setTestFile(self, directory):
        self.test_df = pd.read_csv(directory)
        self.test_df['IsMinor']=np.where(self.test_df['MidTerm']>=60, 1, 0)
        test_data = self.test_df.copy()
        testing = pd.get_dummies(test_data, columns=["Sex"])
        testing.drop('Sex_female', axis=1, inplace=True)
        self.final_test = testing

    def analyzeTrainData(self):
        cols = ["Age","MidTerm","Sex_male","IsMinor"] 
        self.X = self.final_train[cols]
        self.y = self.final_train['Grade']
        # Build a logreg and compute the feature importances
        model = LogisticRegression()
        # create the RFE model and select 4 attributes
        rfe = RFE(model, 4)
        rfe = rfe.fit(self.X, self.y)
        # summarize the selection of the attributes
        print('Selected features: %s' % list(self.X.columns[rfe.support_]))

        # Create the RFE object and compute a cross-validated score.
        # The "accuracy" scoring is proportional to the number of correct classifications
        rfecv = RFECV(estimator=LogisticRegression(), step=1, cv=10, scoring='accuracy')
        rfecv.fit(self.X, self.y)

        print("Optimal number of features: %d" % rfecv.n_features_)
        print('Selected features: %s' % list(self.X.columns[rfecv.support_]))

        self.Selected_features = ["Sex_male","Age","MidTerm","IsMinor"] 
        self.X = self.final_train[self.Selected_features]

        # 10-fold cross-validation logistic regression
        logreg = LogisticRegression()
        # Use cross_val_score function
        # We are passing the entirety of self.X and self.y, not self.X_train or self.y_train, it takes care of splitting the data
        # cv=10 for 10 folds
        # scoring = {'accuracy', 'neg_log_loss', 'roc_auc'} for evaluation metric - althought they are many
        scores_accuracy = cross_val_score(logreg, self.X, self.y, cv=10, scoring='accuracy')
        scores_log_loss = cross_val_score(logreg, self.X, self.y, cv=10, scoring='neg_log_loss')
        scores_auc = cross_val_score(logreg, self.X, self.y, cv=10, scoring='roc_auc')
        print('K-fold cross-validation results:')
        print(logreg.__class__.__name__+" average accuracy is %2.3f" % scores_accuracy.mean())
        print(logreg.__class__.__name__+" average log_loss is %2.3f" % -scores_log_loss.mean())
        print(logreg.__class__.__name__+" average auc is %2.3f" % scores_auc.mean())
        return scores_auc.mean()

    def analyzeTestData(self):
        #Define simple model
        ###############################################################################
        C = np.arange(1e-05, 5.5, 0.1)
        scoring = {'Accuracy': 'accuracy', 'AUC': 'roc_auc', 'Log_loss': 'neg_log_loss'}
        log_reg = LogisticRegression()

        #Simple pre-processing estimators
        ###############################################################################
        std_scale = StandardScaler(with_mean=False, with_std=False)
        #std_scale = StandardScaler()

        #Defining the CV method: Using the Repeated Stratified K Fold
        ###############################################################################

        n_folds=5
        n_repeats=5

        rskfold = RepeatedStratifiedKFold(n_splits=n_folds, n_repeats=n_repeats, random_state=2)

        #Creating simple pipeline and defining the gridsearch
        ###############################################################################

        log_clf_pipe = Pipeline(steps=[('scale',std_scale), ('clf',log_reg)])

        log_clf = GridSearchCV(estimator=log_clf_pipe, cv=rskfold,
                      scoring=scoring, return_train_score=True,
                      param_grid=dict(clf__C=C), refit='Accuracy')

        log_clf.fit(self.X, self.y)
        results = log_clf.cv_results_

        self.final_test['Grade'] = log_clf.predict(self.final_test[self.Selected_features])
        self.final_test['Name'] = self.test_df['Name']
        self.final_test['MidTerm'] = self.test_df['MidTerm']
        self.submission = self.final_test[['Name','MidTerm','Grade']]
        
    def export2CSV(self,directory):
        #self.submission.to_csv("submission.csv", index=False)
        self.submission.to_csv(directory, index=False)

    def getTestAnalyzeResult(self):
        #print(self.submission.tail())
        res = self.submission.to_string()
        return res

    def getSubmission(self):
        return self.submission

"""
lo = LogisReg()
lo.setTrainFile("input/train_female_fail.csv")
lo.setTestFile("input/test.csv")
lo.analyzeTrainData()
lo.analyzeTestData()
txt = lo.getTestAnalyzeResult()
print(txt)
"""

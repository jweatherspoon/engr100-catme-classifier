import numpy as np 
import preprocess 

import pickle

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import GridSearchCV

def get_pipeline():
    return Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MLPClassifier(solver='lbfgs'))
    ])

def get_data():
    with open('training_data', 'rb') as f:
        return pickle.loads(f.read())

def get_split_accuracies(rs, X, y, pipeline):
    accuracies = []
    for train, test in rs.split(X):
        tsd = np.array([X[i] for i in test])
        tsl = np.array([y[i] for i in test])
        score = pipeline.score(tsd, tsl)
        accuracies.append({
            'score': score, 
            'indices': test
        })
    return np.array(accuracies)

def grid_search_cv(X, y):
    param_grid = {
        'activation': ['relu', 'tanh'],
        'hidden_layer_sizes': [
            (5, 2),
            (100,),
            (100,10),
            (1000, 50)
        ],
        'early_stopping': [True, False],
    }

    tv = TfidfVectorizer()
    tv.fit(X)
    XT = tv.transform(X)

    grid_search = GridSearchCV(MLPClassifier(solver='lbfgs'), param_grid, verbose=1e99, cv=5, n_jobs=-1)
    grid_search.fit(XT, y)

    return grid_search


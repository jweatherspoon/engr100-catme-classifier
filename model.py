import numpy as np 
import preprocess 

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm

def get_pipeline():
    return Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', svm.SVC())
    ])
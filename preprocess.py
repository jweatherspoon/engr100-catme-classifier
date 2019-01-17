import argparse 
import sys 
import numpy as np 
import string 
import pickle

import csv 
from functools import reduce 

def row_empty(row):
    mask = [cell == '' for cell in row]
    return reduce(lambda a, b: a and b, mask)

def parse_raw_catme_file(filename):
    comment_data = []
    section_found = False 

    target_row = ['Student', 'Team', 'Section', 'Comment']
    with open(filename, 'r') as csvfile:
        parser = csv.reader(csvfile)
        for row in parser:
            if not section_found:
                if row[0:4] == target_row:
                    section_found = True 
            elif not row_empty(row):
                comment_data.append({
                    'student': row[0],
                    'team': row[1],
                    'section': row[2],
                    'comment': row[3]
                })
            else:
                break 
        
    return np.array(comment_data)

def get_comments(comment_data):
    table = str.maketrans(dict.fromkeys(string.punctuation + string.digits))
    comments = [c['comment'].translate(table).lower() for c in comment_data]
    return np.array(comments)

def process_arguments():
    """ Process the command line arguments when this script is called from the terminal. """
    parser = argparse.ArgumentParser(description="Data preprocessor for ENGR CatMe data.")
    parser.add_argument("-i", dest="infile", type=str, required=True,
        help="The name of the input *.CSV file.")
    parser.add_argument("-o", dest="outfile", type=str, required=False,
        help="The name of the output file.")
    return parser.parse_args()

def parse_csv(contents):
    lines = contents.split('\n')
    # Get all but the first row
    results = [line.strip().split(',') for line in lines]
    results = np.array(results[1:])

    # Map all punctuation to none and set to lower for all words in X
    table = str.maketrans(dict.fromkeys(string.punctuation + string.digits))
    X = results[:,0]
    X = np.array([x.translate(table).lower() for x in X])
    y = results[:,1].astype(int)
    return X, y


def read_csv(filename):
    if filename[-1:] == '.':
        filename += 'csv'
    elif filename[-4:] != '.csv':
        filename += '.csv'
    f = open(filename)
    contents = f.read()
    f.close()
    return contents

if __name__ == "__main__":
    with open('training_data', 'rb') as f:
        X, y = pickle.loads(f.read())
    

    
    
    

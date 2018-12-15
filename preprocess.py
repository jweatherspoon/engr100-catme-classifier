import argparse 
import sys 
import numpy as np 
import string 

def process_arguments(src=sys.argv):
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
    args = process_arguments()
    contents = read_csv(args.infile)
    X, y = parse_csv(contents)
    print(X[0])
    
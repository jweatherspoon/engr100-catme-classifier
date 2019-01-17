import easygui
import pickle
import numpy as np 

import preprocess
import csv 

if __name__ == "__main__":
    # Ask the user to supply a csv file 
    catme_file = easygui.fileopenbox(
        "Choose a CATME CSV file", default="\*.csv", filetypes=["\*.csv"])

    # Parse CSV data 
    comment_data = preprocess.parse_raw_catme_file(catme_file)

    # Open the pipeline and use it to classify the data 
    with open('models/pipeline', 'rb') as fin:
        pipeline = pickle.loads(fin.read())

    # TODO: Error checking for improper data
    comments = preprocess.get_comments(comment_data)
    predictions = pipeline.predict(comments)
    mask = (predictions + 1).astype(bool)

    # Rewrite the negative comments to a file 
    negatives = comment_data[mask]

    save_file = easygui.filesavebox("Save file", default="complaints.csv", filetypes=["\*.csv"])

    # TODO: Error checking for user cancel

    with open(save_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student','Team','Section','Comment'])
        for row in negatives:
            writer.writerow(row.values())
    
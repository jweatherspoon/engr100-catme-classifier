import easygui
import pickle
import numpy as np 

import preprocess
import csv 
from datetime import datetime 
import os 

OUTPUT_DIRECTORY = "output"

def save_file(filename, comments):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Student', 'Team', 'Section', 'Comment'])
        for row in comments:
            writer.writerow(row.values())

if __name__ == "__main__":
    # Ask the user to supply a csv file 
    catme_file = easygui.fileopenbox(
        "Choose a CATME CSV file", default="\*.csv", filetypes=["\*.csv"])

    # Parse CSV data 
    comment_data = preprocess.parse_raw_catme_file(catme_file)

    # Open the pipeline and use it to classify the data 
    with open('models/pipeline', 'rb') as fin:
        pipeline = pickle.loads(fin.read())

    comments = preprocess.get_comments(comment_data)
    predictions = pipeline.predict(comments)

    complaints_mask = (predictions + 1).astype(bool)
    neutral_mask = (predictions - 1).astype(bool)

    # Rewrite the negative comments to a file 
    complaints = comment_data[complaints_mask]
    neutral = filter(lambda x: x['comment'] != '', comment_data[neutral_mask])

    if not (os.path.exists(OUTPUT_DIRECTORY) and os.path.isdir(OUTPUT_DIRECTORY)):
        os.mkdir(OUTPUT_DIRECTORY)

    file_base = datetime.now().strftime('%F')
    output_file_base = f"{OUTPUT_DIRECTORY}/{file_base}"
    complaints_filename = f"{output_file_base}-complaints.csv"
    neutral_filename = f"{output_file_base}-neutral.csv"

    save_file(complaints_filename, complaints)
    save_file(neutral_filename, neutral)

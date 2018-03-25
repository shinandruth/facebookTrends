import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from math import *

interval = 5
name = "1min_test"
filename = "jaccard" + name
time_diff = 1

def compute_jaccard(user1_vals, user2_vals):
    intersection = user1_vals.intersection(user2_vals)
    union = user1_vals.union(user2_vals)
    jaccard = len(intersection)/float(len(union))
    return jaccard

def get_avg():
    df = pd.read_csv(os.path.join("CSV//", name+".csv"))
    total_run = df.scrapeid.max()
    curr = 0
    s = 0
    similarity = []
    for n in range(int((total_run+1)/2)):
        prev = curr
        curr = (df.loc[df["scrapeid"] == n, "title"]).drop_duplicates().values.tolist()
        if prev != 0:
            similarity.append(compute_jaccard(set(prev), set(curr)))
    for val in similarity:
        s += val
    avg = s / len(similarity)
    return avg

def create_input(avg):
    l = []
    l.append(name)
    l.append(interval)
    l.append(avg)
    return l

def plot():
    df = pd.read_csv(os.path.join("CSV//", filename+".csv"))
    ax = df.plot.bar(title="jaccard similarity", x='interval', y='avg', legend=True)
    fig = ax.get_figure()
    #plt.show()
    fig.savefig("..//selenium_env//graphs//"+filename+".png")

# 
# def interval_csv(input_filepath):
#     output_data = []
#     line = 2
#     scrapeid = 0
#     with open(input_filepath, output_filepath) as csv_file:
#         reader = csv.reader(csv_file)
#         start_time = reader[line][8]
#         for row in reader:
#             curr_scrapeid = reader[row][7]
#             if scrapid != curr_scrapeid:
#                 string_date = row[8]
#                 csv_date = datetime.datetime.strptime(string_date, "%c")
#                 if start_time + datetime.timedelta(mintues=time_diff)

if __name__ == "__main__":
    avg = get_avg()
    i = create_input(avg)
    with open(filename+".csv", "a", encoding="utf-8",  newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "interval", "avg"]) #Scrap ID
        writer.writerow(i)
    plot()

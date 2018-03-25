import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from math import *

#--------------CHANGE HERE ---------------------
interval = 1
name = "1min_test"
filename = "jaccard_" + name
time_interval_filename = filename + "_by" + str(interval) + "min"
#--------------CHANGE END HERE-----------------

def compute_jaccard(user1_vals, user2_vals):
    intersection = user1_vals.intersection(user2_vals)
    union = user1_vals.union(user2_vals)
    jaccard = len(intersection)/float(len(union))
    return jaccard


def get_avg():
    df = pd.read_csv(os.path.join("CSV//", time_interval_filename+".csv"))
    id = 0
    t = 0
    curr = []
    similarity = []
    max_id = df.scrapeid.max()
    while id < max_id:
        prev = curr
        curr = (df.loc[df["scrapeid"] == id, "title"]).drop_duplicates().values.tolist()
        if prev != 0:
            similarity.append(compute_jaccard(set(prev), set(curr)))
        if id == 0:
            id += interval - 1
        else:
            id += interval
    for val in similarity:
        t += val
    avg = t / len(similarity)
    return avg


# def get_avg():
#     df = pd.read_csv(os.path.join("CSV//", time_interval_filename+".csv"))
#     total_run = df.scrapeid.max() / interval
#     curr = 0
#     s = 0
#     similarity = []
#     for n in range(int((total_run+1)/2)):
#         prev = curr
#         curr = (df.loc[df["scrapeid"] == n, "title"]).drop_duplicates().values.tolist()
#         print("prev:", prev)
#         print("curr:", curr)
#         if prev != 0:
#             similarity.append(compute_jaccard(set(prev), set(curr)))
#     for val in similarity:
#         s += val
#     avg = s / len(similarity)
#     return avg

def create_input(avg):
    l = []
    l.append(name)
    l.append(interval)
    l.append(avg)
    return l

def plot():
    df = pd.read_csv(os.path.join("jaccard_CSV//", filename+".csv"))
    ax = df.plot.bar(title="How Often does FB Trends Change?", x='interval', y='avg', legend=True)
    y = df['avg']
    ax.set_ylabel("Jaccard Similarity")
    ax.set_xlabel("Intervals")
    # for i, v in enumerate(y):
    #     ax.text(v, i, str(v), color='blue', fontweight='bold')
    fig = ax.get_figure()
    fig.savefig("..//selenium_env//graphs//"+time_interval_filename+".png")

def create_csv():
    output_data = []
    firstline = True
    scrapeid = 0
    with open("CSV//"+name+".csv", "r", encoding="utf-8") as readfile,  open("CSV//"+time_interval_filename+".csv", "a", encoding="utf-8",  newline="") as writefile:
        reader = csv.reader(readfile)
        writer = csv.writer(writefile)
        writer.writerow(["type", "title", "description", "source", "uniquelink", "rank", "scrapeid", "timestamp"])
        #writer.writerow(["name", "interval", "average"])
        for row in reader:
            if firstline:
                firstline = False
                continue
            curr_scrapeid = row[6]
            if scrapeid == int(curr_scrapeid):
                writer.writerow(row)
            elif int(curr_scrapeid) > scrapeid:
                if scrapeid == 0:
                    scrapeid += interval - 1
                else:
                    scrapeid += interval

if __name__ == "__main__":
    # avg = get_avg()
    # i = create_input(avg)
    # Create interval csv files
    # create_csv()
    # with open("jaccard_CSV//"+filename+".csv", "a", encoding="utf-8",  newline="") as f:
    #     writer = csv.writer(f)
    #     #writer.writerow(["name", "interval", "avg"]) #Scrap ID
    #     writer.writerow(i)
    plot()

import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from math import *

#--------------CHANGE HERE ---------------------
interval = 5
name = "1min_test"
filename = "jaccard" + name + "-test"
time_interval_filename = name + "_" + str(interval)
#--------------CHANGE END HERE-----------------

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


def create_csv():
    output_data = []
    firstline = True
    scrapeid = 0
    with open("CSV//"+name+".csv", "r", encoding="utf-8") as readfile,  open(filename+".csv", "a", encoding="utf-8",  newline="") as writefile:
        reader = csv.reader(readfile)
        writer = csv.writer(writefile)
        #writer.writerow(["name", "interval", "average"])
        for row in reader:
            if firstline:
                firstline = False
                continue
            curr_scrapeid = row[6]
            print("curr:", curr_scrapeid, "set:", scrapeid)
            if scrapeid == int(curr_scrapeid):
                writer.writerow(row)
            elif int(curr_scrapeid) > scrapeid:
                if scrapeid == 0:
                    scrapeid += interval - 1
                else:
                    scrapeid += interval

if __name__ == "__main__":
    #avg = get_avg()
    #i = create_input(avg)
    create_csv()
    # with open(filename+".csv", "a", encoding="utf-8",  newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(["name", "interval", "avg"]) #Scrap ID
    #     writer.writerow(i)
    #plot()

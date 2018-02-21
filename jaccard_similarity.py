import csv
import pandas as pd
import os
# import matplotlib.pyplot as plt

from math import *

interval = 5
name = "60m_by_5m"
filename = "jaccard_avg"

def compute_jaccard(user1_vals, user2_vals):
    intersection = user1_vals.intersection(user2_vals)
    union = user1_vals.union(user2_vals)
    jaccard = len(intersection)/float(len(union))
    return jaccard

def get_avg():
    df = pd.read_csv(os.path.join("CSV//", name+".csv"))
    unq_link = df.uniqueLink
    total_run = df.scrapeId.max()
    curr = 0
    s = 0
    similarity = []
    for n in range(total_run+1):
        prev = curr
        curr = (df.loc[df["scrapeId"] == n, "title"]).drop_duplicates().values.tolist()
        if prev != 0:
            print(len(prev), len(curr))
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
if __name__ == "__main__":
    avg = get_avg()
    i = create_input(avg)
    with open(filename+".csv", "a", encoding="utf-8",  newline="") as f:
        writer = csv.writer(f)
        writer.writerow(i)

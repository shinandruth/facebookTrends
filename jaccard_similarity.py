import csv
import pandas as pd
import os

from math import *

name = "60m_by_10m"


def compute_jaccard(user1_vals, user2_vals):
    intersection = user1_vals.intersection(user2_vals)
    union = user1_vals.union(user2_vals)
    jaccard = len(intersection)/float(len(union))
    return jaccard


def conduct_jaccard():
    df = pd.read_csv(os.path.join("CSV//", name+".csv"))
    unq_link = df.uniqueLink
    total_run = df.scrapeId.max()
    curr = 0
    similarity = []
    for n in range(total_run+1):
        prev = curr
        curr = (df.loc[df["scrapeId"] == n, "title"]).drop_duplicates().values.tolist()
        if prev != 0:
            print(len(prev), len(curr))
            similarity.append(compute_jaccard(set(prev), set(curr)))
    return similarity


if __name__ == "__main__":
    print(conduct_jaccard())

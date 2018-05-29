import csv
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from math import *

#--------------CHANGE HERE ---------------------
interval = 5
name = "trends_db"
filename = name
time_interval_filename = filename + "_by" + str(interval) + "min"
_type = ["Top Trends", "Politics", "Science and Technology", "Sports", "Entertainment"]
cumulative_new_trends = 0
path = "CSV//Data for Thesis//Trends//"
#--------------CHANGE END HERE-----------------

def compute_jaccard(user1_vals, user2_vals):
    intersection = user1_vals.intersection(user2_vals)
    union = user1_vals.union(user2_vals)
    jaccard = len(intersection)/float(len(union))
    return jaccard

def get_new_trends(x, type):
    df = pd.read_csv(os.path.join(path, name+".csv"))
    id, num_of_new_trends = 0, 0
    trends, ans = [], []
    max_id = df.scrapeid.max()
    while id < max_id:
        print(id)
        _curr = (df.loc[(df["scrapeid"] == id) & (df["type"] == type)])
        trends.append((_curr.loc[(_curr["type"] == type, "title")]).values.tolist())
        if id == 0:
            id += x - 1
        else:
            id += x
    flat_curr = [item for sublist in trends for item in sublist]
    num_of_new_trends = len(set(flat_curr))
    if type == "Science and Technology":
        ans.append("Science/Tech")
    else:
        ans.append(type)
    ans.append(x)
    ans.append(num_of_new_trends)
    return ans

def get_avg_min_max_sd(x, type):
    df = pd.read_csv(os.path.join(path, name+".csv"))
    id = 0
    t = 0
    first = False
    curr = []
    similarity = []
    max_id = df.scrapeid.max()
    while int(id) < int(max_id):
        print(id)
        prev = curr
        _curr = (df.loc[(df["scrapeid"] == id) & (df["type"] == type)]).drop_duplicates()
        curr = (_curr.loc[(_curr["type"] == type, "title")]).values.tolist()
        if first:
            similarity.append(compute_jaccard(set(prev), set(curr)))
        first = True
        if id == 0:
            id += x - 1
        else:
            id += x
    for val in similarity:
        t += val
    if len(similarity) == 0:
        avg =  t
    else:
        avg = t / len(similarity)
    sm = min(similarity)
    lg = max(similarity)
    sd = get_sd(avg, similarity)
    return avg, sm, lg, sd

def get_sd(avg, arr):
    sq = []
    sum = 0
    for j in arr:
        sq.append((j - avg)**2)
        sum += j
    avg = sum / len(arr)
    return sqrt(avg)

def create_input(avg, sm, lg, sd, x, type):
    l = []
    l.append(name)
    l.append(x)
    l.append(avg)
    l.append(sm)
    l.append(lg)
    l.append(sd)
    if type == "Science and Technology":
        l.append("Science/Tech")
    else:
        l.append(type)
    return l

def create_csv_for_one_min_data():
    output_data = []
    firstline = True
    scrapeid = 0
    with open(path+name+".csv", "r", encoding="utf-8") as readfile,  open("jaccard_CSV//"+time_interval_filename+".csv", "a", encoding="utf-8",  newline="") as writefile:
        reader = csv.reader(readfile)
        writer = csv.writer(writefile)
        writer.writerow(["Type", "Title", "description", "source", "uniquelink", "rank", "scrapeid", "timestamp"])
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

def compare_similarities_of_two_csv(csv1, csv2):
    df1 = pd.read_csv(os.path.join(path, csv1+".csv"))
    df2 = pd.read_csv(os.path.join(path, csv2+".csv"))
    f1 = df1.Title.values.tolist()
    f2 = df2.Title.values.tolist()
    print("total similar:", len([i for i, j in zip(f1,f2) if i == j]), "len of 1: ", len(f1), "len of 2: ", len(f2))

def compare_similarities_of_two_csv_total(csv1, csv2):
    l = []
    df1 = pd.read_csv(os.path.join(path, csv1+".csv"))
    df2 = pd.read_csv(os.path.join(path, csv2+".csv"))
    f1 = df1.Title.values.tolist()
    f2 = df2.Title.values.tolist()
    l.append(len(f1))
    l.append(len(f2))
    l.append(len(set(f1)))
    l.append(len(set(f1)))
    l.append(len(set(f1) & set(f2)))
    return l

def compare_similarities_of_two_csv_per_topic(csv1, csv2, type):
    l = []
    df1 = pd.read_csv(os.path.join(path, csv1+".csv"))
    df2 = pd.read_csv(os.path.join(path, csv2+".csv"))
    f1 = df1.loc[(df1["type"] == type), "title"].values.tolist()
    f2 = df2.loc[(df2["type"] == type), "title"].values.tolist()
    l.append(len(f1))
    l.append(len(f2))
    l.append(len(set(f1)))
    l.append(len(set(f2)))
    print(set(f1).symmetric_difference(set(f2)))
    l.append(len(set(f1) & set(f2)))
    l.append(type)
    return l
def test(csv1):
    df1 = pd.read_csv(os.path.join(path, csv1+".csv"))
    f1 = df1.loc[(df1["type"] == "Science and Technology"), "title"].values.tolist()
    print(set(f1))


if __name__ == "__main__":
    #If you want to divide up the data by time intervals
    #create_csv_for_one_min_data()

    #get avg, min, max, sd for specific time interval
    for type in _type:
        for x in range(5, 65 ,5):
            avg, sm, lg, sd = get_avg_min_max_sd(x, type)
            i = create_input(avg, sm, lg, sd, x, type)
            with open("jaccard_CSV//"+filename+"_avg_min_max_sd5"+".csv", "a", encoding="utf-8",  newline="") as f:
                 writer = csv.writer(f)
                 if x == 5 and type == "Top Trends":
                     writer.writerow(["Name", "Interval", "Avg", "Min", "Max", "Standard Deviation"]) #Scrap ID
                 writer.writerow(i)


    #Get the cumulative new trends
    for type in _type:
        for x in range(5, 65, 5):
            j = get_new_trends(x, type)
            with open("jaccard_CSV//"+filename+"_Cumulative_New_Trends5"+".csv", "a", encoding="utf-8",  newline="") as f:
                 writer = csv.writer(f)
                 if x == 5 and type == "Top Trends":
                     writer.writerow(["Type", "Interval", "New Trends"])
                 writer.writerow(j)

    #get avg, min, max sd for ONE MIN
    # for type in _type:
    #     avg, sm, lg, sd = get_avg_min_max_sd(1, type)
    #     i = create_input(avg, sm, lg, sd, 1, type)
    #     with open("jaccard_CSV//"+filename+"_avg_min_max_sd"+".csv", "a", encoding="utf-8",  newline="") as f:
    #         writer = csv.writer(f)
    #         if type == "Top Trends":
    #             writer.writerow(["Name", "Interval", "Avg", "Min", "Max", "Standard Deviation"]) #Scrap ID
    #         writer.writerow(i)
    #
    # #Get cumulative news for ONE min
    # for type in _type:
    #     j = get_new_trends(1, type)
    #     with open("jaccard_CSV//"+filename+"_Cumulative_New_Trends"+".csv", "a", encoding="utf-8",  newline="") as f:
    #          writer = csv.writer(f)
    #          if type == "Top Trends":
    #              writer.writerow(["Type", "Interval", "New Trends"])
    #          writer.writerow(j)
    # Get num of similar trends of two csv files`
    # with open("jaccard_CSV//"+filename+".csv", "a", encoding="utf-8",  newline="") as f:
    #     writer = csv.writer(f)
    #     # j = compare_similarities_of_two_csv_total("personal","puppet")
    #     # writer.writerow(["Total Trends in Personal", "Total Trends in Puppet", "Total Unique Trends in Person", "Total Unique Trends in Puppet", "Total Similar Unique Trends Between Personal and Puppet"])
    #     # writer.writerow(j)
    #     writer.writerow(["Total Trends in Personal", "Total Trends in Puppet", "Total Unique Trends in Person", "Total Unique Trends in Puppet", "Total Similar Unique Trends Between Personal and Puppet", "Topic"])
    #     for type in _type:
    #         p = compare_similarities_of_two_csv_per_topic("personal_3hr", "puppet_3hr", type)
    #         writer.writerow(p)
    #p = compare_similarities_of_two_csv_per_topic("personal_3hr", "puppet_3hr","Top Trends")

    #plot()

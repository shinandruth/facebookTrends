import csv
import pandas as pd
from collections import Counter

#--------------CHANGE HERE ---------------------
name = "trends_tabs_db_TABS"
_type = ["Top Trends", "Politics", "Science and Technology", "Sports", "Entertainment"]
#--------------CHANGE END HERE-----------------

df = pd.read_csv("CSV//Data for Thesis//Trends and Tabs//"+name+".csv", error_bad_lines=False)

def get_num_of_unique():
    url = df.url.values.tolist()
    set_url = set(url)
    return len(set_url)

def get_num_of_unique_per_type():
    url_per_type = {}
    for type in _type:
        url = df.loc[df["type"] == type, "url"].values.tolist()
        set_url = set(url)
        url_per_type[type] = len(set_url)
    return url_per_type

def get_ranking_of_sources():
    source = df.source.values.tolist()
    freqs = Counter(source).most_common(15)
    return freqs

def get_ranking_of_sources_per_type():
    source_per_type = {}
    for type in _type:
        source = df.loc[df["type"] == type, "source"].values.tolist()
        freqs = Counter(source).most_common(15)
        source_per_type[type] = freqs
    return source_per_type

def get_ranking_of_sources_total():
    source = df.source.values.tolist()
    freqs = Counter(source)
    return list(freqs)

if __name__ == "__main__":
    data_to_csv = []
    num_of_unique_url_overall = get_num_of_unique()
    num_of_unique_url_per_type = get_num_of_unique_per_type()
    ranking_of_sources_overall = get_ranking_of_sources()
    ranking_of_sources_per_type = get_ranking_of_sources_per_type()
    #data_to_csv.append(num_of_unique_url_overall)
    #data_to_csv.append(num_of_unique_url_per_type)
    # print("# of overall unique links", num_of_unique_url_overall)
    # print("# of unique link per type", num_of_unique_url_per_type)
    # print("sources overall", ranking_of_sources_overall)
    # print("sources per", ranking_of_sources_per_type)
    c = get_ranking_of_sources_total()
    # print(ranking_of_sources_overall)
    with open("url_CSV//total_"+name+".csv", "a", encoding="utf-8",  newline="") as f:
         writer = csv.writer(f)
         for v in c:
             writer.writerows([[v]])
         # writer.writerow(["Overall Unique Articles"])
         # writer.writerow([num_of_unique_url_overall])
         # writer.writerow(["Unique Articles Per Topic"])
         # #writer.writerow("Top Trends", "Politics", "Science/Tech", "Sports", "Entertainment")
         # for k,v in num_of_unique_url_per_type.items():
         #     writer.writerow([k, v])
         # writer.writerow(["Ranking Overall"])
         # for k, v in ranking_of_sources_overall:
         #     writer.writerow([k, v])
         # writer.writerow(["Ranking Per Topic"])
         # for k, v in ranking_of_sources_per_type.items():
         #     writer.writerows([[k]])
         #     for i in v:
         #         writer.writerows([i])

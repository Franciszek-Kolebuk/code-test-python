import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt

def NewData():
    data=[]
    with open("event_data.csv","r", newline="") as csvfile:
        csvReader = csv.DictReader(csvfile, delimiter=",")
        for row in csvReader:
            data.append(row)

    data = list(filter(lambda c: c["country"] == "US",data))

    for index,item in enumerate(data[:]):
        geo = item["geo"][6:-1]
        lon,lat=geo.split(" ")
        URL = "https://us-state-api.herokuapp.com/?lat=" + lat + "&lon="+lon
        r = requests.get(URL)
        if("error" in r.json().keys() or r.json()['state']== None):
            data.remove(item)
        else:
            print(index)
            state = r.json()["state"]["name"]
            postal = r.json()["state"]["postal"]
            item.update({"state": state})
            item.update({"state_code": postal})


    with open("newData.csv","w", newline="") as csvfile:
        csvWriter = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        csvWriter.writeheader()
        csvWriter.writerows(data)

#NewData()

def SumChart():
    df = pd.read_csv("newData.csv")

    gr1 = df.groupby('state').count().reset_index()
    gr1["count"] = gr1["id"]
    gr1 = gr1.iloc[:, [0,10]]
    states = gr1.iloc[:, 0]
    counts = gr1.iloc[:, 1]

    plt.figure(figsize=(14,5))
    plt.xticks(rotation=90)
    plt.bar(states, counts)
    plt.show()

#SumChart()    

def ValueChart():
    df = pd.read_csv("newData.csv")

    gr2 = df.groupby('state').sum("eventValue").reset_index()
    states = gr2.iloc[:, 0]
    values = gr2.iloc[:, 1]

    plt.figure(figsize=(14,5))
    plt.xticks(rotation=90)
    plt.bar(states, values)
    plt.show()

ValueChart()  
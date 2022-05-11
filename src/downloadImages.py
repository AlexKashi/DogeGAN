import requests
import csv
from tqdm import tqdm
import os
urls = []
outDir = "output/azuki-v2/"
fileNames = ["cryptopunks.csv","cryptopunks-2.csv", "cryptopunks-3.csv"]
#fileNames = ["boredapeyachtclub.csv","boredapeyachtclub-1.csv", "boredapeyachtclub-2.csv"]
filenames = ["azuki.csv"]

collections = ["boredapeyachtclub", "mutant-ape-yacht-club","bored-ape-kennel-club", "proof-moonbirds", "impostors-genesis-aliens" ,"hakinft-io", "cryptopunks", "doodles-official","cool-cats-nft","the-doge-pound" ]

collections = ["official-kreepy-club"]

for collection in collections:
    data = []
    with open(f"urls/{collection}.csv", "r") as csvFile:
         reader = csv.DictReader(csvFile)
         # print(reader.header)
         for i, row in enumerate(reader):
            data.append([row["name"], row["url"]])
            
    for i, item in enumerate(tqdm(data)):
        name = item[0].replace("#", "-")
        path = f"output/{collection}"
        if not os.path.exists(path):
            os.makedirs(path)
        with open(f"output/{collection}/{name}.jpg", "wb+") as file:
            file.write(requests.get(item[1]).content)

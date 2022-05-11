import requests
import os
import json
import csv
def getKey():
    key = None
    with open('/home/alex/Harvard/API_KEY.txt', "r") as f:
        key = f.readlines()[0]
    return key

API_KEY = getKey()


collections = "azuki"

collections = ["boredapeyachtclub", "mutant-ape-yacht-club","bored-ape-kennel-club", "proof-moonbirds", "impostors-genesis-aliens" ,"hakinft-io", "cryptopunks", "doodles-official","cool-cats-nft","the-doge-pound" ]
#collections = ["official-kreepy-club"]
def getUrl(collection,cursor = None):
    if cursor is None:
        return f"https://api.opensea.io/api/v1/assets?collection={collection}&order_direction=asc&limit=50&&include_orders=false"
    return f"https://api.opensea.io/api/v1/assets?collection={collection}&cursor={cursor}&order_direction=asc&limit=50&&include_orders=false"

headers = {
    "Accept": "application/json",
    "X-API-KEY": API_KEY
}




def isDone():
    return cursor is None and count > 0

assets = []


header = ["name", "url"]

for collection in collections:
    output = "urls/" + collection + ".csv"
    count = 0
    cursor = None
    assets = []
    with open(output, 'w+', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()

        while not isDone():
            response = requests.request("GET", getUrl(collection, cursor), headers=headers)
          #  print(response.text)
            json_response = json.loads(response.text)
            print(collection, count)
            for asset in json_response["assets"]:
                name = asset["name"]
                if name is None or name == "":
                    name = asset["token_id"]
                writer.writerow({"name" : "".join(name.split(" ")), "url" : asset["image_url"]})

                count +=1
            assets.extend(json_response["assets"])

            cursor = json_response["previous"]
      #      break

    output = "urls/" + collection + ".json"
   # mydata = json.loads(assets)
    with open(output, 'w') as outfile:
        json.dump(assets, outfile, indent = 4)
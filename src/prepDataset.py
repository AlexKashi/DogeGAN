import numpy as np
import glob
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from multiprocessing import Process
import json

finalSize = (128,128)


collections = ["azuki","official-kreepy-club", "boredapeyachtclub", "mutant-ape-yacht-club","bored-ape-kennel-club", "proof-moonbirds", "impostors-genesis-aliens" ,"hakinft-io", "cryptopunks", "doodles-official","cool-cats-nft","the-doge-pound", "rococo", "romanticism", "early-renaissance", "high-renaissance", "mannerism-late-renaissance", "cubism"]

# collections = ["boredapeyachtclub", "mutant-ape-yacht-club"]

collections = ["azuki", "hakinft-io"]


collections = ["hakinft-io"]
# collections = ["cryptopunks", "proof-moonbirds"]
collections = ["official-kreepy-club"]
collections = ["doodles-official"]
collections = ["boredapeyachtclub"]

collections = ["cryptopunks"]
# collections = ["proof-moonbirds", "impostors-genesis-aliens" ,"hakinft-io", "cryptopunks", "doodles-official","cool-cats-nft","the-doge-pound" ]
# collections = ["rococo", "romanticism", "early-renaissance", "high-renaissance", "mannerism-late-renaissance", "cubism"]
    # \b
    # {
    #     "labels": [
    #         ["00000/img00000000.png",6],
    #         ["00000/img00000001.png",9],
    #         ... repeated for every image in the datase
    #         ["00049/img00049999.png",1]
    #     ]
    # }

labels = []

def loadImages(collection):
    fileNames = glob.glob(f"output/{collection}/*.png")
    fileNames.extend(glob.glob(f"output/{collection}/*.jpg"))
    fileNames = sorted(fileNames)
    print(f"Found {len(fileNames)} files!")
    images = []
    for i, fileName in tqdm(enumerate(fileNames)):
        #print(i, fileName,cv2.imread(fileName))
        img = cv2.imread(fileName)
        if img is None:
            print(f"{fileName} is corrupt SKIP!")
            continue
        images.append(resize(centerCrop(img), size = finalSize))
      #  break
    return images 

def centerCrop(image):
    size = image.shape
    length = min(size[0], size[1])
    w = length
    h = length
    x = image.shape[1] / 2 - w/2
    y = image.shape[0] / 2 - h/2
    return image[int(y):int(y+h), int(x):int(x+w)]

def resize(image, size):
    return cv2.resize(image, size, interpolation = cv2.INTER_NEAREST)

def setupOutputDir(collection):
    outPath = f"../output/{collection}/"
    exists = os.path.exists(outPath)
    if not exists:
        os.makedirs(outPath)

    return outPath


def saveImages(path, images, collection):
    for i, image in enumerate(images):
        imageName = path + collection + "-" + str(i) + ".jpg"
        cv2.imwrite(path + collection + "-" + str(i) + ".jpg", image)
        labels.append([imageName.split("/")[-1], collections.index(collection)])


def main(collection):
    path = setupOutputDir("cryptopunks")
    images = loadImages(collection)
    saveImages(path, images, collection)
    print("Done!")


if __name__ == '__main__':
    processes = []
    for collection in collections:
        print(collection)
        main(collection)
    with open("../output/cryptopunks/dataset.json", "w+") as outfile:
        json.dump({"labels" : labels}, outfile, indent=4, sort_keys=True)

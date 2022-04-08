import numpy as np
import glob
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
finalSize = (128,128)
from tqdm import tqdm

def loadImages():
	fileNames = sorted(glob.glob("../../dataset/image/*.jpeg"))
	print(f"Found {len(fileNames)} files!")
	images = []
	for i, fileName in tqdm(enumerate(fileNames)):

		images.append(resize(centerCrop(cv2.imread(fileName)), size = finalSize))
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
	return cv2.resize(image, size, interpolation = cv2.INTER_LANCZOS4)

def setupOutputDir():
	outPath = "../output/preppedData/"
	exists = os.path.exists("../output/preppedData/")
	if not exists:
		os.makedirs(outPath)

	return outPath


def saveImages(path, images):
	for i, image in enumerate(images):
		cv2.imwrite(path + str(i) + ".jpg", image)


def main():
	path = setupOutputDir()
	images = loadImages()
	saveImages(path, images)
	print("Done!")


if __name__ == '__main__':
	main()

from PIL import Image
import os
import argparse

parser = argparse.ArgumentParser(description="Goes through images in a given directory and deletes corrupted ones")
parser.add_argument("-d", "--dataset_path", help = "Path to the directory with images", default=r"/Volumes/Matija_ExtH/WatchedOlives/WatchedOlives/dataset_oil_estimation")

args = vars(parser.parse_args())

dataset_path = args['dataset_path']

for image_name in os.listdir(dataset_path):

	image_path = os.path.join(dataset_path, image_name)

	try:
		img = Image.open(image_path)
		img.verify()
		img.close() 
	except Exception as e: 
		print('File {0}: \n{1}'.format(image_path, e))
		os.remove(image_path)
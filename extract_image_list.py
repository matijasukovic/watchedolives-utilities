import os
import argparse

parser = argparse.ArgumentParser(description='For a given YOLO subset, extracts a list of image filenames and saves as annotations.txt in the labels directory. This is used when uploading a YOLO dataset to CVAT, since it is needed in this process.')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
images = args["images"]
labels = args["labels"]

# Example input
# dataset_path = r"W:\rock_detection_v4.5"
# images = r"\images\valid"
# labels = r"\labels\valid"


directory = os.fsencode(dataset_path + images)

output_file = open(os.path.join(dataset_path, labels, 'annotations.txt'), 'w')

for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    output_file.write(filename + '\n')

output_file.close()

import os
import argparse

parser = argparse.ArgumentParser(description='Counts the number of annotations in a YOLO subset')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels director', required=True)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
labels = args["labels"]

# Example input
# dataset_path = r"W:\rock_detection_v4.5"
# labels = r"\labels\test"


number_of_annotations = 0

directory = os.fsencode(dataset_path + labels)
    
for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    label_path = dataset_path + labels + "\\" + filename

    with open(label_path, 'r') as fp:
        lines = len(fp.readlines())
        number_of_annotations += lines
    
print('number of annotations in ' + dataset_path + labels + ": ", number_of_annotations)

# 3852 + 94 + 123 = 
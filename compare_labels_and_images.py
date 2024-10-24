import os
import argparse

parser = argparse.ArgumentParser(description="Use this script to compare contents of 'images' and 'labels' directories of a YOLO dataset. Lists out any images that miss annotations or annotations that are missing a corresponding image.")
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', default="\images")
parser.add_argument('-l','--labels', help='Inner path to labels directory', default="\labels")
parser.add_argument('-del', '--delete_missing', help='Delete files whose counterpart is missing', default=False)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
images = args["images"]
labels = args["labels"]
delete_missing = args["delete_missing"]

# Example inputs
# dataset_path = r"W:\rock_detection_v4.5"
# images = r"\images\val"
# labels = r"\labels\val"
# delete_missing = False


print("Going through labels...")

directory = os.fsencode(dataset_path + labels)
    
for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    label_path = dataset_path + labels + "\\" + filename

    image_filename = filename.split('.')[0] + '.png'
    image_path = dataset_path + images + "\\" + image_filename

    if not os.path.isfile(image_path):
        print('Missing image: ', image_path)

        if delete_missing == "True":
            os.remove(label_path)


print("Going through images...")

directory = os.fsencode(dataset_path + images)
    
for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    image_path = dataset_path + images + "\\" + filename

    label_filename = filename.split('.')[0] + '.txt'
    label_path = dataset_path + labels + "\\" + label_filename

    if not os.path.isfile(label_path):
        print('Missing label: ', label_path)
        if delete_missing == "True":
            
            os.remove(image_path)

import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Given a YOLO subset, extract unannotated images to an output directory, leaving behind images containing annotations')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
parser.add_argument('-e','--image_extension', help='Extention of the images', default='.png')
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
images = args["images"]
labels = args["labels"]
image_extension = args["image_extension"]

# Example input
# dataset_path = r"W:\rock_detection_v4.0"
# images = r"\images\valid"
# labels = r"\labels\valid"
# image_extension = '.png'


directory = os.fsencode(dataset_path + labels)

annotated_image_count = 0
background_image_count = 0

print('extracting background images: ')

for file in os.listdir(directory):
    label_filename = str(file)[2:len(str(file)) - 1]
    label_path = dataset_path + labels + "\\" + label_filename

    if os.path.getsize(label_path) == 0:
        background_image_count += 1

        image_filename = label_filename.split('.')[0] + image_extension
        image_path = dataset_path + images + "\\" + image_filename

        shutil.move(label_path, dataset_path + labels + '\\..\\backgrounds\\' + label_filename)
        shutil.move(image_path, dataset_path + images + '\\..\\backgrounds\\' + image_filename)

        print(image_filename)
    else:
        annotated_image_count += 1

print("No. of annotated images: ", annotated_image_count)
print("No. of background images: ", background_image_count)

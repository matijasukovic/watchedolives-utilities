import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Given a YOLO subset, extract raw images to an output directory, leaving augmented images behind')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
parser.add_argument('-e','--image_extension', help='Extention of the images', default='.png')
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
images = args["images"]
labels = args["labels"]
output_directory_name = args["output_directory_name"]
image_extension = args["image_extension"]

# Example input
# dataset_path = r"W:\rock_detection_v4.0"
# images = r"\images\valid"
# labels = r"\labels\valid"
# output_directory_name = r"valid_raw"
# image_extension = '.png'


directory = os.fsencode(dataset_path + labels)

print('extracting raw images: ')

for file in os.listdir(directory):
    label_filename = str(file)[2:len(str(file)) - 1]
    label_path = dataset_path + labels + "\\" + label_filename

    if not "aug" in label_filename:
        image_filename = label_filename.split('.')[0] + image_extension
        image_path = dataset_path + images + "\\" + image_filename

        output_label_path = dataset_path + labels + '\\..\\' + output_directory_name + '\\' + label_filename
        output_image_path = dataset_path + images + '\\..\\' + output_directory_name + '\\' + image_filename

        os.makedirs(os.path.dirname(output_label_path), exist_ok=True)
        shutil.copy(label_path, dataset_path + labels + '\\..\\' + output_directory_name + '\\' + label_filename)

        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
        shutil.copy(image_path, dataset_path + images + '\\..\\' + output_directory_name + '\\' + image_filename)

        print(image_filename)


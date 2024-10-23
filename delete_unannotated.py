import os
import random
import argparse

parser = argparse.ArgumentParser(description='Given a YOLO subset, deletes a portion or all of images whose annotations are empty')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
parser.add_argument('-e','--image_extension', help='Extension of the images', default=".png")
parser.add_argument('-c','--chance_for_removal', help='Chance in percents for each unannotated image to be deleted', default=0)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
images = args["images"]
labels = args["labels"]
image_extension = args["image_extension"]
chance_for_removal = args["chance_for_removal"]

# Example input
# dataset_path = r"W:\rock_detection_v4.5"
# images = r"\images\test_tiled"
# labels = r"\labels\test_tiled"
# image_extension = '.png'
# chance_for_removal = 0


def randomlyChosenForRemoval():
    if chance_for_removal == 100:
        return True

    if chance_for_removal == 0:
        return False

    return random.randint(0,100) < chance_for_removal

directory = os.fsencode(dataset_path + labels)

annotated_image_count = 0
background_image_count = 0

for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    label_path = dataset_path + labels + "\\" + filename

    if os.path.getsize(label_path) == 0:
        if randomlyChosenForRemoval():
            image_filename = filename.split('.')[0] + image_extension
            image_path = dataset_path + images + "\\" + image_filename

            os.remove(image_path)
            os.remove(label_path)
            print("Deleted " + image_path)
        else:
            background_image_count += 1
    else:
        annotated_image_count += 1

print("No. of annotated images: ", annotated_image_count)
print("No. of background images: ", background_image_count)

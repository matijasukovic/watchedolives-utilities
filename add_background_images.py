import os
import random
import shutil
import argparse

parser = argparse.ArgumentParser(description='Add a number of background images (images with no annotations) to an existing subset.')
parser.add_argument('-oip','--output_images_path', help='Images directory (where backgrounds are to be added)', required=True)
parser.add_argument('-olp','--output_labels_path', help='Labels for the images', required=True)
parser.add_argument('-bip','--background_images_path', help='Background images directory', required=True)
parser.add_argument('-blp','--background_labels_path', help='Background labels directory', required=True)
parser.add_argument('-n','--number_of_backgrounds_to_copy', help='Number of backgrounds to copy', required=True)
args = vars(parser.parse_args())

output_images_path = args["output_images_path"]
output_labels_path = args["output_labels_path"]
background_images_path = args["background_images_path"]
background_labels_path = args["background_labels_path"]
number_of_backgrounds_to_copy = args["number_of_backgrounds_to_copy"]

# Example inputs
# output_images_path = r"W:\rock_detection_v4.5\images\valid"
# output_labels_path = r"W:\rock_detection_v4.5\labels\valid"
# background_images_path = r"W:\rock_detection_v4.0\images\backgrounds"
# background_labels_path = r"W:\rock_detection_v4.0\labels\backgrounds"
# number_of_backgrounds_to_copy = 50


def random_files(num, list_): 
  file_names = []
  while True: 
    ap = random.choice(list_) 
    if ap not in file_names: 
        file_names.append(ap) 
        if len(file_names) == num: 
            return file_names 

bg_images_list = os.listdir(background_images_path)

random_bg_list = random_files(number_of_backgrounds_to_copy, bg_images_list)

for image in random_bg_list:
   filename = image[:len(image)-4]
   label = filename + '.txt'

   shutil.copy(background_images_path + "/" + image, output_images_path + '/' + image)
   shutil.copy(background_labels_path + "/" + label, output_labels_path + '/' + label)
   print('Copied ' + filename)

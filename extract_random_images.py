import os
import argparse
import random
import shutil
from PIL import Image

parser = argparse.ArgumentParser(description='Given image sets, randomly extracts an amount of images to an output directory.')
parser.add_argument('-s','--sets_path', help='Path to the directory containing sets', default=r"/Volumes/Matija_ExtH/WatchedOlives/WatchedOlives/dataset_no_dupes")
parser.add_argument('-a','--amount_per_set', help='How many images to extract per set', default=2)
parser.add_argument('-o','--output_path', help='Path to the output directory', default=r"/Volumes/Matija_ExtH/WatchedOlives/WatchedOlives/dataset_oil_estimation")
args = vars(parser.parse_args())

sets_path = args["sets_path"]
amount_per_set = args["amount_per_set"]
output_path = args["output_path"]

if __name__ == '__main__':
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for set_name in os.listdir(sets_path):
        set_path = os.path.join(sets_path, set_name)
        
        number_to_extract = amount_per_set if len(os.listdir(set_path)) > amount_per_set else len(os.listdir(set_path))
        target_image_names = random.sample(os.listdir(set_path), k=number_to_extract)
        
        for image_name in target_image_names:
            if image_name[:1] == '.':
                continue
            
            print(image_name)

            image_path = os.path.join(set_path, image_name)

            try:
                img = Image.open(image_path)
                img.verify()
                img.close() 
            except Exception as e: 
                print('File {0}: \n{1}'.format(image_path, e))
                continue

            shutil.copyfile(image_path, os.path.join(output_path, image_name))
        
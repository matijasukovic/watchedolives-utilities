import datumaro as dm
import os
import argparse

parser = argparse.ArgumentParser(description='Given a list of datasets in CVAT format, generates dataset in YOLO format')
parser.add_argument('-i','--input_path', help='Path to the directory containing CVAT datasets', required=True)
parser.add_argument('-o','--output_path', help='Output directory path', required=True)
args = vars(parser.parse_args())

input_path = args["input_path"]
output_path = args["output_path"]

# Example input
# input_path = r'W:\cvat_train'
# output_path = r'W:\rock_detection_v1.0\train'

first_set = 'set'

merged_dataset  = dm.Dataset.import_from(input_path + first_set, 'cvat')

directory = os.fsencode(input_path)
    
for set_directory in os.listdir(directory):
    set_name = os.fsdecode(set_directory)

    if set_name == first_set:
        continue

    print('Merging ' + set_name + '...')

    dataset = dm.Dataset.import_from(input_path + set_name, 'cvat')
    merged_dataset.update(dataset)

print('Sets merged! Exporting...')

merged_dataset.export(output_path, 'yolo')
print(merged_dataset.infos)

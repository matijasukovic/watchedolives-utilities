import datumaro as dm
import argparse

parser = argparse.ArgumentParser(description='Converts a CVAT dataset to a YOLO dataset')
parser.add_argument('-i','--input_path', help='Input path', required=True)
parser.add_argument('-o','--output_path', help='Output path', required=True)
args = vars(parser.parse_args())

input_path = args["input_path"]
output_path = args["output_path"]

# Example input
# input_path = r"W:\cvat_train\set137"
# output_path = r"W:\rock_detection_v4.5\set_137_raw"


input_dataset = dm.Dataset.import_from(input_path, 'cvat')

input_dataset.export(output_path, 'yolo')
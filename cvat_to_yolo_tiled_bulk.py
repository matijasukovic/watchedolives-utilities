import os
import datumaro as dt
from datumaro.plugins.tiling import Tile
import argparse

parser = argparse.ArgumentParser(description='Given a list of datasets in CVAT format, generates a tiled dataset in YOLO format')
parser.add_argument('-i','--path_to_cvat_datasets', help='Path to the directory containing CVAT datasets', required=True)
parser.add_argument('-o','--output_path', help='Output path', required=True)
args = vars(parser.parse_args())

path_to_cvat_datasets = args["path_to_cvat_datasets"]
output_path = args["output_path"]

# Example input
# path_to_cvat_datasets = r'W:\cvat_test'
# output_path = r'W:\rock_detection_v4.5\test_tiled'


# Settings to tile 1920x1080 images into 6 images of size 640x640:
gridSize=(2, 3)
overlap=(0.372, 0)

thresholdDropAnn=0.20

for dir in os.listdir(path_to_cvat_datasets):
    dataset = dt.Dataset.import_from(path_to_cvat_datasets + '\\' + dir, 'cvat')

    print('Tiling ' + dir + '...')
    tiled_dataset = dataset.transform(
        Tile, grid_size=gridSize, overlap=overlap, threshold_drop_ann=thresholdDropAnn
    )

    dataset.export(output_path, 'yolo', save_media=True)
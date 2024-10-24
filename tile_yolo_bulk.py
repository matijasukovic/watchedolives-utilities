import os
import datumaro as dt
from datumaro.plugins.tiling import Tile
import argparse

parser = argparse.ArgumentParser(description='Given a list of datasets in CVAT format, generates a tiled dataset in YOLO format')
parser.add_argument('-i','--input_path', help='Path to the directory containing datasets', required=True)
parser.add_argument('-o','--output_path', help='Output path', required=True)
args = vars(parser.parse_args())

input_path = args["input_path"]
output_path = args["output_path"]

# Example input
# input_path = r'W:\cvat_test'
# output_path = r'W:\rock_detection_v4.5\test_tiled'


def createYoloMetadata(set_path):
    with open(os.path.join(set_path, 'obj.names'), 'w') as f:
        f.write('rock')
    f.close()

    with open(os.path.join(set_path, 'obj.data'), 'w') as f:
        f.write('classes = 1\n')
        f.write('names = obj.names')
    f.close()


# Settings to tile 1920x1920 images into 9 images of size 640x640:
gridSize=(3, 3)
overlap=(0, 0)

thresholdDropAnn=0.25

for dir in os.listdir(input_path):
    set_path = os.path.join(input_path, dir)
    
    createYoloMetadata(set_path)

    dataset = dt.Dataset.import_from(set_path, 'yolo')

    print('Tiling ' + dir + '...')
    tiled_dataset = dataset.transform(
        Tile, grid_size=gridSize, overlap=overlap, threshold_drop_ann=thresholdDropAnn
    )

    dataset.export(output_path, 'yolo', save_media=True)
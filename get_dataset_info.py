import datumaro as dm
import argparse

parser = argparse.ArgumentParser(description='Prints details of a CVAT dataset')
parser.add_argument('-i','--dataset_path', help='Dataset path', required=True)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]

# Example input
# dataset_path = r'W:\cvat_valid\set100'


dataset = dm.Dataset.import_from(dataset_path, 'cvat')

print(dataset.infos)
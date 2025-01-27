from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Exports a PyTorch model to a desired format')
parser.add_argument('-i','--input_path', help='Path to PyTorch (.pt) model', required=True)
parser.add_argument('-f','--format', help='Output format', default="ncnn")
args = vars(parser.parse_args())

input_path = args["input_path"]
format = args["format"]

# Example input
# input_path = r'W:\runs\n_p2_tuned\weights\best.pt'
# format = 'ncnn'


model = YOLO(input_path)

model.export(format=format) 

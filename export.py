from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-i','--input_path', help='Path to PyTorch (.pt) model', required=True)
args = vars(parser.parse_args())

input_path = args["input_path"]

# Example input
# input_path = r'W:\runs\n_p2_tuned\weights\best.pt'


model = YOLO(input_path)

model.export(format="ncnn") 
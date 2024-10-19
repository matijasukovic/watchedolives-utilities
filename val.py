from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Starts a validation process')
parser.add_argument('-m','--model_path', help='Path to PyTorch (.pt) model', required=True)
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-s','--split', help='Dataset split', choices=["val", "test"], default="val")
args = vars(parser.parse_args())

model_path = args["model_path"]
dataset_path = args["dataset_path"]
split = args["split"]

# Example input
# model_path = r"W:\runs\s_p2_optuna\weights\best.pt"
# dataset_path = r"D:\rock_detection_v4.5\config.yaml"
# split = 'test'

model = YOLO(model_path)

if __name__ == '__main__':
    model.val(data=dataset_path, split=split, conf=0.2, iou=0.2)


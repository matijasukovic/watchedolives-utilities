from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Starts hyperparameter tuning via ultralytics YOLO built-in tuner')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-m','--model_config', help='YAML file of a YOLO model configuration', default="yolov8n.yaml")
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
model_config = args["model_config"]

# Example input
# dataset_path = r'D:\rock_detection_v4.5\config.yaml'
# model_config = 'yolov8s-p2.yaml'


model = YOLO(model_config)

model.tune(data=dataset_path, epochs=30, iterations=300, batch=30, imgsz=640, save=False, val=False, plots=False)
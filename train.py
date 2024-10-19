from ultralytics import YOLO
import yaml
import argparse

parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-h','--hyperparameters_path', help='Path to a YAML file with a list of hyperparameters', required=True)
parser.add_argument('-m','--model_config', help='YAML file of a YOLO model configuration', default="yolov8n.yaml")
parser.add_argument('-d','--dataset_config_path', help='Path to a YAML file with a dataset configuration', required=True)
args = vars(parser.parse_args())

hyperparameters_path = args["hyperparameters"]
model_config = args["model_config"]
dataset_config_path = args["dataset_config"]

# Example input
# hyperparameters_path = r"W:\optuna_output\best_trial.yaml"
# model_config = 'yolov8s-p2.yaml'
# dataset_config_path = r"D:\rock_detection_v4.5\config.yaml"


with open(hyperparameters_path, 'r') as f:
    best_hyperparams = yaml.safe_load(f)


model = YOLO(model_config)

if __name__ == '__main__':
    model.train(
        data=dataset_config_path,
        imgsz=640,
        single_cls=True,
        epochs=350,
        batch=32,
        optimizer="AdamW",
        patience=100,
        iou=0.2,
        deterministic=False,
        **best_hyperparams
    )
from sahi import AutoDetectionModel
from sahi.predict import get_prediction, get_sliced_prediction
from sahi.utils.file import save_json
import os
import cv2

import argparse

parser = argparse.ArgumentParser(description='Performs normal and tiled inference on a given YOLO subset')
parser.add_argument('-m','--model_path', help='Path to a PyTorch (.pt) model', required=True)
parser.add_argument('-i','--images', help='Inner path to images directory', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
parser.add_argument('-e','--export_path', help='Directory to export visualizations to', required=True)
args = vars(parser.parse_args())

model_path = args["model_path"]
images = args["images"]
labels = args["labels"]
export_path = args["export_path"]

# Example input
# model_path = r"W:\runs\v45_m_bs28_340epoch_base\weights\best.pt"
# images = r"D:\rock_detection_v4.5\images\test"
# labels = r"D:\rock_detection_v4.5\labels\test"
# export_path = r"C:\Users\suksa\Desktop\training\inference"


def draw_ground_truth(image_path, label_path):
    image = cv2.imread(image_path)
    H, W = image.shape[:2]

    label_file = open(label_path, "r").read()
    labels = [[float(value) for value in label.split()] for label in label_file.split("\n") if label.strip()]

    for label in labels:
        class_id, x_center, y_center, width, height = label
        x1 = int(x_center*W - width*W/2)
        y1 = int(y_center*H - height*H/2)
        x2 = int(x_center*W + width*W/2)
        y2 = int(y_center*H + height*H/2)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    cv2.imwrite(image_path, image)

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path=model_path,
    confidence_threshold=0.4,
    device="cuda:0",
)

# results_array = []

for image in os.listdir(images):
    image_path = images + '\\' + image

    filename = str(image)[0:len(str(image)) - 4]
    label_path = labels + "\\" + filename + '.txt'

    result_normal = get_prediction(image_path, detection_model, verbose=1)
    result_normal.export_visuals(export_dir=export_path, file_name=filename + '_normal', text_size=1.25, hide_conf=True)

    draw_ground_truth(export_path + "\\" + filename + '_normal.png', label_path)

    result_sliced = get_sliced_prediction(
        image_path,
        detection_model,
        slice_height=640,
        slice_width=640,
        overlap_height_ratio=0.2,
        overlap_width_ratio=0.2,
        verbose=1
    )

    result_sliced.export_visuals(export_dir=export_path, file_name=filename + '_sliced')

    # results_array.append(result_sliced.to_coco_annotations())

    draw_ground_truth(export_path + "\\" + filename + '_sliced.png', label_path)

# save_json(data=results_array, save_path="runs\\predict\\coco_predict.json")
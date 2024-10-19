from ultralytics import YOLO
import argparse

parser = argparse.ArgumentParser(description='Resumes a paused training')
parser.add_argument('-m','--model_path', help='Path to a PyTorch (.pt) model. Recommended to use last.pt to continue training with the last reached state.', required=True)
args = vars(parser.parse_args())

model_path = args["model_path"]

# Example input
# model_path = r"C:\Users\suksa\Desktop\training\runs\detect\train2\weights\last.pt"


model = YOLO(model_path) 

if __name__ == '__main__':  
    results = model.train(resume=True)
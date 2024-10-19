import optuna
from ultralytics import YOLO
import yaml
import pickle
import optuna.visualization as vis
import os
import argparse

parser = argparse.ArgumentParser(description='Starts hyperparameter tuning via Optuna framework with F2-score as fitness function')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-o','--output_directory', help='Output directory', required=True)
parser.add_argument('-m','--model_config', help='YAML file of a YOLO model configuration', default="yolov8n.yaml")
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
output_directory = args["output_directory"]
model_config = args["model_config"]

# Example input
# dataset_path = r"D:\rock_detection_v4.5\config.yaml"
# output_directory = r".\optuna_output"
# model_config = 'yolov8n.yaml'


def objective(trial):
    lr0 = trial.suggest_float('lr0', 1e-5, 1e-1)
    lrf= trial.suggest_float('lrf', 0.0001, 0.1)
    momentum = trial.suggest_float('momentum', 0.7, 0.95)
    warmup_momentum = trial.suggest_float('warmup_momentum', 0.0, 0.95)
    warmup_epochs = trial.suggest_int('warmup_epochs', 0, 5)
    weight_decay = trial.suggest_float('weight_decay', 1e-6, 1e-3)
    box = trial.suggest_float('box', 1.0, 20.0)
    cls = trial.suggest_float('cls', 0.2, 4.0)
    dfl = trial.suggest_float('dfl', 0.4, 6.0)
    
    
    model = YOLO(model_config)
    
    results = model.train(
        data = dataset_path, 
        epochs = 30,
        imgsz = 640,
        optimizer = 'AdamW',
        flipud = 0.5,
        fliplr = 0.5,
        iou = 0.2,
        deterministic = False,
        batch = 52,
        close_mosaic = False,
        lr0 = lr0,
        lrf = lrf,
        momentum = momentum,
        warmup_momentum = warmup_momentum,
        warmup_epochs = warmup_epochs,
        weight_decay = weight_decay,
        box = box,
        cls = cls,
        dfl = dfl,
    )

    precision = results.results_dict['metrics/precision(B)']
    recall = results.results_dict['metrics/recall(B)']
    
    try:
        f2_score = (5 * precision * recall) / (4 * precision + recall)
    except ZeroDivisionError:
        f2_score = 0

    return f2_score


def save_plots_callback(study, trial):
    plot_filenames = [
        os.path.join(output_directory, 'optimization_history_plot.png'),
        os.path.join(output_directory, 'parallel_coordinate_plot.png'),
        os.path.join(output_directory, 'contour_plot.png')
    ]

    for filename in plot_filenames:
        if os.path.exists(filename):
            os.remove(filename)

    fig = vis.plot_parallel_coordinate(study)
    fig.write_image(os.path.join(output_directory, 'parallel_coordinate_plot.png'))

    fig = vis.plot_contour(study)
    fig.write_image(os.path.join(output_directory, 'contour_plot.png'))

    fig = vis.plot_optimization_history(study)
    fig.write_image(os.path.join(output_directory, 'optimization_history_plot.png'))

    print(f"Plots updated after trial {trial.number}")


def main():
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    study = optuna.create_study(direction='maximize') 

    study.optimize(objective, n_trials=300, callbacks=[save_plots_callback]) 

    print("Best trial:")
    trial = study.best_trial
    print(f"  Value: {trial.value}")

    output_dict = {}

    print("  Params: ")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
        output_dict.update({key: value})


    with open(os.path.join(output_directory, 'best_trial.yaml'), 'w') as f:
        yaml.dump(output_dict, f)
        print("Best trial saved to 'best_trial.yaml'")

    with open(os.path.join(output_directory, 'optuna_study.pkl'), 'wb') as f:
        pickle.dump(study, f)

if __name__ == '__main__':
    main()
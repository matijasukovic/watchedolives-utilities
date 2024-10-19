import os
import argparse

parser = argparse.ArgumentParser(description='Searches and deletes the given annotation from a given YOLO subset')
parser.add_argument('-d','--dataset_path', help='Dataset path', required=True)
parser.add_argument('-l','--labels', help='Inner path to labels directory', required=True)
parser.add_argument('-a','--wrong_annotation', help='Annotation to be deleted from the labels', required=True)
args = vars(parser.parse_args())

dataset_path = args["dataset_path"]
labels = args["labels"]
wrong_annotation = args["wrong_annotation"]

# Example input
# dataset_path = r"W:\rock_detection_v4.0"
# labels = r"\train_split1_messed\obj_train_data"
# wrong_annotation = "0 0.241219 0.701883 0.045031 0.035047\n"


directory = os.fsencode(dataset_path + labels)

for file in os.listdir(directory):
    filename = str(file)[2:len(str(file)) - 1]
    
    label_path = dataset_path + labels + '\\' + filename

    with open(label_path) as f:
        content = f.read()

        if wrong_annotation in content:
            print('Found wrong annotation in: ', filename)

            cleaned_annotations = content.replace(wrong_annotation, '')
            f.close()

            with open(label_path, 'w') as f2:
                f2.write(cleaned_annotations)
                f2.close()
        
        else:
            f.close()
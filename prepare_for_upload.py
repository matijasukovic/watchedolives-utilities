import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Given raw dataset obtained from WatchedOlives Pi device, generates zipped labels file for uploading labels to CVAT')
parser.add_argument('-s','--set_path', help='Set path', required=True)
args = vars(parser.parse_args())

set_path = args["set_path"]

# Example input
#set_path = r"W:\2024_sets\raw\2024_set1"


images_dir = os.path.join(set_path, 'images')
labels_dir = os.path.join(set_path, 'labels')

def createAnnotationsFile(images_dir, labels_dir):
    print("Generating annotations.txt")

    with open(os.path.join(labels_dir, 'annotations.txt'), 'w') as annotations_list_file:

        for file in os.listdir(images_dir):
            image_filename = str(file)
            label_filename = image_filename[:len(image_filename) - 4] + '.txt'

            # create empty annotation if an image is missing one
            if not os.path.exists(os.path.join(labels_dir, label_filename)):
                with open(os.path.join(labels_dir, label_filename), 'w') as fp:
                    pass

            annotations_list_file.write(image_filename + '\n')

    annotations_list_file.close()

def createObjFiles(labels_dir):
    print("Generating obj files")
    with open(os.path.join(labels_dir, 'obj.names'), 'w') as f:
        f.write('rock')
    f.close()

    with open(os.path.join(labels_dir, 'obj.data'), 'w') as f:
        f.write('classes = 1\n')
        f.write('annotations = annotations.txt\n')
        f.write('names = obj.names')
    f.close()

def createArchive(set_path, labels_dir):
    print('Packaging into obj_annotations_data.zip')
    shutil.make_archive(os.path.join(set_path, 'obj_annotations_data'), 'zip', labels_dir)

def removeAddedFiles(labels_dir):
    print("Cleaning up")

    os.remove(os.path.join(labels_dir, 'annotations.txt'))
    os.remove(os.path.join(labels_dir, 'obj.data'))
    os.remove(os.path.join(labels_dir, 'obj.names'))


createAnnotationsFile(images_dir, labels_dir)

createObjFiles(labels_dir)

createArchive(set_path, labels_dir)

removeAddedFiles(labels_dir)
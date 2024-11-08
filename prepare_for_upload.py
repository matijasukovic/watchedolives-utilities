import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Given raw dataset obtained from WatchedOlives Pi device, generates zipped labels file for uploading labels to CVAT')
parser.add_argument('-s','--sets_path', help='Path to the directory containing sets', default=r"W:\2024_sets\raw")
parser.add_argument('-o', '--overwrite', help="Wheather or not to overwrite existing annotations", default="False")
args = vars(parser.parse_args())

sets_path = args["sets_path"]
overwrite = args["overwrite"]

def createAnnotationsFile(images_dir, labels_dir):
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
    with open(os.path.join(labels_dir, 'obj.names'), 'w') as f:
        f.write('rock')
    f.close()

    with open(os.path.join(labels_dir, 'obj.data'), 'w') as f:
        f.write('classes = 1\n')
        f.write('annotations = annotations.txt\n')
        f.write('names = obj.names')
    f.close()

def createArchive(set_path, labels_dir):
    shutil.make_archive(os.path.join(set_path, 'obj_annotations_data'), 'zip', labels_dir)

def removeAddedFiles(labels_dir):
    os.remove(os.path.join(labels_dir, 'annotations.txt'))
    os.remove(os.path.join(labels_dir, 'obj.data'))
    os.remove(os.path.join(labels_dir, 'obj.names'))

if __name__ == '__main__':  
    for set_name in os.listdir(sets_path):
        set_path = os.path.join(sets_path, set_name)

        uploadFile_exists = os.path.exists(os.path.join(set_path, 'obj_annotations_data.zip'))
        if uploadFile_exists and overwrite != "True":
            continue

        print(set_name)

        images_dir = os.path.join(set_path, 'images')
        labels_dir = os.path.join(set_path, 'labels')
    
        createAnnotationsFile(images_dir, labels_dir)
        createObjFiles(labels_dir)
        createArchive(set_path, labels_dir)
        removeAddedFiles(labels_dir)
    
    print('Upload files generated.')
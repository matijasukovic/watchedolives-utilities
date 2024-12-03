import os
import shutil
import argparse

parser = argparse.ArgumentParser(description='Given a directory containing annotated sets, processes zipped annotations downloaded from CVAT in YOLO format into YOLO sets.')
parser.add_argument('-r', '--raw_sets_path', help="Path to the directory containing raw sets", default=r"W:\2024_sets\raw")
parser.add_argument('-a','--annotated_sets_path', help='Path to the directory containing annotated sets', default=r"W:\2024_sets\annotated")
parser.add_argument('-e', '--image_extension', help='Extension of images', default='.png')
parser.add_argument('-o', '--overwrite', help="Wheather or not to overwrite sets with the same name as the zip files", default="False")
args = vars(parser.parse_args())

raw_sets_path = args["raw_sets_path"]
annotated_sets_path = args["annotated_sets_path"]
image_extension = args["image_extension"]
overwrite = args["overwrite"]

def removeMetadata(set_path):
    os.remove(os.path.join(set_path, 'train.txt'))
    os.remove(os.path.join(set_path, 'obj.data'))
    os.remove(os.path.join(set_path, 'obj.names'))

def renameLabelsDirectory(set_path):
    os.rename(os.path.join(set_path, 'obj_train_data'), os.path.join(set_path, 'labels'))

def copyImagesFromRawToAnnotatedSet(raw_set_path, annotated_set_path, image_extension='.png'):
    raw_images_dir = os.path.join(raw_set_path, 'images')

    annotated_images_dir = os.path.join(annotated_set_path, 'images')
    annotated_labels_dir = os.path.join(annotated_set_path, 'labels')

    os.makedirs(annotated_images_dir)

    for file in os.listdir(annotated_labels_dir):
        image_filename = str(file)[:len(str(file)) - 4] + image_extension

        source_path = os.path.join(raw_images_dir, image_filename)
        destination_path = os.path.join(annotated_images_dir, image_filename)

        assert os.path.exists(source_path), "Missing image: {0}".format(source_path)

        shutil.copyfile(
            src = source_path,
            dst = destination_path
        )


if __name__ == '__main__':  
    for item_name in os.listdir(annotated_sets_path):
        if not '.zip' in item_name:
            continue

        zipped_file_path = os.path.join(annotated_sets_path, item_name)

        print("Processing {0}...".format(zipped_file_path))

        set_name = item_name.split('.')[0]
        raw_set_path = os.path.join(raw_sets_path, set_name)
        annotated_set_path = os.path.join(annotated_sets_path, set_name)

        set_exists = os.path.exists(annotated_set_path)
        if set_exists:
            if overwrite != "True":
                print("Set with name '{0}' already exists, skipping it. To overwrite existing sets, pass the argument --overwrite='True'.".format(set_name))
                continue
            else:
                shutil.rmtree(annotated_set_path)

        rawSet_exists = os.path.exists(raw_set_path)
        assert rawSet_exists, "Raw set with name '{0}' does not exist at '{1}'.".format(set_name, raw_set_path)

        shutil.unpack_archive(
            filename=zipped_file_path,
            extract_dir=annotated_set_path, 
            format='zip',
        )  

        removeMetadata(annotated_set_path)
        renameLabelsDirectory(annotated_set_path)

        copyImagesFromRawToAnnotatedSet(raw_set_path, annotated_set_path, image_extension)

        os.remove(zipped_file_path)
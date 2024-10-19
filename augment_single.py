import albumentations as A
import cv2
import argparse

parser = argparse.ArgumentParser(description='Augment an image.')
parser.add_argument('-i','--input', help='Path to the input image', required=True)
parser.add_argument('-o','--output', help='Path and filename of the exported image', required=True)
args = vars(parser.parse_args())

input_path = args['input']
output = args['output']

# Example inputs
# input_path = 'demo_image.png'
# output = 'augmented.png'


image = cv2.imread(input_path)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

transform = A.ElasticTransform(alpha=175, sigma=15, always_apply=True, border_mode=cv2.BORDER_CONSTANT, interpolation=cv2.INTER_CUBIC)
rbc = A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.1, always_apply=True)

augmented_image = transform(image=image)['image']
augmented_image = rbc(image=augmented_image)['image']

cv2.imwrite(output, augmented_image)
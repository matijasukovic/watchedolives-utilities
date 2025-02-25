from scipy.spatial import distance as dist
import argparse
import glob
import cv2
import os
import shutil
import math

parser = argparse.ArgumentParser(description="Given a dataset of images, compares them to a reference image by histogram values and sorts them to classes based on similarity")
parser.add_argument("-d", "--dataset_path", help = "Path to the directory with images", default=r"/Volumes/Matija_ExtH/WatchedOlives/WatchedOlives/example")
parser.add_argument("-r", "--reference_image_filename", help = "Filename of the reference image. Other images in the dataset will be compared to this one", default=r"good_olives.png")
parser.add_argument("-f", "--format", help = "Image format", default=r".png")
parser.add_argument("-o", "--output_path", help = "Path to the output directory", default=r"/Volumes/Matija_ExtH/WatchedOlives/WatchedOlives/output")

args = vars(parser.parse_args())

dataset_path = args['dataset_path']
reference_image_filename = args['reference_image_filename']
format = args['format']
output_path = args['output_path']

index = {}
images = {}

def print_progress_percent(iteration, total, message=""):
	LINE_UP = '\033[1A'
	LINE_CLEAR = '\x1b[2K'

	print("{0} {1}%".format(message, math.ceil(iteration / total * 100)))

	if (iteration + 1) != total:
		print(LINE_UP, end=LINE_CLEAR)

list_of_image_paths = glob.glob(dataset_path + "/*")
for i, image_path in enumerate(list_of_image_paths):
	print_progress_percent(
		i, len(list_of_image_paths), 
		message="Calculating histograms:"
	)

	filename = image_path[image_path.rfind("/") + 1:]
	image = cv2.imread(image_path)

	images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	
	hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
		[0, 256, 0, 256, 0, 256])
	hist = cv2.normalize(hist, hist).flatten()

	index[filename] = hist

# OpenCV distance methods: Correlation: cv2.HISTCMP_CORREL, Chi-Squared: cv2.HISTCMP_CHISQR, Intersection: cv2.HISTCMP_INTERSECT, Hellinger: cv2.HISTCMP_BHATTACHARYYA
# SciPy methods: Euclidean: dist.euclidean, Manhattan: dist.cityblock, Chebysev: dist.chebyshev

distance_method = dist.euclidean

results = {}

for i, (filename, histogram) in enumerate(index.items()):
	print_progress_percent(
		i, len(index), 
		message="Comparing histograms:"
	)
	
	distance = distance_method(index[reference_image_filename], histogram)
	results[filename] = distance

results = sorted([(distance, filename) for (filename, distance) in results.items()])

sorted_filenames = [filename for (distance, filename) in results]
length = len(sorted_filenames)

class_breakpoints = {
	'class1': int(length * 0.3),
	'class2': int(length * 0.8),
	'class3': length
}

os.mkdir(output_path)

previous_class_breakpoint = 0
for class_name, class_breakpoint in class_breakpoints.items():
	os.mkdir(os.path.join(output_path, class_name))

	filenames = sorted_filenames[previous_class_breakpoint:class_breakpoint]
	previous_class_breakpoint = class_breakpoint

	for i, filename in enumerate(filenames):
		print_progress_percent(i, len(filenames), message="Exporting class '{0}':".format(class_name))

		source = os.path.join(dataset_path, filename)
		destination = os.path.join(output_path, class_name, filename)

		shutil.copy2(source, destination)

		
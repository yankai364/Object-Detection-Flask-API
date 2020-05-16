import cv2
import matplotlib.pyplot as plt

from utils import *
from darknet import Darknet


def process(uploads_dir, plots_dir, filename):

    # Set the location and name of the cfg file
    cfg_file = './cfg/yolov3.cfg'

    # Set the location and name of the pre-trained weights file
    weight_file = './weights/yolov3.weights'

    # Set the location and name of the COCO object classes file
    namesfile = 'data/coco.names'

    # Load the network architecture
    m = Darknet(cfg_file)

    # Load the pre-trained weights
    m.load_weights(weight_file)

    # Load the COCO object classes
    class_names = load_class_names(namesfile)

    # Set the default figure size
    plt.rcParams['figure.figsize'] = [24.0, 14.0]

    # Set the NMS threshold
    nms_thresh = 0.6

    # Set the IOU threshold
    iou_thresh = 0.4

    # Set the default figure size
    plt.rcParams['figure.figsize'] = [24.0, 14.0]

    # Load the image
    img = cv2.imread(uploads_dir + '/' + filename + '.jpg')

    # Convert the image to RGB
    original_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # We resize the image to the input width and height of the first layer of the network.
    resized_image = cv2.resize(original_image, (m.width, m.height))

    # Set the IOU threshold. Default value is 0.4
    iou_thresh = 0.4

    # Set the NMS threshold. Default value is 0.6
    nms_thresh = 0.6

    # Detect objects in the image
    boxes = detect_objects(m, resized_image, iou_thresh, nms_thresh)

    # Print and save the objects found and their confidence levels
    objects_count, objects_confidence = print_objects(boxes, class_names)

    # Plot the image with bounding boxes and corresponding object class labels
    plot_boxes(original_image, boxes, class_names, plots_dir, filename)

    return objects_count, objects_confidence
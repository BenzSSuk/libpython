# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import time
import os
import pathlib
import tensorflow as tf

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
import glob
import pandas as pd
import cv2

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

# ----- User input
listRunType = ['VisualizeBox','ChopBox']
# print(listRunType)
print('Please select run type ?\n')
cr = 0
for ir in listRunType:
  cr = cr + 1
  print(f'{cr}: {ir}')
runTypeSelect = int(input('>'))
runType = listRunType[runTypeSelect-1]

pathExportedModel = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/exported-models/ssd_mobilenet_v1_fpn_640x640'
# pathExportedModel = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/exported-models/my_ssd_resnet50'

pathImg = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/Meter/ArtHome2/closeup'
# pathImg = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/Meter/BenzHome3'
pathImgOut = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/BoxMeter/ArtHome2_MobileNet_closeup'

if runType == 'VisualizeBox':
  pathImgVisual = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/images/Meter_VisualObject/ArtHome2_MobileNet_closeup'
  if not os.path.exists(pathImgVisual):
    os.makedirs(pathImgVisual)
  PATH_TO_LABELS = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/annotations/label_map.pbtxt'
  category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,use_display_name=True)

detectTH=0.7

# ----- Initialize, not edit
PATH_TO_SAVED_MODEL = pathExportedModel + "/saved_model"

listImg = glob.glob(pathImg + '/*.jpg')

if not os.path.exists(pathImgOut):
  os.makedirs(pathImgOut)

print('Loading model...')

start_time = time.time()
# Load saved model and build the detection function
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))

# %% [markdown]
# ## Load label

# %%

# %% [markdown]
# ## Plot test image

warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    img = Image.open(path)
    img_mode = img.mode

    return np.array(img), img_mode

# dfLabelOut  = pd.DataFrame(columns=['filename',])

# IMAGE_PATHS = glob.glob(pathImg)
nImgs = len(listImg)
countImg = 0
for image_path in listImg:
    # print('Running inference for {}... '.format(image_path), end='')
    print(f'i:{countImg+1}/{nImgs}')

    countImg = countImg + 1 
    filename = image_path.split('/')[-1]
    image_np, img_mode = load_image_into_numpy_array(image_path)

    # image_np.shape
    height,width,channel = image_np.shape
    if height < width:
      image_np = cv2.rotate(image_np, cv2.ROTATE_90_CLOCKWISE)
      height,width,channel = image_np.shape

    # Things to try:
    # Flip horizontally
    # image_np = np.fliplr(image_np).copy()

    # Convert image to grayscale
    # image_np = np.tile(
    #     np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

    # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    if runType == 'VisualizeBox':
      image_np_with_detections = image_np.copy()

      # filter detected object before plot
      #indexScore = detections['detection_scores'] > 0.7
      #detections['detection_scores'] = detections['detection_scores'][indexScore]

      viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=detectTH,
            agnostic_mode=False)

      # plt.figure(1)
      # plt.imshow(image_np_with_detections)
      # plt.show()

      # save image
      imOut = Image.fromarray(image_np_with_detections)
      imOut.save(pathImgVisual + '/' + filename)

    elif runType == 'ChopBox':
      # Chop box
      indexScore = (detections['detection_scores'] >= detectTH)
      detectBox = detections['detection_boxes'][indexScore]
      nBoxFound = len(detectBox)

      for ibox in range(nBoxFound):
          # get pixel 
          box_coor = detectBox[ibox]

          # Coordinate from function 
          # detections['detection_scores'] = [[ymin_1,xmin_1,ymax_1,xmax_1],
          #                                   [ymin_2,xmin_2,ymax_2,xmax_2],
          #                                   ....                          ]

          box_ymin = int(box_coor[0]*height)
          box_xmin = int(box_coor[1]*width)
          box_ymax = int(box_coor[2]*height)
          box_xmax = int(box_coor[3]*width)
          
          box_arr = image_np[box_ymin:box_ymax, box_xmin:box_xmax]
          # box_arr = image_np[box_xmin:box_xmax, box_ymin:box_ymax]
          
          # plt.figure(1)
          # plt.imshow(box_arr)
          # plt.show()

          imOut = Image.fromarray(box_arr)
          imOut.save(pathImgOut + '/' + str(ibox+1) + '_' + filename)

    # plt.figure()
    # plt.imshow(image_np_with_detections)
    # plt.show()
    # print('Done')
print('#--- Finished ---#')
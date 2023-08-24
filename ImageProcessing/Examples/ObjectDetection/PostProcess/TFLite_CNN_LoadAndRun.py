import numpy as np
import tensorflow as tf
import cv2 
import os

# Load the TFLite model and allocate tensors.
print('Load model tflite...')
# path_tflite = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/resnet50.tflite'
folderModel = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model/CustomCNN/20210809_01'
# path_tflite = os.path.join(folderModel,'Pretrained_mnist','mnist.tflite')
path_tflite = os.path.join(folderModel,'64_10_ep_300_batch_10_mata.tflite')

interpreter = tf.lite.Interpreter(model_path=path_tflite)

print('Allocating input...')
# just use to test with tflite that input shape = 1x1
# interpreter.resize_tensor_input(0, [1, 640, 640, 3], strict=True)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()

# Test the model on random input data.
input_shape = input_details[0]['shape']
img_tensor = np.zeros((input_shape),dtype='uint8')



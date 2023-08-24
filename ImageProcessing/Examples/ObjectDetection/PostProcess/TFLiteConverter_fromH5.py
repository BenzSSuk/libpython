import tensorflow as tf

modelName_h5 = '64_10_ep_300_batch_10.h5'
pathCNN_h5 = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model/CustomCNN/20210809_01'
modelName_tflite = modelName_h5.split('.')[0] + '.tflite'
pathTFLite = pathCNN_h5

model = tf.keras.models.load_model(pathCNN_h5 + '/' + modelName_h5)

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open(pathTFLite + '/' + modelName_tflite, 'wb') as f:
  f.write(tflite_model)



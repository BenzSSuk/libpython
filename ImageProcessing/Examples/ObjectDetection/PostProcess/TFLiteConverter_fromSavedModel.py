import tensorflow as tf

# listConvertType = ['Original', 'Float16_quant']
# print(f"Convert_type: {listConvertType}")
# convertType = input("Convert type: ")
# modelName = input("Model name: ")

# Convert the model
pathSavedModel = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/exported-models/ssd_mobilenet_v1_fpn_640x640/saved_model'
# pathSavedModel = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/exported-models/ssd_mobilenet_v1_fpn_640x640/tflite/saved_model'

folderSaveModel = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model'
modelName = 'ssd_resnet50_v1_fpn_640x640_.tflite'

converter = tf.lite.TFLiteConverter.from_saved_model(pathSavedModel)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]

# if convertType == listConvertType[0]:
#     # Original  
#     converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS, tf.lite.OpsSet.SELECT_TF_OPS]

# elif convertType == listConvertType[1]:
#     converter.optimizations = [tf.lite.Optimize.DEFAULT]
#     converter.target_spec.supported_types = [tf.float16]
#     converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]

tflite_model = converter.convert()

# Save the model
with open(folderSaveModel + '/' + modelName, 'wb') as f:
    f.write(tflite_model)

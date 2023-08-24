import tensorflow as tf

# Convert the model
pathSavedModel = '/Users/pannawis/Projects/TensorFlow/workspace/training_PowerMeter/exported-models/ssd_mobilenet_v1_fpn_640x640/saved_model'

folderSaveModel = '/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model'
modelName = 'ssd_mobilenet_v1_fpn_640x640_notGraph.tflite'

# ------ Load by concrete
# Load the SavedModel.
saved_model_obj = tf.saved_model.load(export_dir=pathSavedModel)

# Load the specific concrete function from the SavedModel.
concrete_func = saved_model_obj.signatures['serving_default']

# Set the shape of the input in the concrete function.
concrete_func.inputs[0].set_shape([1,640,640,3])

# Convert the model to a TFLite model.
converter =  tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])
converter.optimizations =  [tf.lite.Optimize.DEFAULT]
# converter.target_spec.supported_types = [tf.float16]
converter.target_spec.supported_ops = [ tf.lite.OpsSet.TFLITE_BUILTINS, # enable TensorFlow Lite ops.
                                        tf.lite.OpsSet.SELECT_TF_OPS] # enable TensorFlow ops.
converter.allow_custom_ops = True

# convert to tensorflow model
tflite_model = converter.convert()

# Save the model
print('Writing model...')
with open(folderSaveModel + '/' + modelName, 'wb') as f:
    f.write(tflite_model)

print('# ---- Finished ! ---- #')
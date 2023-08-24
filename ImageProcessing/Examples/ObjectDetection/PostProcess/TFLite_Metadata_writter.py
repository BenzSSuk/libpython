from tflite_support.metadata_writers import object_detector
from tflite_support.metadata_writers import writer_utils
from tflite_support import metadata as _metadata
from tflite_support import metadata_schema_py_generated as _metadata_fb
import os
import tensorflow as tf
import flatbuffers

ObjectDetectorWriter = object_detector.MetadataWriter
# modelName = 'ssd_resnet50_v1_fpn_640x640.tflite'
# pathModel = "/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model/ssd_resnet50_v1_fpn_640x640.tflite"
pathModel = input('pathModel: ')

# Task Library expects label files that are in the same format as the one below.
# pathLabel = "/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/ssd_mobilenet_labels.txt"
pathLabel = input('pathLabel: ')

modelName = pathModel.split('/')[0]
modelNameWithoutExtend = modelName.split('.')[0]
modelName_meta = modelNameWithoutExtend + '_meta.tflite'

pathSave = "/Users/pannawis/Projects/01_SmartMeter/SmartPowerMeter_SW/trained_model"

# -------------- Pack to tflite -----------------
# Load model tflite
# model_tflite = tf.lite.Interpreter(pathModel)

""" ... """
"""Creates the metadata for an image classifier."""

# Creates model info.
model_meta = _metadata_fb.ModelMetadataT()
model_meta.name = "Keras CNN 64 filters - 10 softmaxs"
model_meta.description = ("Image classification of binary single digit 0 - 9")
model_meta.version = "v1"
model_meta.author = "TensorFlow.keras"
model_meta.license = ("Apache License. Version 2.0 "
                      "http://www.apache.org/licenses/LICENSE-2.0.")

# Creates input info.
input_meta = _metadata_fb.TensorMetadataT()

# Creates output info.
output_meta = _metadata_fb.TensorMetadataT()

input_meta.name = "image"
input_meta.description = (
    "Input image to be classified. The expected image is binary 0 {0} x {1}, with "
    "binary per pixel. Each value in the "
    "tensor is a single byte between 0 and 255.".format(55, 43))
input_meta.content = _metadata_fb.ContentT()
input_meta.content.contentProperties = _metadata_fb.ImagePropertiesT()
input_meta.content.contentProperties.colorSpace = (
    _metadata_fb.ColorSpaceType.RGB)
input_meta.content.contentPropertiesType = (
    _metadata_fb.ContentProperties.ImageProperties)
input_normalization = _metadata_fb.ProcessUnitT()
input_normalization.optionsType = (
    _metadata_fb.ProcessUnitOptions.NormalizationOptions)
input_normalization.options = _metadata_fb.NormalizationOptionsT()
input_normalization.options.mean = [127.5]
input_normalization.options.std = [127.5]
input_meta.processUnits = [input_normalization]
input_stats = _metadata_fb.StatsT()
input_stats.max = [255]
input_stats.min = [0]
input_meta.stats = input_stats

output_meta = _metadata_fb.TensorMetadataT()
output_meta.name = "probability"
output_meta.description = "Probabilities of the 1001 labels respectively."
output_meta.content = _metadata_fb.ContentT()
output_meta.content.content_properties = _metadata_fb.FeaturePropertiesT()
output_meta.content.contentPropertiesType = (
    _metadata_fb.ContentProperties.FeatureProperties)
output_stats = _metadata_fb.StatsT()
output_stats.max = [1.0]
output_stats.min = [0.0]
output_meta.stats = output_stats
label_file = _metadata_fb.AssociatedFileT()
label_file.name = os.path.basename(pathLabel)
label_file.description = "Binary single digit 0 - 9"
label_file.type = _metadata_fb.AssociatedFileType.TENSOR_AXIS_LABELS
output_meta.associatedFiles = [label_file]

# Creates subgraph info.
subgraph = _metadata_fb.SubGraphMetadataT()
subgraph.inputTensorMetadata = [input_meta]
subgraph.outputTensorMetadata = [output_meta]
model_meta.subgraphMetadata = [subgraph]

b = flatbuffers.Builder(0)
b.Finish(
    model_meta.Pack(b),
    _metadata.MetadataPopulator.METADATA_FILE_IDENTIFIER)
metadata_buf = b.Output()

populator = _metadata.MetadataPopulator.with_model_file(pathModel)
populator.load_metadata_buffer(metadata_buf)
populator.load_associated_files([pathLabel])
populator.populate(modelName_meta)
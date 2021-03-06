import os
import tensorflow as tf
from utils.models_download import download_model
from segmentation.src.fit import predict
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def main_segmentation(input_filename, output_folder, model_name, brain_mask_filepath=None, gpu_device='-1'):
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = gpu_device

    download_model(model_name=model_name)
    predict(input_filename=input_filename, output_path=output_folder, selected_model=model_name,
            brain_mask_filename=brain_mask_filepath)
    tf.keras.backend.clear_session()

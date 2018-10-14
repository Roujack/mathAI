import os
import cv2
import numpy as np
from config import *
import tensorflow as tf
from tools.cnn_model import cnn_symbol_classifier
from tools.image_input import *



# def main(unused_argv):
train_data,train_data_labels = read_img_file('train')
eval_data,eval_data_labels = read_img_file('eval')

# set up logging for predictions
# log the values in the "softmax" tensor with label "probabilities"
tensors_to_log = {"probabilities": "softmax_tensor"}
logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)
#这是训练cnn模型的，如果需要继续训练，则去除下面的注释，一般情况下不需要再训练
# # train the model
# train_input_fn = tf.estimator.inputs.numpy_input_fn(
#     x={"x": train_data},
#     y=train_data_labels,
#     batch_size=100,
#     num_epochs=None,
#     shuffle=True)
# # print(train_input_fn)
# cnn_symbol_classifier.train(
#     input_fn=train_input_fn,
#     steps=TRAINING_STEPS,
#     hooks=[logging_hook])

# evaluate the model and print results
eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    x={"x": eval_data},
    y=eval_data_labels,
    num_epochs=1,
    shuffle=False)
eval_results = cnn_symbol_classifier.evaluate(input_fn=eval_input_fn)
print(eval_results)
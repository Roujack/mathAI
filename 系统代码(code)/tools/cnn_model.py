from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from config import MODEL_DIR,SYMBOLS
from tools.image_input import read_img_file
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
tf.logging.set_verbosity(tf.logging.INFO)
def cnn_model_fn(features, labels, mode):
  """Model function for CNN."""
  # Input Layer
  # Reshape X to 4-D tensor: [batch_size, width, height, channels]
  # MNIST images are 28x28 pixels, and have one color channel
  input_layer = tf.reshape(features["x"], [-1, 45, 45, 1])

  # Convolutional Layer #1
  # Computes 32 features using a 5x5 filter with ReLU activation.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 28, 28, 1]
  # Output Tensor Shape: [batch_size, 28, 28, 32]
  conv1 = tf.layers.conv2d(
      inputs=input_layer,
      filters=32,
      kernel_size=[3, 3],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #1
  # First max pooling layer with a 3x3 filter and stride of 3
  # Input Tensor Shape: [batch_size, 45, 45, 32]
  # Output Tensor Shape: [batch_size, 15, 15, 32]
  pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=3)

  # Convolutional Layer #2
  # Computes 64 features using a 5x5 filter.
  # Padding is added to preserve width and height.
  # Input Tensor Shape: [batch_size, 15, 15, 32]
  # Output Tensor Shape: [batch_size, 15, 15, 64]
  conv2 = tf.layers.conv2d(
      inputs=pool1,
      filters=64,
      kernel_size=[3, 3],
      padding="same",
      activation=tf.nn.relu)

  # Pooling Layer #2
  # Second max pooling layer with a 3x3 filter and stride of 3
  # Input Tensor Shape: [batch_size, 15, 15, 64]
  # Output Tensor Shape: [batch_size, 5, 5, 64]
  pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[3, 3], strides=3)

  # Flatten tensor into a batch of vectors
  # Input Tensor Shape: [batch_size, 5, 5, 64]
  # Output Tensor Shape: [batch_size, 5 * 5 * 64]
  pool2_flat = tf.reshape(pool2, [-1, 5 * 5 * 64])

  # Dense Layer
  # Densely connected layer with 1024 neurons
  # Input Tensor Shape: [batch_size, 5 * 5 * 64]
  # Output Tensor Shape: [batch_size, 1024]
  dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)

  # Add dropout operation; 0.6 probability that element will be kept
  dropout = tf.layers.dropout(
      inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)

  # Logits layer
  # Input Tensor Shape: [batch_size, 1024]
  # Output Tensor Shape: [batch_size, 32]
  logits = tf.layers.dense(inputs=dropout, units=32)

  predictions = {
      # Generate predictions (for PREDICT and EVAL mode)
      "classes": tf.argmax(input=logits, axis=1),
      # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
      # `logging_hook`.
      "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
  }
  if mode == tf.estimator.ModeKeys.PREDICT:
    # sess = tf.InteractiveSession()
    # print('logits:',logits.eval(session = sess))
    return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

  # Calculate Loss (for both TRAIN and EVAL modes)
  loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)

  # Configure the Training Op (for TRAIN mode)
  if mode == tf.estimator.ModeKeys.TRAIN:
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
    train_op = optimizer.minimize(
        loss=loss,
        global_step=tf.train.get_global_step())
    return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)

  # Add evaluation metrics (for EVAL mode)
  eval_metric_ops = {
      "accuracy": tf.metrics.accuracy(
          labels=labels, predictions=predictions["classes"])}
  return tf.estimator.EstimatorSpec(
      mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)
# def cnn_model_fn(features, labels, mode):
#   """Model function for CNN."""
#   # Input Layer
#   # Reshape X to 4-D tensor: [batch_size, width, height, channels]
#   # MNIST images are 28x28 pixels, and have one color channel
#   input_layer = tf.reshape(features["x"], [-1, 45, 45, 1])
#
#   # Convolutional Layer #1
#   # Computes 32 features using a 5x5 filter with ReLU activation.
#   # Padding is added to preserve width and height.
#   # Input Tensor Shape: [batch_size, 28, 28, 1]
#   # Output Tensor Shape: [batch_size, 28, 28, 32]
#   conv1 = tf.layers.conv2d(
#       inputs=input_layer,
#       filters=32,
#       kernel_size=[5, 5],
#       padding="same",
#       activation=tf.nn.relu)
#
#   # Pooling Layer #1
#   # First max pooling layer with a 3x3 filter and stride of 3
#   # Input Tensor Shape: [batch_size, 45, 45, 32]
#   # Output Tensor Shape: [batch_size, 15, 15, 32]
#   pool1 = tf.layers.max_pooling2d(inputs=conv1, pool_size=[3, 3], strides=3)
#
#   # Convolutional Layer #2
#   # Computes 64 features using a 5x5 filter.
#   # Padding is added to preserve width and height.
#   # Input Tensor Shape: [batch_size, 15, 15, 32]
#   # Output Tensor Shape: [batch_size, 15, 15, 64]
#   conv2 = tf.layers.conv2d(
#       inputs=pool1,
#       filters=64,
#       kernel_size=[5, 5],
#       padding="same",
#       activation=tf.nn.relu)
#
#   # Pooling Layer #2
#   # Second max pooling layer with a 3x3 filter and stride of 3
#   # Input Tensor Shape: [batch_size, 15, 15, 64]
#   # Output Tensor Shape: [batch_size, 5, 5, 64]
#   pool2 = tf.layers.max_pooling2d(inputs=conv2, pool_size=[3, 3], strides=3)
#
#   # Flatten tensor into a batch of vectors
#   # Input Tensor Shape: [batch_size, 5, 5, 64]
#   # Output Tensor Shape: [batch_size, 5 * 5 * 64]
#   pool2_flat = tf.reshape(pool2, [-1, 5 * 5 * 64])
#
#   # Dense Layer
#   # Densely connected layer with 1024 neurons
#   # Input Tensor Shape: [batch_size, 5 * 5 * 64]
#   # Output Tensor Shape: [batch_size, 1024]
#   dense = tf.layers.dense(inputs=pool2_flat, units=1024, activation=tf.nn.relu)
#
#   # Add dropout operation; 0.6 probability that element will be kept
#   dropout = tf.layers.dropout(
#       inputs=dense, rate=0.4, training=mode == tf.estimator.ModeKeys.TRAIN)
#
#   # Logits layer
#   # Input Tensor Shape: [batch_size, 1024]
#   # Output Tensor Shape: [batch_size, 32]
#   logits = tf.layers.dense(inputs=dropout, units=32)
#
#   predictions = {
#       # Generate predictions (for PREDICT and EVAL mode)
#       "classes": tf.argmax(input=logits, axis=1),
#       # Add `softmax_tensor` to the graph. It is used for PREDICT and by the
#       # `logging_hook`.
#       "probabilities": tf.nn.softmax(logits, name="softmax_tensor")
#   }
#   if mode == tf.estimator.ModeKeys.PREDICT:
#     return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)
#
#   # Calculate Loss (for both TRAIN and EVAL modes)
#   loss = tf.losses.sparse_softmax_cross_entropy(labels=labels, logits=logits)
#
#   # Configure the Training Op (for TRAIN mode)
#   if mode == tf.estimator.ModeKeys.TRAIN:
#     optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001)
#     train_op = optimizer.minimize(
#         loss=loss,
#         global_step=tf.train.get_global_step())
#     return tf.estimator.EstimatorSpec(mode=mode, loss=loss, train_op=train_op)
#
#   # Add evaluation metrics (for EVAL mode)
#   eval_metric_ops = {
#       "accuracy": tf.metrics.accuracy(
#           labels=labels, predictions=predictions["classes"])}
#   return tf.estimator.EstimatorSpec(
#       mode=mode, loss=loss, eval_metric_ops=eval_metric_ops)


# 定义一个分类器供其他模块引用
# create the estimator
cnn_symbol_classifier = tf.estimator.Estimator(
  model_fn=cnn_model_fn, model_dir=MODEL_DIR)

# cnn分类器训练函数
def train_cnn_model(steps):
    train_data,train_data_labels = read_img_file('train')

    # set up logging for predictions
    # log the values in the "softmax" tensor with label "probabilities"
    tensors_to_log = {"probabilities": "softmax_tensor"}
    logging_hook = tf.train.LoggingTensorHook(tensors=tensors_to_log, every_n_iter=50)

    # train the model
    train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": train_data},
        y=train_data_labels,
        batch_size=100,
        num_epochs=None,
        shuffle=True)
    print(train_input_fn)
    cnn_symbol_classifier.train(
        input_fn=train_input_fn,
        steps=steps,
        hooks=[logging_hook])

def eval_cnn_model():
    eval_data, eval_data_labels, filelist = read_img_file('eval')
    # evaluate the model and print results
    eval_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={"x": eval_data},
        y=eval_data_labels,
        num_epochs=1,
        shuffle=False)
    eval_results = cnn_symbol_classifier.evaluate(input_fn=eval_input_fn)
    print(eval_results)

if __name__ == "__main__":
  tf.app.run()
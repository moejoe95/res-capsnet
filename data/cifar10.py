
import numpy as np
import tensorflow as tf
import tensorflow_addons as tfa
import tensorflow_datasets as tfds
from tensorflow import keras



HEIGHT = 32
WIDTH = 32
DEPTH = 3


def create_cifar10(args):
    args.img_width = WIDTH
    args.img_height = HEIGHT
    args.img_depth = DEPTH

    train_ds = tfds.load(name="cifar10", split="train", as_supervised=True)
    test_ds = tfds.load(name="cifar10", split="test", as_supervised=True)
    train_ds = (train_ds
        .map(_augmentation)
        .shuffle(buffer_size=50000)
        .map(_normalize)
        .batch(args.batch_size, drop_remainder=True))

    test_ds = (test_ds
        .map(_no_augmentation)
        .shuffle(buffer_size=10000)
        .map(_normalize)
        .batch(32, drop_remainder=True))

    class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return train_ds, test_ds, class_names


def _augmentation(x, y):
    x = tf.image.convert_image_dtype(x, tf.float32)
    x = tf.image.random_crop(x, size=[HEIGHT, WIDTH, DEPTH])
    x = tf.image.random_brightness(x, max_delta=0.25)
    return x, y


def _no_augmentation(x, y):
    x = tf.image.convert_image_dtype(x, tf.float32)
    x = tf.image.resize_with_crop_or_pad(x, HEIGHT, WIDTH)
    return x, y


def _normalize(x, y):
    x = tf.image.per_image_standardization(x)
    y = tf.cast(y, tf.int32)
    return x, y
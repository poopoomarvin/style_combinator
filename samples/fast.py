#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: fast.py
# Author: Qian Ge <geqian1001@gmail.com>
# python3 fast.py --train \
#    --batch BATCH_SIZE \
#    --lr LEARNING_RATE \
#    --styleim FILE_NAME_OF_STYPE_IMAGE \
#
# python3 fast.py --generate_image \
#    --input_path TEST_IMAGE_PATH_AND_NAME \
#    --loadstyle STYLE_NAME(wave, oil ...) \
#    --save_path PATH_AND_NAME_FOR_SAVING
import os
import argparse
import platform
import imageio
import scipy.misc
import numpy as np
import tensorflow as tf
from tensorcv.dataflow.image import ImageFromFile

import sys
sys.path.append('../')
from lib.models.faststyle import FastStyle
import lib.utils.image as imagetool

DATA_PATH = '../data/dataset/COCO/train2014/'
SAVE_PATH = '../data/models/'
VGG_PATH = '../data/pretrain/vgg/vgg19.npy'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', action='store_true',
                        help='Train the model')
    parser.add_argument('--generate_image', action='store_true',
                        help='generate image')
    parser.add_argument('--generate_video', action='store_true',
                        help='generate image')

    parser.add_argument('--batch', default=1, type=int,
                        help='Batch size')
    parser.add_argument('--lr', default=1e-3, type=float,
                        help='Learning rate')

    parser.add_argument('--style', default=10, type=float,
                        help='Style weight')
    parser.add_argument('--content', default=15, type=float,
                        help='Content weight')
    parser.add_argument('--tv', default=1e-4, type=float,
                        help='TV weight')

    parser.add_argument('--styleim', default='la_muse.jpg', type=str,
                        help='Style image name')
    parser.add_argument('--loadstyle', default='oil', type=str,
                        help='Load pretrained style transfer model')
    parser.add_argument('--input_path', default='../data/cat.png', type=str,
                        help='test image path')
    parser.add_argument('--save_path', default='../data/transfered.png', type=str,
                        help='save image path')

    return parser.parse_args()

# rain s 5 c 20 tv 1e-4

# other s 5 c 15 tv 1e-4

def train():
    FLAGS = get_args()
    style_name = os.path.splitext(FLAGS.styleim)[0]
    style_im = scipy.misc.imread('../data/{}'.format(FLAGS.styleim))
    style_im = [imagetool.resize_image_with_smallest_side(style_im, 512)]
    style_shape = [style_im[0].shape[0], style_im[0].shape[1]]

    train_data = ImageFromFile(
        ext_name='.jpg',
        data_dir=DATA_PATH,
        num_channel=3,
        shuffle=True,
        batch_dict_name=['im'],
        pf=imagetool.im_normalize)
    train_data.setup(epoch_val=0, batch_size=FLAGS.batch)

    test_im = scipy.misc.imread('../data/cat.png')
    test_im = [test_im]

    train_model = FastStyle(content_size=256,
                            style_size=style_shape,
                            c_channel=3,
                            s_channel=3,
                            vgg_path=VGG_PATH,
                            s_weight=FLAGS.style,
                            c_weight=FLAGS.content,
                            tv_weight=FLAGS.tv)

    train_model.create_train_model()

    generate_model = FastStyle(c_channel=3)
    generate_model.create_generate_model()

    writer = tf.summary.FileWriter(SAVE_PATH)
    saver = tf.train.Saver(
        var_list=tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='style_net'))
    sessconfig = tf.ConfigProto()
    sessconfig.gpu_options.allow_growth = True
    with tf.Session(config=sessconfig) as sess:
        sess.run(tf.global_variables_initializer(), feed_dict={train_model.style_image: style_im})
        writer.add_graph(sess.graph)
        # 40000 steps
        for i in range(400):
            train_model.train(sess, train_data, num_iteration=100, summary_writer=writer)
            generate_model.generate(sess, test_im, summary_writer=writer)
            saver.save(sess, '{}{}_step_{}'.format(SAVE_PATH, style_name, i))
    writer.close()

# def generate_image(input_path = get_args().input_path, loadstyle = get_args().loadstyle, save_path = get_args().save_path):
def generate_image(input_path, loadstyle, save_path):
    # FLAGS = get_args()

    model = FastStyle(c_channel=3)
    model.create_generate_model()

    test_im = [scipy.misc.imread(input_path)]
    saver = tf.train.Saver(
        var_list=tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='style_net'))
    sessconfig = tf.ConfigProto()
    sessconfig.gpu_options.allow_growth = True
    with tf.Session(config=sessconfig) as sess:
        sess.run(tf.global_variables_initializer())
        saver.restore(sess, '{}{}'.format(SAVE_PATH, loadstyle))
        model.generate(sess, test_im, save_name=save_path)

def generate_video():
    FLAGS = get_args()

    vid = imageio.get_reader(FLAGS.input_path,  'ffmpeg')
    fps = vid.get_meta_data()['fps']
    print('Video loaded (fps: {}.'.format(fps))
    writer = imageio.get_writer(FLAGS.save_path, fps=fps)

    model = FastStyle(c_channel=3)
    model.create_generate_model()

    saver = tf.train.Saver(
        var_list=tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='style_net'))
    sessconfig = tf.ConfigProto()
    sessconfig.gpu_options.allow_growth = True

    save_path = '../data/'
    with tf.Session(config=sessconfig) as sess:
        sess.run(tf.global_variables_initializer())
        frame_id = 0
        for image in vid.iter_data():
            frame_id += 1
            print('process frame {}'.format(frame_id))
            saver.restore(sess, '{}{}'.format(SAVE_PATH, FLAGS.loadstyle))
            # image = scipy.misc.imresize(image, (368, 640))
            transferred_im = model.generate(sess, [image])[0]
            writer.append_data(transferred_im.astype(np.uint8))

    writer.close()


if __name__ == '__main__':
    FLAGS = get_args()

    if FLAGS.train:
        train()
    if FLAGS.generate_image:
        generate_image()
    if FLAGS.generate_video:
        generate_video()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: image.py
# Author: Qian Ge <geqian1001@gmail.com>

import scipy.misc
import numpy as np
from PIL import Image

def resize_image_with_smallest_side(image, small_size):
    """
    Resize single image array with smallest side = small_size and
    keep the original aspect ratio.
    Args:
        image (np.array): 2-D image of shape
            [height, width] or 3-D image of shape
            [height, width, channels] or 4-D of shape
            [1, height, width, channels].
        small_size (int): A 1-D int. The smallest side of resize image.
    """
    im_shape = image.shape
    shape_dim = len(im_shape)
    assert shape_dim <= 4 and shape_dim >= 2,\
        'Wrong format of image!Shape is {}'.format(im_shape)

    if shape_dim == 4:
        image = np.squeeze(image, axis=0)
        height = float(im_shape[1])
        width = float(im_shape[2])
    else:
        height = float(im_shape[0])
        width = float(im_shape[1])

    if height <= width:
        new_height = int(small_size)
        new_width = int(new_height/height * width)
    else:
        new_width = int(small_size)
        new_height = int(new_width/width * height)

    if shape_dim == 2:
        # im = np.array(Image.fromarray(image).resize((new_height, new_width)))
        im = scipy.misc.imresize(image, (new_height, new_width))
    elif shape_dim == 3:
        # im = np.array(Image.fromarray(image).resize((new_height, new_width, image.shape[2])))
        im = scipy.misc.imresize(image, (new_height, new_width, image.shape[2]))
    else:
        # im = np.array(Image.fromarray(image).resize((new_height, new_width, image.shape[3])))
        im = scipy.misc.imresize(image, (new_height, new_width, im_shape[3]))
        im = np.expand_dims(im, axis=0)

    return im

def im_normalize(im):
    return scipy.misc.imresize(im, [256, 256])

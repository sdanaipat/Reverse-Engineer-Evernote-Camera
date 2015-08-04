import numpy as np
from skimage.color import rgb2gray
from skimage.filters import threshold_adaptive
from skimage.morphology import dilation
from skimage.morphology import rectangle


def text_segments(img, min_h=20, max_h=50):
    gray_scale_img = rgb2gray(img)
    gray_scale_img /= gray_scale_img.max()
    gray_scale_img *= 255

    binarized_adaptive_img = threshold_adaptive(gray_scale_img, block_size=40, offset=20)
    dilated = dilation(~binarized_adaptive_img, rectangle(1, 15))
    for segment in extract_segments(dilated.copy()):
        if min_h < height(segment) < max_h:
            yield segment


def height(segment):
    return segment[2] - segment[0]


def segment(img, i, j):
    s = [(i, j)]
    topleft_i, topleft_j, bottomright_i, bottomright_j = i, j, 0, 0
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    while s:
        i, j = s.pop()
        topleft_i = min(topleft_i, i)
        topleft_j = min(topleft_j, j)
        bottomright_i = max(bottomright_i, i)
        bottomright_j = max(bottomright_j, j)
        img[i, j] = False
        for d in directions:
            ii = i + d[0]
            jj = j + d[1]
            if ii >= 0 and ii < img.shape[0] and jj >= 0 and jj < img.shape[1] and img[ii, jj]:
                s.append((ii, jj))
    return topleft_i, topleft_j, bottomright_i, bottomright_j


def extract_segments(img):
    segments = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j]:
                segments.append(segment(img, i, j))
    return np.array(segments)

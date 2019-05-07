import os
import time
import cv2
import imutils
import numpy as np

DIR = './pics'
R_WIDTH = 8400
WIDTH = 8002
HEIGHT = 4001
BLACK_COLOR = 25
RESULT = './result.jpg'
files = os.listdir(DIR)

def stitch(files):
    imgs = []
    for file in files:
        imgs.append(cv2.imread(DIR + '/' + file))
    try_use_gpu = False
    stitcher = cv2.createStitcher(try_use_gpu)
    status, pano = stitcher.stitch(imgs)
    if status == 0:
        return pano
    else:
        return None

def crop(img):
    width, height = img.shape[1], img.shape[0]
    if width > R_WIDTH:
        img = imutils.resize(img, width=R_WIDTH)
        width, height = img.shape[1], img.shape[0]

    top, bottom = 0, height
    limit = int(height/8)
    top_limit = limit
    bottom_limit = height - limit

    # top
    c = 0
    while c < width:
        r = 0
        while r < top_limit:
            if sum(img[r,c]) < BLACK_COLOR:
                r = r + 1
            else:
                if r > top:
                    top = r
                break
        c = c + 1
    top = top + 1

    # bottom
    c = 0
    while c < width:
        r = height - 1
        while r > bottom_limit:
            if sum(img[r,c]) < BLACK_COLOR:
                r = r - 1
            else:
                if r < bottom:
                    bottom = r
                break
        c = c + 1
    bottom = bottom -1

    tmp = img[top:bottom, 0:width]
    width, height = tmp.shape[1], tmp.shape[0]
    limit = int(height/8)
    left, right = 0, width
    left_limit = limit
    right_limit = width - limit

    # left
    r = 0
    while r < height:
        c = 0
        while c < left_limit:
            if sum(tmp[r,c]) < BLACK_COLOR:
                c = c + 1
            else:
                if c > left:
                    left = c
                break
        r = r + 1

    # right
    r = 0
    while r < height:
        c = width - 1
        while c > right_limit:
            if sum(tmp[r,c]) < BLACK_COLOR:
                c = c - 1
            else:
                if c < right:
                    right = c
                break
        r = r + 1

    tmp = tmp[0:height, left:right]
    return tmp

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

#!/usr/bin/env python2.7

import numpy as np
import cv2

img = cv2.imread('input.jpeg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150, apertureSize=3)
h, w = edges.shape
print edges.shape

for i in xrange(0,h-1):
    for j in xrange(0,w-1):
        l = edges[i+1, j]
        d = edges[i, j+1]
        c = edges[i, j]
        edges[i, j] = max(l, d, c)

backtorgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

h, w = backtorgb.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
cv2.floodFill(backtorgb, mask, (0,0), 255)

cv2.imshow('edges', backtorgb)

cv2.waitKey(0)
cv2.destroyAllWindows()

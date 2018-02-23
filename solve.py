#!/usr/bin/env python2.7

import os
import numpy as np
import cv2
import shutil
import pickle

OUT_DIR = 'data'
INPUT_IMG = 'input.jpeg'

img = cv2.imread(INPUT_IMG)
origImg = np.copy(img)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150, apertureSize=3)
h, w = edges.shape

for i in xrange(0,h-1):
    for j in xrange(0,w-1):
        l = edges[i+1, j]
        d = edges[i, j+1]
        c = edges[i, j]
        edges[i, j] = max(l, d, c)

#backtorgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

h, w = edges.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)
cv2.floodFill(edges, mask, (0,0), 42)

for i in xrange(0,h-1):
    for j in xrange(0,w-1):
        c = edges[i, j]
        if c != 42:
            edges[i, j] = 255
        else:
            edges[i, j] = 0

#edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
_, contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print 'total:', len(contours)

#cv2.drawContours(img, contours, -1, (0,255,0), 3)

mask = np.zeros((h, w), np.uint8)

shutil.rmtree(OUT_DIR, ignore_errors=True)
os.makedirs(OUT_DIR)

n = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 1000:
        continue

    #print cnt
    #cv2.drawContours(img, [cnt], 0, (255, 0, 0), 1)

    hull = cv2.convexHull(cnt)
    print 'size:', len(cnt), len(hull)

    cv2.drawContours(img, [hull], 0, (255, 0, 0), 3)
    cv2.drawContours(mask, [hull], 0, 255, -1)

    currMask = np.zeros((h, w), np.uint8)
    cv2.drawContours(currMask, [hull], 0, 255, -1)

    cx, cy, cw, ch = cv2.boundingRect(hull)
    currImg = np.zeros((ch, cw, 4), np.uint8)
    for i in xrange(ch):
        for j in xrange(cw):
            oi = cy + i
            oj = cx + j
            if currMask[oi, oj] == 255:
                currImg[i, j] = tuple(origImg[oi, oj]) + (255,)

    points = []
    for point in hull:
        ccx, ccy = tuple(point[0])
        ccx -= cx
        ccy -= cy
        points.append((ccx, ccy))

    cv2.imwrite(OUT_DIR + '/out_%d.png' % n, currImg, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    with open(OUT_DIR + '/out_%d.bin' % n, 'wb') as f:
        f.write(pickle.dumps(points))

    #cv2.imshow('curr', currImg)
    #cv2.waitKey(0)

    #cv2.rectangle(img, (cx, cy), (cx + cw, cy + ch), (0, 255, 0), 2)

    # if area < 2000 or area > 4000:
    #     continue

    # if len(cnt) < 5:
    #     continue

    #ellipse = cv2.fitEllipse(cnt)
    #cv2.ellipse(img, ellipse, (0,255,0), 2)

    # epsilon = 0.1 * cv2.arcLength(cnt, True)
    # approx = cv2.approxPolyDP(cnt, epsilon, True)
    # print ' === approx:'
    # print approx
    n += 1

for i in xrange(0,h):
    for j in xrange(0,w):
        if mask[i,j] != 255:
            img[i,j] = (255, 255, 255)

cv2.imshow('edges', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

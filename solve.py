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

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 1000:
        continue
    #print cnt
    #cv2.drawContours(img, [cnt], 0, (255, 0, 0), 1)

    hull = cv2.convexHull(cnt)
    cv2.drawContours(img, [hull], 0, (255, 0, 0), 3)
    cv2.drawContours(mask, [hull], 0, 255, -1)

    print 'size:', len(cnt), len(hull)

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

for i in xrange(0,h):
    for j in xrange(0,w):
        if mask[i,j] != 255:
            img[i,j] = (255, 255, 255)

cv2.imshow('edges', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

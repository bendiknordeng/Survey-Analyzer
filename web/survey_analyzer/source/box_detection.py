import cv2
import os
import sys
import numpy as np
import pickle

#find angle of corner
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def merge_close_points(cnt):
	keep = np.ones(np.shape(cnt)[0], dtype=int)
	for i in range(len(cnt)):
		for j in range(i+1, len(cnt)):
			if keep[j] == 0:
				continue
			if np.abs(cnt[i][0] - cnt[j][0]) < 4 and np.abs(cnt[i][1] - cnt[j][1]) < 4:
				keep[j] = 0
	return cnt[keep == 1]

def find_squares(contours):
    squares = []
    for cnt in contours:
		#approximate conour by polygon using a pressicion of 2% arc length.
        cnt_len = cv2.arcLength(cnt, True)
        cnt = cv2.approxPolyDP(cnt, 0.05*cnt_len, True)
        cnt = cnt.reshape(-1, 2)

        cnt = merge_close_points(cnt)

        #if polygon has 4 edges, area bigger than 100 and is convex, then it is a box
        #if abs(w-h) < 50 and len(cnt) == 4 and 1000 > cv2.contourArea(cnt) > 600 :#and cv2.isContourConvex(cnt):
        if len(cnt) == 4 and 1000 > cv2.contourArea(cnt) > 50 :#and cv2.isContourConvex(cnt):
            #if angle is close to 90 deg add it
            #max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
            if True:#max_cos < 0.2:
                squares.append(cnt)
    return np.array(squares)

def box_detection(image):
    # Find Canny edges
    edged = cv2.Canny(image, 100, 255)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #find which countours are squares and discard the rest
    squares = find_squares(contours)
    return boxes_to_images(image, squares)

def boxes_to_images(image, boxes):
    images = {}
    for box in boxes:
        y1 = np.min(box[:,1]) + 4
        y2 = np.max(box[:,1]) - 4
        x1 = np.min(box[:,0]) + 4
        x2 = np.max(box[:,0]) - 4
        if y2 > y1 and x2 > x1:
            images[x1] = (image[y1:y2, x1:x2])
    return [images[x] for x in sorted(images.keys())]

if __name__ == '__main__':
	i=2
	img = cv2.imread('data/survey' + str(i) + '.jpg')

	scale_percent = 30. # percent of original size
	width = int(img.shape[1] * scale_percent / 100)
	height = int(img.shape[0] * scale_percent / 100)
	dim = (width, height)
	# resize image
	resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

	_, cont, sq = box_detection(resized)
	with open('squares.bin', 'wb') as f:
		pickle.dump(sq, f)

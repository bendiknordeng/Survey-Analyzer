import cv2
import os
import sys
import numpy as np
import pickle

boxlocations = np.array([
       [ 300,  525],
       [ 400,  525],
       [ 670,  525],
       [ 730,  525],
       [ 790,  525],
       [1265,  525],
       [1335,  525],
       [ 652,  705],
       [ 787,  705],
       [ 945,  705],
       [1110,  705],
       [1263,  705],
       [ 652,  778],
       [ 787,  778],
       [ 945,  778],
       [1110,  778],
       [1263,  778],
       [ 652,  853],
       [ 787,  853],
       [ 945,  853],
       [1110,  853],
       [1263,  853],
       [ 652,  944],
       [ 787,  944],
       [ 945,  944],
       [1110,  944],
       [1263,  944],
       [ 652, 1038],
       [ 787, 1038],
       [ 945, 1038],
       [1110, 1038],
       [1263, 1038],
       [ 652, 1112],
       [ 787, 1112],
       [ 945, 1112],
       [1110, 1112],
       [1263, 1112]])
       
def box_detection(image):
	# Grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Find Canny edges
	edged = cv2.Canny(gray, 100, 255)
	cv2.waitKey(0)
	
	squares = []
	
	for [x, y] in boxlocations:
		subimg = edged[y:y+50, x:x+50]
		contours, _ = cv2.findContours(subimg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		square = find_square(contours)
		square = square + np.array([x, y])
		squares.append(square)
	
	#cv2.drawContours(image, squares, -1, (0, 255, 0), 3)
	
	images = []
	for box in squares:
		border = 4
		y1 = np.min(box[:,1]) + border
		y2 = np.max(box[:,1]) - border
		x1 = np.min(box[:,0]) + border
		x2 = np.max(box[:,0]) - border
		
		side = (y2-y1 + x2-x1) // 2
		if side > 0:
			images.append(image[y1:y1+side, x1:x1+side, 0])
	
	return images

def find_square(cnts):
	best_square = cv2.convexHull(cnts[0]).reshape(-1, 2)
	if len(cnts) > 1:
		best_score = square_score(best_square)
		for cnt in cnts:
			cnt = cv2.convexHull(cnt)
			cnt = cnt.reshape(-1, 2)
			score = square_score(cnt)
			if score > best_score:
				best_square = cnt
				best_score = score
	return polish_square(best_square)

def polish_square(cnt):
	return cnt

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )


def square_score(cnt):
	s = 1000
	l = len(cnt)
	s = s - abs(l-4)*50
	#s = s - np.max([angle_cos( cnt[i], cnt[(i+1) % l], cnt[(i+2) % l] ) for i in range(l)])*100
	s = s - abs(cv2.contourArea(cnt) - 900)
	return s
	
if __name__ == '__main__':
	img = cv2.imread('data/survey_jpgs/survey1.jpg')
	box_detection(img)

'''
[
[300, 525],
[400, 525],
[670, 525],
[730, 525],
[790, 525],
[1265, 525],
[1335, 525]]

xs = [652, 787, 945, 1110, 1263]
ys = [705, 778, 853, 944, 1038, 1112]

for x in xs:
	for y in ys:
		boxlocations.append([x, y])
	
boxlocations = np.array(boxlocations)
'''

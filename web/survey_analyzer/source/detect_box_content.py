import utils
import numpy as np
import skimage.io
import cv2
import sys

def box_content_detection(imgs: []):
    """
            Takes in an array of images of boxes, and estimates the probabilities that it is
            1. ticked, 2. empty or 3. scribbled out.
        args:
            images of boxes as np.arrays
        return: a list with three entries: [prob_ticked, prob_empty, prob_scribbled]
    """

    MAX_THINNESS_THRESHOLD = 14

    if len(imgs) == 0:
        #Empty inputs arguments
        return

    conf_list = []
    for img in imgs:
        #smoothing filter
        img = cv2.filter2D(img,-1, np.ones((3, 3),np.float32)/3**2)
        #region grow
        img = region_growing(img, 220)

        thickness = get_thickness(img)
        thinness = get_thinness(img)

        # thin_thick_to_probs(thickness, thinness)
        if thinness > MAX_THINNESS_THRESHOLD:
            conf_list.append(0)
        else:
            conf_list.append(1/thickness**2)

    #Normalize conf_list
    if sum(conf_list) > 0:
        norm_conf_list = [float(i)/sum(conf_list) for i in conf_list]
    else:
        norm_conf_list = conf_list

    best_index = (norm_conf_list.index(max(norm_conf_list)))

    return (best_index, norm_conf_list[best_index])


def thin_thick_to_probs(thickness: int, thinness: int):
    """
            Creates a probability vector which sums to 1 based on thickness and thinness
            The solution is hardcoded now, but should be improved and maybe have some nice formulas later.
        args:
            thickness, thinness
        return: a list with three entries: [prob_ticked, prob_empty, prob_scribbled]
    """
    probs = [0, 0, 0]

    if thickness < 2 or thinness > 10:
        probs[1] = 1

    if thickness > 2 and thinness == 2:
        probs[0] = 0.5
        probs[1] = 0
        probs[2] = 0.5

    if thickness > 2 and thinness < 2:
        probs[2] = 1
        probs[1] = 0
        probs[0] = 0

    if thickness > 2 and thinness > 2:
        probs[2] = 0
        probs[1] = 0
        probs[0] = 1

    if thickness > 10 and thinness < 4:
        probs[2] = 1
        probs[1] = 0
        probs[0] = 0

    return probs


def checkNeighbours(row, col, seed_min, seed_max, seg, img):
    """
            Recursively finds and updates the neighbours in the region grow
        args:
            row, col: coordinates of the seed point
            seed_min, seed_max: min and max threshold for the neighbours. They have to be within a interval to be valid values
            segmented image: seg
            original image: im
        return: void
    """

    for i in range(0,3):
        for j in range(0,3):
            if (row+i-1 < 0 or
                row+i-1 >= img.shape[0] or
                col+j-1 < 0 or
                col+j-1 >= img.shape[1]):
                continue
            if img[row+i-1, col+j-1] < seed_max:
                if seg[row+i-1, col+j-1] != 0:
                    seg[row+i-1][col+j-1] = 0
                    checkNeighbours(row+i-1, col+j-1, seed_min, seed_max, seg, img)
    return




def find_lowest_intensity(im: np.ndarray) -> int:
    """
            Finds and returns the lowest intensity in the image.
        args:
            im: np.ndarray of shape (H, W) in the range [0, 255] (dtype=np.uint8)
        return:
            x and y coordinate of the lowest intensity pixel.
    """
    lowest_intensity = 255
    x, y = 0, 0
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i,j] < lowest_intensity:
                lowest_intensity = im[i,j]
                x, y = i, j
    return x, y

def region_growing(im: np.ndarray, T: int) -> np.ndarray:
    """
        A region growing algorithm that segments an image into 1 or 0 (True or False).
        Finds candidate pixels with a Moore-neighborhood (8-connectedness).
        Uses pixel intensity thresholding with the threshold T as the homogeneity criteria.
        The function takes in a grayscale image and outputs a boolean image

        args:
            im: np.ndarray of shape (H, W) in the range [0, 255] (dtype=np.uint8)
            seed_points: list of list containing seed points (row, col). Ex:
                [[row1, col1], [row2, col2], ...]
            T: integer value defining the threshold to used for the homogeneity criteria.
        return:
            (np.ndarray) of shape (H, W). dtype=np.bool
    """

    #Find the lowest intensity and use this as seed_point
    row, col = find_lowest_intensity(im)

    #Instantiate the segmented image
    segmented = np.zeros_like(im)
    segmented.fill(255)
    segmented[row, col] = 0
    seed_min = 0
    seed_max = T

    #Add all the neighbours that are inside the threshold interval.
    sys.setrecursionlimit(10000)
    checkNeighbours(row, col, seed_min, seed_max, segmented, im)

    return segmented

def get_thickness(img: np.ndarray) ->int:
    """
       An algorithm that uses dilation in several steps to find how thick the black region is.
       If the thickness = 1, then we are probably workin on a empty box.
       if the thickness = 2 then we are probably working on a cross.
       if the thickness >= 3 then we are probably working on a ticked box.
        args:
            im: binary image of values 0 and 255
        return:
            (int) thickness of the region
    """

    thickness = 0
    kernel = np.ones((3,3))

    while np.sum(img) < img.size*255:
        if thickness > 15:
            return thickness
        thickness += 1
        img = cv2.dilate(img, kernel)

    return thickness

def get_thinness(img: np.ndarray):
    """
       An algorithm that uses erosion in several steps to find how thin the black region is.
       If the thinness < 3, then we are probably workin on a scribbled box.
       if the thinness > 10 then we are probably working on a empty box.
       else we are probably working on a ticked box
        args:
            im: binary image of values 0 and 255
        return:
            (int) thinness of the region
    """
    thinness = 0
    kernel = np.ones((3,3))
    while np.sum(img) > 0 and thinness < 100:
        thinness += 1
        img = cv2.erode(img, kernel)
    return thinness


if __name__ == "__main__":
    # for i in range(3):
    #     filename = "box"+str(i+1)+".png"
    #     img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    #     print(i+1)
    #     print(get_thickness(img))


    imgs = []
    box = "(0,0)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    box = "(27,6)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    box = "(27,9)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    box = "(27,21)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    box = "(98,2)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))

    box = "(0,11)"
    filename = "data/box_samples/box" + box + ".jpg"
    imgs.append(cv2.imread(filename, cv2.IMREAD_GRAYSCALE))


    print(box_content_detection(imgs))

    # kernel_size = 11
    # kernel = np.ones((kernel_size, kernel_size),np.float32)/kernel_size**2
    # smoothed_img = cv2.filter2D(img,-1,kernel)
    # processed_img = region_growing(img, 220)
    # cv2.imwrite("27,24problem.png", processed_img)

    # thickness = get_thickness(processed_img)
    # thinness = get_thinness(processed_img)
    # print(f"Box: {box} \nImage thickness: {thickness} \nImage thinness: {thinness}")

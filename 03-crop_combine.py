import numpy as np
import cv2 as cv
import pandas as pd

# PATHS on lines 102, 120, 125, 148
# "new_wings_overview.txt" is a list of all original image files / sample IDs


def custom_gray(img, BGR=(0.114, 0.587, 0.299)):
    # Y ← 0.114⋅B + 0.587⋅G + 0.299⋅R
    gray = np.ndarray((img.shape[0], img.shape[1]), dtype=np.uint8)
    for x in range(0, (img.shape[0] - 1)):  # x-axis
        for y in range(0, (img.shape[1] - 1)):  # y-axis
            gray[x, y] = BGR[0]*img[x, y, 0] + BGR[1]*img[x, y, 1] + BGR[2]*img[x, y, 2]
    return gray


def img_to_square(img, size):
    top = int((size - img.shape[0]) / 2)
    bottom = int((size - img.shape[0]) / 2)
    left = int((size - img.shape[1]) / 2)
    right = int((size - img.shape[1]) / 2)
    square_img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, (0, 0, 0))
    return square_img


def crop_to_object(img):
    img_og = img.copy()
    img_blur = cv.GaussianBlur(img, (3, 3), 0)

    edges = cv.Canny(image=img_blur, threshold1=40, threshold2=120, apertureSize=3)  # Canny Edge Detection

    # create mask from edge detection output
    edgemask = custom_gray(img)

    # draw foreground circles
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edges[x, y] == 0:
                continue
            else:
                cv.circle(edgemask, (y, x), 2, 50, -1)  # it's this one, this one flips the axes

    # colour background black (if I do this in one step with the previous loop some of the black overlays the
    # grey circles because of the order in which the pixels are checked)
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edgemask[x, y] == 50:
                continue
            else:
                edgemask[x, y] = 0

    contours, hierarchy = cv.findContours(edgemask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours, key=cv.contourArea, reverse=True)

    if len(cnt) != 0:
        wing = cnt[0]
        fx, fy, fw, fh = cv.boundingRect(wing)
        min_wing = img_og[fy:fy + fh, fx:fx + fw]
        return min_wing
    else:
        return img_og



def get_bounding_rect(img):
    img_blur = cv.GaussianBlur(img, (3, 3), 0)

    edges = cv.Canny(image=img_blur, threshold1=40, threshold2=120, apertureSize=3)  # Canny Edge Detection

    # create mask from edge detection output
    edgemask = custom_gray(img)

    # draw foreground circles
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edges[x, y] == 0:
                continue
            else:
                cv.circle(edgemask, (y, x), 2, 50, -1)  # it's this one, this one flips the axes

    # colour background black (if I do this in one step with the previous loop some of the black overlays the
    # grey circles because of the order in which the pixels are checked)
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edgemask[x, y] == 50:
                continue
            else:
                edgemask[x, y] = 0

    contours, hierarchy = cv.findContours(edgemask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours, key=cv.contourArea, reverse=True)

    if len(cnt) != 0:
        wing = cnt[0]
        x, y, w, h = cv.boundingRect(wing)

        return x, y, w, h


def combine_wings(fore, hind):
    final = cv.imread("//PATH//TO//BLANK//BACKGROUND.png")

    fx, fy, fw, fh = get_bounding_rect(fore)
    hx, hy, hw, hh = get_bounding_rect(hind)

    final[0:fh, 0:fw] = fore

    final[fh+20:fh+20+hh, 0:hw] = hind

    final = final[0:fh+20+hh, 0:fw]

    return final



#=======================================================================================================================


path = "//PATH//TO//WD//"
overview = pd.read_csv(path + "new_wings_overview.txt", header=0, sep="\t")

names_all = overview.iloc[:, 0]

scale = cv.imread("//PATH//TO//STANDARD//SCALE.png")


for file in (names_all):
    free_fw = cv.imread(path + "forewings_rotated//fw_r_" + file + ".png")
    free_hw = cv.imread(path + "hindwings_rotated//hw_r_" + file + ".png")

    min_fw = crop_to_object(free_fw)
    min_hw = crop_to_object(free_hw)

    combo = combine_wings(min_fw, min_hw)

    combo[50:50 + 54, 50:50 + 198] = scale

    square = img_to_square(combo, 950)

    # make transparent background
    tmp = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
    _, alpha = cv.threshold(tmp, 0, 255, cv.THRESH_BINARY)
    b, g, r = cv.split(square)
    rgba = [b, g, r, alpha]
    t_square = cv.merge(rgba, 4)

    cv.imwrite("//PATH//TO//RESULT//" + file + ".png", t_square)

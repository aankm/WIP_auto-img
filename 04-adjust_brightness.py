import numpy as np
import cv2 as cv
from scipy import stats
import pandas as pd

# PATHS on lines 43
# "new_wings_overview.txt" is a list of all original image files / sample IDs


#https://ie.nitk.ac.in/blog/2020/01/19/algorithms-for-adjusting-brightness-and-contrast-of-an-image/

def cutoff(val):
    if val < 0:
        val = 0
    elif val > 255:
        val = 255
    return val

def brightness(img):            #note: black pixels are not included
    summe, mean, anzahl = 0.0, 0.0, 0.0
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    for x in range(0, (img_gray.shape[0] - 1)):  # x-axis
        for y in range(0, (img_gray.shape[1] - 1)):  # y-axis
            if img_gray[x, y] != 0:
                summe = summe + img_gray[x, y]
                anzahl += 1
    mean = float(summe)/float(anzahl)
    return mean

def adjust_brightness(img, target):
    b = brightness(img)
    for x in range(0, (img.shape[0] - 1)):  # x-axis
        for y in range(0, (img.shape[1] - 1)):  # y-axis
            if (img[x, y] != 0).all():
                img[x, y, 0] = cutoff(img[x, y, 0] + (target - b))
                img[x, y, 1] = cutoff(img[x, y, 1] + (target - b))
                img[x, y, 2] = cutoff(img[x, y, 2] + (target - b))
    return img


#=======================================================================================================================

path = "//PATH//TO//WD//"
overview = pd.read_csv(path + "new_wings_overview.txt", header=0, sep="\t")

names_all = overview.iloc[:, 0]

sumB = 0.0
meanB = 0.0

for file in (names_all):
    source = cv.imread(path + "wings_combined//rct_" + file + ".png")
    sumB = sumB + brightness(source)

meanB = sumB/23.0

print(meanB)

for file in (names_all):
    img = cv.imread(path + "wings_combined//rct_" + file + ".png")
    B = adjust_brightness(img, meanB)

    # make transparent background
    tmp = cv.cvtColor(B, cv.COLOR_BGR2GRAY)
    _, alpha = cv.threshold(tmp, 0, 255, cv.THRESH_BINARY)
    b, g, r = cv.split(B)
    rgba = [b, g, r, alpha]
    t_B = cv.merge(rgba, 4)

    cv.imwrite(path + "wings_combined_adjusted//rctb_" + file + ".png", t_B)

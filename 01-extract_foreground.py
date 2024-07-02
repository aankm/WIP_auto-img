import numpy as np
import cv2 as cv
import pandas as pd

# PATHS on lines 18, 107
# "new_wings_overview.txt" is a list of all original image files / sample IDs

def custom_gray(img, BGR=(0.114, 0.587, 0.299)):
    # Y ← 0.114⋅B + 0.587⋅G + 0.299⋅R
    gray = np.ndarray((img.shape[0], img.shape[1]), dtype=np.uint8)
    for x in range(0, (img.shape[0] - 1)):  # x-axis
        for y in range(0, (img.shape[1] - 1)):  # y-axis
            gray[x, y] = BGR[0]*img[x, y, 0] + BGR[1]*img[x, y, 1] + BGR[2]*img[x, y, 2]
    return gray


def extract_foreground(IMG):
# load image and apply Gaussian blur
    img = cv.imread("//PATH//TO//ORIGINAL//IMGS//" + IMG + ".jpg")
    img_blur = cv.GaussianBlur(img, (3, 3), 0)

# detect edges in the images (output is a b/w of where colour contrasts are)
    edges = cv.Canny(image=img_blur, threshold1=40, threshold2=120, apertureSize=3)  # Canny Edge Detection

# create base for mask
    edgemask = custom_gray(img)

# draw foreground circles (white) on each white point of the edge detection output
# NB choose size of the circles to create a continuous object covering the whole wing with minimal background
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edges[x, y] == 0:
                continue
            else:
                cv.circle(edgemask, (y, x), 2, 50, -1)  # it's this one, this one flips the axes

# colour background black (if I do this in one step with the previous loop some of the black overlays the
# white circles because of the order in which the pixels are checked)
    for x in range(0, (edgemask.shape[0] - 1)):  # x-axis
        for y in range(0, (edgemask.shape[1] - 1)):  # y-axis
            if edgemask[x, y] == 50:
                continue
            else:
                edgemask[x, y] = 0

# find the contours (read: continuous objects) in the mask and sort them by size (decreasing order)
    contours, hierarchy = cv.findContours(edgemask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnt = sorted(contours, key=cv.contourArea, reverse=True)
    wings = []
# the first (largest) contour in the list (index 0) should be the forewing
    forewing = cnt[0]
    fw_edgemask = edgemask.copy()
# if the contour is large enough to be the forewing: fill everything within its boundaries
    if cv.contourArea(forewing) > 50000:
        cv.fillPoly(fw_edgemask, pts =[forewing], color=(255, 255, 255))

# in a copy of the input image: apply the mask, leaving the wing contour as is
    fw = img.copy()

    for x in range(0, (fw.shape[0]-1)):    # x-axis
        for y in range(0, (fw.shape[1]-1)):    # y-axis
            if fw_edgemask[x, y] == 255:
                continue
            else:
                fw[x, y] = [0, 0, 0]

# add black frame to cover edges
    fw[0:fw.shape[0] + 1, 0:10] = (0, 0, 0)
    fw[0:10, 0:] = (0, 0, 0)
    fw[fw.shape[0] - 10:, 0:] = (0, 0, 0)
    fw[0:, fw.shape[1] - 10:] = (0, 0, 0)

    final_fw = fw[5:fw.shape[0] - 5, 4:fw.shape[1] - 4]


# the second (second largest) contour in the list (index 1) should be the hindwing
    hindwing = cnt[1]
    hw_edgemask = edgemask.copy()

# if the contour is large enough to be the hindwing: fill everything within its boundaries
    if cv.contourArea(hindwing) > 20000:
        cv.fillPoly(hw_edgemask, pts =[hindwing], color=(255, 255, 255))

# in a copy of the input image: apply the mask, leaving the wing contour as is
    hw = img.copy()

    for x in range(0, (hw.shape[0]-1)):    # x-axis
        for y in range(0, (hw.shape[1]-1)):    # y-axis
            if hw_edgemask[x, y] == 255:
                continue
            else:
                hw[x, y] = [0, 0, 0]

# add black frame to cover edges
    hw[0:hw.shape[0] + 1, 0:10] = (0, 0, 0)
    hw[0:10, 0:] = (0, 0, 0)
    hw[hw.shape[0] - 10:, 0:] = (0, 0, 0)
    hw[0:, hw.shape[1] - 10:] = (0, 0, 0)

    final_hw = hw[5:hw.shape[0] - 5, 4:hw.shape[1] - 4]

    return final_fw, final_hw


#=======================================================================================================================


path = "//PATH//TO//SAVE//ISOLATED//IMGS//"
overview = pd.read_csv(path + "new_wings_overview.txt", header=0, sep="\t")

names_all = overview.iloc[:, 0]

for file in (names_all):
    free_fw, free_hw = extract_foreground(file)
    cv.imwrite(path + "forewings_regular//fw_" + file + ".png", free_fw)
    cv.imwrite(path + "hindwings_regular//hw_" + file + ".png", free_hw)

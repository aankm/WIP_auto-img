# SOURCE: https://github.com/opencv/opencv/blob/master/samples/python/grabcut.py

# PATHS on lines 113
# "new_wings_overview.txt" is a list of all original image files / sample IDs


# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2 as cv
import imutils
import pandas as pd

import math

def rotate(img, angle):
    height, width = img.shape[:2]
    center = (width / 2, height / 2)
    rotate_matrix = cv.getRotationMatrix2D(center=center, angle=angle, scale=1)
    rotated_img = cv.warpAffine(src=img, M=rotate_matrix, dsize=(width, height))
    return rotated_img


#region draw orientation axis

class App():
    BLUE = [255,0,0]        # line color
    RED = [0,0,255]         # PR BG
    GREEN = [0,255,0]       # PR FG
    BLACK = [0,0,0]         # sure BG
    WHITE = [255,255,255]   # sure FG

    DRAW_BG = {'color' : BLACK, 'val' : 0}
    DRAW_FG = {'color' : WHITE, 'val' : 1}
    DRAW_PR_BG = {'color' : RED, 'val' : 2}
    DRAW_PR_FG = {'color' : GREEN, 'val' : 3}

    # setting up flags
    rect = (0,0,1,1)
    drawing = False         # flag for drawing curves
    line = False       # flag for drawing rect
    rect_over = False       # flag to check if rect drawn
    rect_or_mask = 100      # flag for selecting rect or mask mode
    value = DRAW_FG         # drawing initialized to FG
    thickness = 2           # brush thickness

    def onmouse(self, event, x, y, flags, param):
    # Draw Rectangle
        if event == cv.EVENT_RBUTTONDOWN:
            self.line = True
            self.ix, self.iy = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.line == True:
                self.img = self.img2.copy()
                cv.line(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
                self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
                self.rect_or_mask = 0

        elif event == cv.EVENT_RBUTTONUP:
            self.line = False
            self.rect_over = True
            cv.line(self.img, (self.ix, self.iy), (x, y), self.BLUE, 2)
            self.rect = (min(self.ix, x), min(self.iy, y), abs(self.ix - x), abs(self.iy - y))
            self.rect_or_mask = 0
            print(" Press r to reset, s to save, n to move on \n")
            global coordinates
            coordinates = [[x, y], [self.ix, self.iy]]
#            return coordinates


    def run(self, input):
        # Loading images
#        self.img = cv.imread("C://Users//annep//Desktop//UNI//MSc_Bonn//OEP_free_Christoph//WIP_ML//all_sp_ed//data_plus//0d_2629573_1.jpg")
        self.img = input
        self.img2 = self.img.copy()                               # a copy of original image
        self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG

        # input and output windows
        cv.namedWindow('input')
        cv.setMouseCallback('input', self.onmouse)

        print(" Draw a line to use to orient the image using right mouse button \n")

        while(1):

            cv.imshow('input', self.img)
            k = cv.waitKey(1)

            # key bindings
            if k == ord('r'): # reset everything
                print("resetting \n")
                self.rect = (0,0,1,1)
                self.drawing = False
                self.line = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.img2.copy()
                self.mask = np.zeros(self.img.shape[:2], dtype = np.uint8) # mask initialized to PR_BG
            elif k == ord('n'): # segment the image
                return self.img

#endregion


coordinates = [] #np.ndarray((2, 2))


#=======================================================================================================================



path = "C://Users//annep//Desktop//UNI//MSc_Bonn//OEP_IND_Christoph//WIP_ML//improved_edit_publication//"


## trying out the program on just one image:
##region just one:
#inim = cv.imread(//PATH//TO//IMG.png")
#ogim = inim.copy()
#output = App().run(inim)

#dx = coordinates[0][0] - coordinates[1][0]
#dy = coordinates[0][1] - coordinates[1][1]
#rad = math.atan2(dy, dx)
#deg = 57.2958 * rad
#rot = imutils.rotate_bound(ogim, -deg)

#cv.imshow('output', rot)
#k = cv.waitKey(0)

#cv.imwrite(//PATH//TO//RESULT.png", rot)
##endregion


# all:

overview = pd.read_csv(path + "new_wings_overview.txt", header=0, sep="\t")
names_all = overview.iloc[:, 0]

#region rotate forewing

for file in (names_all):
    inim = cv.imread(path + "forewings_regular//fw_" + file + ".png")
    ogim = inim.copy()
    output = App().run(inim)


    dx = coordinates[0][0] - coordinates[1][0]
    dy = coordinates[0][1] - coordinates[1][1]
    rad = math.atan2(dy, dx)
    deg = 57.2958 * rad
    rot = imutils.rotate_bound(ogim, -deg)

    cv.imwrite(path + "forewings_rotated//fw_r_" + file + ".png", rot)
    cv.destroyAllWindows()

#endregion


#region rotate hindwing

for file in (names_all):
    inim = cv.imread(path + "hindwings_regular//hw_" + file + ".png")
    ogim = inim.copy()
    output = App().run(inim)


    dx = coordinates[0][0] - coordinates[1][0]
    dy = coordinates[0][1] - coordinates[1][1]
    rad = math.atan2(dy, dx)
    deg = 57.2958 * rad
    rot = imutils.rotate_bound(ogim, -deg)

    cv.imwrite(path + "hindwings_rotated//hw_r_" + file + ".png", rot)
    cv.destroyAllWindows()

#endregion

# WIP_auto-img
(semi)-automated image processing for wing interference pattern (WIP) analysis


All editing steps use OpenCV (cv2, Bradski 2000) and imutils v0.5.4 (Rosebrock 2015) for image manipulation, and NumPy (Harris et al. 2020) and Pandas (Pandas Development Team 2020) when working with arrays.
This protocol is by no means optimised in terms of efficiency or computing resources. It’s an approach out of many that can work. 

1.	Isolate the wings: In order to remove extraneous signal from the images, isolate the wings from the background. As is, the script will save the forewing and hindwing for each individual in separate files. The two wings were processed separately and recombined to a final image in a standardised way after the subsequent editing steps, but just combine both contours to maintain the wings’ orientation to each other. 
 01-extract_foreground.py
1.1	Create a mask from the contours detected in the image with the edge detection function cv2.Canny() by overlaying the edges with small circles of the same solid colour (grey). The size of the circles should be selected so that all edges within the desired foreground area connect into one shape. Fill all areas outside this shape with a solid colour. If the background is too noisy, this step may not work as desired.
1.2	Now find all contours (read: continuous objects) within the mask using cv2.findContours(), and sort them in order of decreasing area.
1.3	Then fill the largest contour of the mask (the forewing) in a different solid colour (white). Use this mask to black out all areas of a copy of the original image that are not part of the foreground object.
1.4	Repeat this for the second largest contour (the hindwing). If the forewing and hindwing areas intersect, or one part is missing in some images, make these steps conditional on the size of the contours.

2	(Only if magnification and resolution differ within the series of images: Re-size images to put them to scale. In this dataset it was not necessary.)
3	Standardize orientation: Rotate the images so that the back margin of the forewing and the front margin of the hindwing were horizontal. The rotation function was customised from an OpenCV interactive grabcut algorithm available at
https://github.com/opencv/opencv/blob/master/samples/python/grabcut.py
The program opens a new window and prompts the user to draw a line in the image indicating the edge that should be horizontally aligned. The difference between the angle of this line and the 0° horizontal is calculated and the image rotated accordingly. Note that it is important to keep the direction (start and end points) of the guiding line consistent. Use any two consistent landmarks across the dataset. 
 02-interactive_rotation.py

4	Crop isolated and rotated images to their minimum possible size and combine the fore- and hindwings into one image. 
 03-crop_combine.py
4.1	Create a mask from the contours detected in the image with the edge detection function cv2.Canny() by overlaying the edges with small circles of the same solid colour (grey). The size of the circles should be selected so that all edges within the desired foreground area connect into one shape. Fill all areas outside this shape with a solid colour.
4.2	Now find all contours (read: continuous objects) within the mask using cv2.findContours(). There should be one contour in each image, since the wings were already isolated.
4.3	Find the minimum dimensions of the wing contours (cv2.boundingRect()), and crop the image to the corresponding coordinates.
4.4	Using the bounding rectangle dimensions, place the wings into a blank background with specified distance from the edges and each other. 
4.5	A standardised scale can be placed into the images. 

5	If necessary, adjust the brightness of the images to the same level. Do this after removing the background and exclude black pixels from the calculation. 
 04-adjust_brightness.py


references:
Bradski G. 2000. The OpenCV Library. Dr. Dobb’s Journal of Software Tools 25(11), p. 120-123. 
Harris CR, Millman KJ, van der Walt SJ, Gommers R, Virtanen P, Cournapeau D, Wieser E, Taylor J, Berg S, Smith NJ, Kern R. 2020. Array programming with NumPy. Nature 585(7825), p. 357-362. 
Pandas Development Team (McKinney et al.). 2020. pandas-dev/pandas: Pandas (v1.3.3). DOI 10.5281/zenodo.3509134 
Rosebrock A. 2015. Imutils: A series of OpenCV convenience functions. https://pyimagesearch.com/2015/02/02/just-open-sourced-personal-imutils-package-series-opencv-convenience-functions/ - https://github.com/PyImageSearch/imutils 
Virtanen P, Gommers R, Oliphant TE, Haberland M, Reddy T, Cournapeau D, Burovski E, Peterson P, Weckesser W, Bright J, van der Walt SJ, Brett M, Wilson J, Millman KJ, Mayorov N, Nelson ARJ, Jones E, Kern R, Larson E, Carey CJ, Polat İ, Yu F, Moore EW, VanderPlas J, Laxalde D, Perktold J, Cimrman R, Henrikson I, Quintero EA, Harris CR, Archibald AM, Ribeiro AH, Pedregosa F, van Mulbregt P, SciPy 1.0 Cotributors. 2020. SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python. Nature Methods, 17(3), 261-272. 

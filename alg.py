import pydicom;
import cv2
from PIL import Image
import matplotlib
import sys
import numpy
numpy.set_printoptions(threshold=sys.maxsize)



# reading a file on this computer
# file path for pydicom: /Users/AmyEric/Desktop/OHSU Research/pydicom.dcm
dataset = pydicom.dcmread('/Users/AmyEric/Desktop/OHSU Research/1tagtest.dcm')

# getting pixel data in array form
#print dataset.__sizeof__()
pixel_array = dataset.pixel_array


# OpenCV Shape ID Code:
##################################################################################################

from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils

#convert pixel_array to uint8 from uint 16 for compatability
#pixel_array = (pixel_array/256).astype('uint8')
#print pixel_array
pixel_array = cv2.normalize(pixel_array, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

pixelimage = Image.fromarray(pixel_array)
#pixelimage.show()


# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image=cv2.cvtColor(pixel_array, cv2.COLOR_RGB2BGR)

#imageimage = Image.fromarray(image)
#imageimage.show()

newwdith = 1000
resized = imutils.resize(image, width=newwdith)
ratio = image.shape[0] / float(resized.shape[0])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

#INRANGE, EXPERIMENTAL WAY TO EXCLUDE EXTRANEOUS FEATURES
#thresh1 = cv2.inRange(blurred, 120, 129)
#thresh1image = Image.fromarray(thresh1)
#thresh1image.show()

thresh2 = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
#around 123 is the pixel_array value of the tags

#ERROR HYPOTHESIS: pixel_array from pydicom is not RGB,
# so conversion to GBR, renders it in wrong format ex: not unit 8

threshimage = Image.fromarray(thresh2)
threshimage.show()

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

sd = ShapeDetector()

# loop over the contours
for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    cX = int((M["m10"] / (0.00001+M["m00"])) * ratio)
    cY = int((M["m01"] / (0.00001+M["m00"])) * ratio)
    shape = sd.detect(c)
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")

    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    print cv2.contourArea(c)
    tagcenters = []
    if shape == "tag" and cv2.contourArea(c) < (25*newwdith/300) and cv2.contourArea(c) >(15*newwdith/300):
        cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                     0.5, (255, 255, 255), 2)



    # draw the contour and center of the shape on the image
    if shape == "tag" and cv2.contourArea(c) < (25*newwdith/300) and cv2.contourArea(c) >(15*newwdith/300):
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, "center", (cX - 20, cY - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)


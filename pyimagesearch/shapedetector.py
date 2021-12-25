# import the necessary packages
import ocvproto
import cv2
from numpy.ma.testutils import approx


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        # initialize the shape name and approximate the contour
        shape = "?"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        #if shape is a tag, it will have 2 vertices
        if len(approx) == 2:
            shape = "tag"

        # if the shape is a triangle, it will have 3 vertices
        elif len(approx) == 3:
            shape = "tag"

        # return the name of the shape
        if shape =="tag":
            return shape





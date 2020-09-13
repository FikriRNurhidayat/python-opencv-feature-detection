import threading
import cv2
from lib.image import Image

match = None

def query(sourceFrame = None):
    global match
    # Convert frame into gray scale
    # To improve perfomance
    frame = cv2.cvtColor(sourceFrame, cv2.COLOR_BGR2GRAY)
    image = Image.create('Frame', fileBuffer = frame, usePath = False, useColor = True)

    # Query Image in the dictionaries
    # If the result is None, then we don't mutate
    # lastMatch, somehow it is useful someday.
    result = Image.find(image)
    if (match != result):
        match = result

import cv2
import sys
from lib.image import Image

# Parse process arguments
# For now, we only have the useWindow Option
# Add more if you want to, but tweaks it yourself :P
useWindow = True
for argument in sys.argv:
    if argument == 'disable-window': useWindow = False 

# Run configuration
Image.config(useColor = False)
WINDOW_NAME = 'OpenCV Test'
INTERVAL = 60

# Window Setup
cv2.startWindowThread()
video = cv2.VideoCapture(0)
frameNumber = 1
lastMatch = None

while True:
    frameNumber += 1

    _, sourceFrame = video.read()
    frame = Image()
    frame.name = WINDOW_NAME
    frame.fileBuffer = sourceFrame

    # Run query every INTERVAL value frame, to save some perfomance :D
    if frameNumber % INTERVAL == 0:
        # Convert frame into gray scale
        # To improve perfomance
        grayFrame = cv2.cvtColor(sourceFrame, cv2.COLOR_BGR2GRAY)
        grayImage = Image.create('Frame', fileBuffer = grayFrame, usePath = False, useColor = False)

        # Query Image in the dictionaries
        # If the result is None, then we don't mutate
        # lastMatch, somehow it is useful someday.
        result = Image.find(grayImage)
        if (result is not None) & (lastMatch != result):
            lastMatch = result
            print(lastMatch)

    # Initialize Key
    key = None

    # Check if the process wants to create window on the Display Server
    if useWindow:
        key = frame.show(waitKey=1)
    else:
        key = cv2.waitKey(1)

    # If key pressed is ESC, it will close the process
    if key in [27, 1048603]:
        cv2.destroyAllWindows()
        break

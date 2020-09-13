import cv2
import sys
import threading
import lib.event
from lib.image import Image

# Parse process arguments
# For now, we only have the useWindow Option
# Add more if you want to, but tweaks it yourself :P
useWindow = True
for argument in sys.argv:
    if argument == 'disable-window': useWindow = False 

# Run configuration
Image.config(useColor = True)
WINDOW_NAME = 'OpenCV Test'
INTERVAL = 15

# Window Setup
cv2.startWindowThread()
video = cv2.VideoCapture(0)
frameNumber = 1

while True:
    global sourceFrame
    global match

    frameNumber += 1
    _, sourceFrame = video.read()

    frame = Image()
    frame.name = WINDOW_NAME
    frame.fileBuffer = sourceFrame

    thread = None
    # Run query every INTERVAL value frame, to save some perfomance :D
    if frameNumber % INTERVAL == 0:
        totalThread = threading.active_count()
        if totalThread == 1:
            thread = threading.Thread(target = lib.event.query, args = (sourceFrame,))
            thread.start()

    # Initialize Key
    key = None

    # Check if the process wants to create window on the Display Server
    if useWindow:
        # I don't know how to pass argument when calling  a function dynamically
        # IN PYTHON, OKAY! But, let's just do the duck typing
        if lib.event.match is not None: key = frame.show(waitKey = 1, withText = lib.event.match)
        else: key = frame.show(waitKey = 1)
    else:
        key = cv2.waitKey(1)

    # If key pressed is ESC, it will close the process
    if key in [27, 1048603]:
        cv2.destroyAllWindows()
        break

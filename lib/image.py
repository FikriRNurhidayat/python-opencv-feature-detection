import cv2
import os

class Image:
    sourceFiles = []
    sourceImages = []
    classifications = []
    orb = None
    bruteForce = None

    def __init__(self):
        self.name = None
        self.fileBuffer = None 
        self.keypoint = None
        self.descriptor = None 

    # This method is being used to show the image
    # Using the image viewer
    # But, fuck it, I don't want to use this.
    # Since wayland will fuck me up
    def show(self, waitKey = 0):
        cv2.imshow(self.name or 'OpenCV Test', self.fileBuffer)
        return cv2.waitKey(waitKey)

    def _formatFileName(self, fileName):
        fileName = fileName.lower().split(' ')
        return '_'.join(fileName)

    # Use this method to save the file 
    def save(self, directory = 'keypoints', bufferType = None, extention = 'png'):
        switcher = {
            None: self.fileBuffer,
            'keypoints': cv2.drawKeypoints(self.fileBuffer, self.keypoint, None)
        }
        fileBuffer = switcher.get(bufferType)
        fileName = self._formatFileName(self.name if bufferType == None else f'{self.name}-{bufferType}')
        return cv2.imwrite(f'{directory}/{fileName}.{extention}', fileBuffer)

    # Use this method when you want to
    # Create new instance of Image
    # So you will automatically
    # Setup the basic configuration for OpenCV
    @classmethod
    def create(cls, name, filePath = None, fileBuffer = None, usePath = True, useColor = True):
        self = cls()
        self.name = name
        if usePath:
            self.fileBuffer = cv2.imread(filePath) if useColor else cv2.imread(filePath, 0)
        else:
            self.fileBuffer = fileBuffer

        self.keypoint, self.descriptor = cls.orb.detectAndCompute(self.fileBuffer, None)
        return self

    # This method will return array of good point
    # After matching process
    @classmethod
    def compare(cls, x, y):
        matchingPoints = cls.bruteForce.knnMatch(x.descriptor, y.descriptor, k = 2)
        goodPoints = []
        for k1, k2 in matchingPoints:
            if k1.distance < 0.75 * k2.distance: goodPoints.append([k1]) 
        return goodPoints

    # This method will return member of Image class
    # which has similar points with source image
    # which being passed
    @classmethod
    def find(cls, image, treshold = 20):
        try:
            score = []
            for sourceImage in cls.sourceImages:
                points = cls.compare(sourceImage, image)
                score.append(len(points))
            # Find the best score of matchs
            # And return the index of that image
            # On the sourceImages array
            maximumScore = max(score)
            matchingImageIndex = score.index(maximumScore) if maximumScore > treshold else -1
            return cls.classifications[matchingImageIndex] if matchingImageIndex > -1 else None
        except:
            return None

    # This method will calculate the matching point
    # Then return the matching point as Image member
    @classmethod
    def drawMatches(cls, x, y):
        self = cls()
        self.name = f'{x.name} {y.name} match point'
        self.fileBuffer = cv2.drawMatchesKnn(x.fileBuffer, x.keypoint, y.fileBuffer, y.keypoint, cls.compare(x, y), None, flags = 2)
        return self

    @classmethod
    def config(cls, useColor = True, nfeatures = 1500, path = 'dictionaries'):
        cls.orb = cv2.ORB_create(nfeatures = nfeatures)
        cls.bruteForce = cv2.BFMatcher()
        cls.sourceFiles = os.listdir(path)
        for fileName in cls.sourceFiles:
            image = cls.create(os.path.splitext(fileName)[0], filePath = f'{path}/{fileName}', useColor = useColor)
            cls.sourceImages.append(image)
            cls.classifications.append(image.name)

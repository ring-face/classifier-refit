from joblib import load
import face_recognition
import os
import numpy as np
import logging

from . import helpers
from ringFace.ringUtils import commons


def testClassifier(clfFile, imageDir):
    """
    This methods loads the persisted classifier, and tests ist capabilities on the test set of the **/test-images folder.
    These images were not part of the encoding and fitting process, and hence are good candidates to test the quality of the fitting.
    TODO: The classifier will assign any face to a known person, and will never results in unknow face. This is the 
    result of the split of the solution space, as any point in the eucilidian space will be assigned to exacly one person.
    Additional euclidian distance calcuation must be added to reveal if the distance for the know faces in under a given tolerance.
    """
    logging.info(f"Testing the classifier from {clfFile}")
    clf = load(clfFile)

    for personName in os.listdir(imageDir):
        testImagesDir=imageDir + "/" + personName + "/test-images"
        encodingsDir=imageDir + "/" + personName + "/encodings"
        

        if os.path.exists(testImagesDir):

            logging.debug(f"testing faces of {personName} from dir {testImagesDir}")

            for testImage in os.listdir(testImagesDir):
                personImageFile = testImagesDir + "/" + testImage

                logging.debug(f"testing {personImageFile}")

                testImageNp = face_recognition.load_image_file(personImageFile)

                # Find all the faces in the test image using the default HOG-based model
                face_locations = face_recognition.face_locations(testImageNp)
                no = len(face_locations)
                logging.debug(f"Number of faces detected: {no}")

                # Predict all the faces in the test image using the trained classifier
                for i in range(no):
                    encoding = face_recognition.face_encodings(testImageNp)[i]
                    name = clf.predict([encoding])
                    if commons.isWithinTolerance(encoding, encodingsDir):
                        logging.debug(f"Found: {name}")
                    else: 
                        logging.warn(f"Unknown person in the image {personImageFile}")

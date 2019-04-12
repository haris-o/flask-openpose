import logging
import sys

import cv2

sys.path.append('/usr/local/python')
from openpose import pyopenpose as op

logger = logging.getLogger(__name__)


def get_points_from_image(image_path):
    try:
        logger.debug('Starting analysis')

        # parameters
        params = dict()
        params["model_folder"] = "./openpose_models/"
        params["face"] = True
        params["hand"] = True

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Image
        datum = op.Datum()
        imageToProcess = cv2.imread(image_path)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        logger.debug('Analysis done, raw data: {}'.format(datum.cvOutputData))

        return datum.cvOutputData
    except Exception as e:
        logger.error('An error occurred while analysing an image')
        logger.error(e, exc_info=True)
        # propagate error forward
        raise e

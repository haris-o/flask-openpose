import logging
import sys
from math import ceil

import cv2
import numpy as np

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
        # params["write_json"] = "./json_outputs/"

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


def get_points_from_video(video_path, results_per_second):
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

        result = []
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise FileNotFoundError('Video not found')

        frame_rate = int(capture.get(cv2.CAP_PROP_FPS))
        step = int(ceil(frame_rate / results_per_second))

        index = 0
        while True:
            success, frame = capture.read()
            if not success:
                break
            elif index % step == 0:
                datum = op.Datum()
                datum.cvInputData = frame
                opWrapper.emplaceAndPop([datum])

                data = {
                    'pose_keypoints_2d': datum.poseKeypoints.tolist(),
                    'pose_keypoints_3d': datum.poseKeypoints3D.tolist(),

                    'face_keypoints_2d': datum.faceKeypoints.tolist(),
                    'face_keypoints_3d': datum.faceKeypoints3D.tolist(),

                    'hand_keypoints_2d': np.asarray(datum.handKeypoints).tolist(),
                    'hand_keypoints_3d': np.asarray(datum.handKeypoints3D).tolist()
                }

                logger.debug('Analysis for image index {} done, raw data: {}'.format(index, datum))

                time = capture.get(cv2.CAP_PROP_POS_MSEC)
                result.append({
                    'time': time,
                    'index': index,
                    'data': data
                })
            index += 1

        logger.debug('Analysis done, result: {}'.format(result))
        return result
    except Exception as e:
        logger.error('An error occurred while analysing an image')
        logger.error(e, exc_info=True)
        # propagate error forward
        raise e

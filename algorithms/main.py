import logging
import os
import uuid

import cv2

from flask import url_for

from algorithms.tensorflow_openpose import get_points_from_image as tf_from_image
from algorithms.basic_openpose import get_points_from_image as op_from_image

STATIC_FOLDER = './static'
logger = logging.getLogger(__name__)


def analyse_image(algorithm, image_path):
    try:
        logger.debug('Analysing path: {} with algorithm: {}'.format(image_path, algorithm))

        if algorithm == 'tf-openpose':
            data = tf_from_image(image_path)
        elif algorithm == 'openpose':
            data = op_from_image(image_path)
        else:
            raise KeyError('Specified algorithm not supported.')

        logger.debug('Algorithm finished, raw data: {}'.format(data))

        # save the result as image
        title = str(uuid.uuid4()) + '.jpg'
        image_path = os.path.join(STATIC_FOLDER, title)

        logger.debug('Writing resulting image to: {}'.format(image_path))

        cv2.imwrite(image_path, data)
        result_path = url_for('static', filename=title)

        logger.debug('Final image path: {}'.format(result_path))

        return True, result_path
    except Exception as e:
        logger.error('An error occurred while analysing image')
        logger.error(e, exc_info=True)
        print(e)
        return False, str(e)

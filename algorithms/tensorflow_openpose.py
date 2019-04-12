import logging

from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

STATIC_FOLDER = './static'
RESIZE = '0x0'
RESIZE_OUT_RATIO = 4.0
MODEL = 'cmu'
logger = logging.getLogger(__name__)


def get_points_from_image(image_path):
    w, h = model_wh(RESIZE)

    # load image
    image = common.read_imgfile(image_path, None, None)
    if image is None:
        raise FileNotFoundError('Image not found')

    # configure the estimator
    if w == 0 or h == 0:
        e = TfPoseEstimator(get_graph_path(MODEL), target_size=(432, 368))
    else:
        e = TfPoseEstimator(get_graph_path(MODEL), target_size=(w, h))

    # get points
    humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=RESIZE_OUT_RATIO)
    data = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
    return data

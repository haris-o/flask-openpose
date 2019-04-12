import logging
import logging.handlers
import os

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename

from algorithms.main import analyse_image

UPLOAD_FOLDER = './uploads'
STATIC_FOLDER = './static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 's_e_c_r_e_t'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# logging
fullHandler = logging.handlers.RotatingFileHandler('debug.log', maxBytes=5048576, backupCount=1)
fullHandler.setLevel(logging.DEBUG)
fullHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
root = logging.getLogger()
root.setLevel(logging.DEBUG)
root.addHandler(fullHandler)

logger = logging.getLogger(__name__)


@app.route('/')
def home():
    logger.debug('Received GET for /')
    return render_template('home.html')


@app.route('/analyse', methods=['POST'])
def analyse():
    try:
        logger.debug('Received POST for /analyse')

        # check if the post request has the image part
        if 'image' not in request.files:
            return redirect('/')

        image = request.files['image']
        algorithm = request.form['algorithm']

        logger.debug('Image: {}'.format(image.filename))
        logger.debug('Algorithm: {}'.format(algorithm))

        if image.filename == '':
            logger.debug('Image not found, returning to /')
            return redirect('/')

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            logger.debug('Image saved to {}'.format(image_path))

            success, result = analyse_image(algorithm, image_path)
            logger.debug('Algorithm result: {}, {}'.format(success, result))

            if success:
                logger.debug('Returning /result with image_path: {}'.format(result))
                return render_template('result.html', image_path=result)
            else:
                # an error occurred, show the error message
                logger.debug('An error occurred in the algorithm: {}'.format(result))
                return result
    except Exception as e:
        logger.error('An error occurred while analysing image')
        logger.error(e, exc_info=True)
        print(e)
        return 'An error occurred, try again'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)

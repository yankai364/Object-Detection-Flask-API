from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from yolo import process
from datetime import datetime
from random import randint


app = Flask(__name__)
CORS(app)
uploads_dir = os.path.join(app.instance_path, 'uploads')
plots_dir = os.path.join(app.instance_path, 'plots')


@app.route('/upload/', methods=['POST'])
def upload_image():
    try:
        os.mkdir(uploads_dir)
        os.mkdir(plots_dir)
    except:
        pass

    file = request.files['file']
    if not file:
        return {'error': 'Missing file'}
    
    now = datetime.now()
    filename = now.strftime("%Y%m%d_%H%M%S") + "_" + str(randint(000, 999))
    file.save(os.path.join(uploads_dir, secure_filename(filename + '.jpg')))
    objects_count, objects_confidence = process(uploads_dir, plots_dir, filename)
    
    return {'objects_count': objects_count, 'objects_confidence': objects_confidence, 'filename': filename + '.jpg'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

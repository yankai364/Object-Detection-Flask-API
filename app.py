from flask import Flask, request
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
from yolo import process


app = Flask(__name__)
CORS(app)
uploads_dir = os.path.join(app.instance_path, 'uploads')



@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload/', methods=['POST'])
def upload_image():
    file = request.files['file']
    print(file.filename)
    file.save(os.path.join(uploads_dir, secure_filename('image.jpg')))
    return {'classes': process(uploads_dir)}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

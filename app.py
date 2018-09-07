import os
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename

from utils import get_python_version

py_version = get_python_version()
if py_version >= 31:
    import fleep
else:
    import fleep27 as fleep

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

ALLOWED_FILE_TYPE_MAPPING = {
    'pdf': 'application/pdf',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation'

}
ALLOWED_EXTENSIONS = set(ALLOWED_FILE_TYPE_MAPPING.keys())
ALLOWED_MIME_TYPES = set(ALLOWED_FILE_TYPE_MAPPING.values())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files.get('file', None)
    # print(upload_file.content_length)
    # print(upload_file.content_length)
    # print(upload_file.mimetype)
    # print(upload_file.content_type)
    # print(upload_file.headers)

    if not upload_file or not upload_file.filename:
        return "NOT EXIST FILE"

    if upload_file and allowed_file(upload_file.filename):
        filename = secure_filename(upload_file.filename)
        save_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('SAVE_FILE_PATH : {}'.format(save_file_path))
        upload_file.save(save_file_path)

        with open(save_file_path, "rb") as file:
            info = fleep.get(file.read(128))
            mime_type = info.mime

        if mime_type and allowed_mime(mime_type):
            return "SAVED : {}".format(save_file_path)
        else:
            os.remove(save_file_path)
            return 'INVALID MIMETYPE : {}'.format(mime_type)
    else:
        return 'INVALID FILE'


def allowed_mime(mime_type):
    return len(set(mime_type).intersection(ALLOWED_MIME_TYPES)) == len(mime_type)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0')

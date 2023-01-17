from flask import Flask, request, render_template, jsonify, send_file, make_response, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/static/uploads', methods=['GET'])
def download(file_name):
    return send_file(f'images/{file_name}', as_attachment=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            c_name = file.filename.rsplit('.', 1)[0] + '.png'
            c_img_path = os.path.join(app.config['UPLOAD_FOLDER'], c_name)
            file.save(image_path)
            image = Image.open(image_path)
            image.save(c_img_path, optimize=True, quality=95)
            response = make_response()
            # make_response(redirect(url_for('download', file_name=c_img_path)))
            # make_response(send_file(os.path.join(app.config['UPLOAD_FOLDER'], file.filename.rsplit('.', 1)[0] + '.png'), as_attachment=True))
            response.headers.add('message', 'Image compressed successfully')
            response.headers.add('file_name', c_name)
            return response
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')

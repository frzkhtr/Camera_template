from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ensure this directory exists
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File successfully uploaded'
    else:
        return 'Allowed file types are png, jpg, jpeg, gif'

@app.route('/upload_camera', methods=['POST'])
def upload_camera():
    image_data = request.form['image']
    if image_data:
        image_data = image_data.split(",")[1]
        filename = secure_filename("camera_image.png")
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as fh:
            fh.write(base64.b64decode(image_data))
        return 'Camera image successfully uploaded'
    return 'Failed to upload camera image'

if __name__ == "__main__":
    # app.run(debug=True, host = '0.0.0.0', port = 5000)
    app.run(debug = True)

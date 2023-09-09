import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, flash, redirect, url_for
import cv2

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"The Operation is {operation} and the filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "png":
            new = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(new, img)
            return new
        case "jpg":
            new = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(new, img)
            return new
        case "webp":
            new = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(new, img)
            return new
        case "grayscale":
            new = f"static/{filename}"
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(new, imgProcessed)
            return new
        case "resize50":
            new = f"static/{filename}"
            imgProcessed = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
            cv2.imwrite(new, imgProcessed)
            return new
        case "mirror":
            new = f"static/{filename}"
            imgProcessed = cv2.flip(img, 1)
            cv2.imwrite(new, imgProcessed)
            return new
        case "squarecrop":
            new = f"static/{filename}"
            min_dimension = min(img.shape[0], img.shape[1])
            x1 = (img.shape[1] - min_dimension) // 2
            x2 = x1 + min_dimension
            y1 = (img.shape[0] - min_dimension) // 2
            y2 = y1 + min_dimension
            imgProcessed = img[y1:y2, x1:x2]
            cv2.imwrite(new, imgProcessed)
            return new


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == 'POST':
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "Error: No Selected File"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(
                f"Your image has been processed and is available <a target='_blank' href='/{new}'>here</a>")

            return redirect(url_for("home"))


app.run(debug=True)

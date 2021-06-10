import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(BASE_DIR)

SECRET_KEY = os.environ.get("SECRET_KEY", "default")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["IMAGE_UPLOADS"] = os.path.join(BASE_DIR, "static")
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ("jpeg", "jpg", "png", "gif")
app.config["MAX_IMAGE_SIZE"] = 1024 * 1024 * 8


def allowed_image(filename):
    return (
        "." in filename
        and filename.split(".")[-1].lower()
        in app.config["ALLOWED_IMAGE_EXTENSIONS"]
    )


def allowed_image_filesize(filesize):
    return int(filesize) <= app.config["MAX_IMAGE_SIZE"]


def get_latest_image(
    dirpath=app.config["IMAGE_UPLOADS"],
    valid_extensions=app.config["ALLOWED_IMAGE_EXTENSIONS"],
):
    valid_files = [
        os.path.join(dirpath) + "/" + filename
        for filename in os.listdir(dirpath)
    ]
    valid_files = [
        f
        for f in valid_files
        if "." in f
        and f.split(".")[-1] in valid_extensions
        and os.path.isfile(f)
    ]
    if not valid_files:
        return ""
    return max(valid_files, key=os.path.getmtime)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    return redirect(request.url)

                image = request.files["image"]
                if image.filename == "":
                    return redirect(request.url)

                if allowed_image(image.filename):
                    image.save(
                        os.path.join(
                            app.config["IMAGE_UPLOADS"], image.filename
                        )
                    )
                    return redirect(request.url)
                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    image = get_latest_image().split("/")[-1] if session.get("visit") else None
    if "visit" not in session:
        session["visit"] = True
    return render_template("index.html", last_image=image)


@app.route("/rotate/<string:angle>", methods=["GET", "POST"])
def rotate(angle):
    with Image.open(get_latest_image()) as image:
        if angle == "left":
            image.rotate(90, expand=True).save(
                os.path.join(app.config["IMAGE_UPLOADS"], image.filename),
                quality=100,
                subsampling=0,
            )
        else:
            image.rotate(270, expand=True).save(
                os.path.join(app.config["IMAGE_UPLOADS"], image.filename),
                quality=100,
                subsampling=0,
            )
    return redirect("/")


@app.route("/get-image")
def get_image():
    try:
        return send_from_directory(
            directory=app.config["IMAGE_UPLOADS"],
            path=get_latest_image().split("/")[-1],
            as_attachment=True,
        )
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

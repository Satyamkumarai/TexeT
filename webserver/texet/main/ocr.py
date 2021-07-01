
import os
import shlex
from subprocess import PIPE, run
from tempfile import TemporaryDirectory

from flask import (
    Flask,
    Response,
    abort,
    flash,
    redirect,
    request,
    send_from_directory,
    url_for,current_app
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "secret"
app.config['MAX_CONTENT_LENGTH'] = 50_000_000
app.config.from_envvar("OCRMYPDF_WEBSERVICE_SETTINGS", silent=True)

ALLOWED_EXTENSIONS = set(["pdf"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def do_ocrmypdf(file):
    uploaddir = TemporaryDirectory(prefix="ocrmypdf-upload")
    downloaddir = TemporaryDirectory(prefix="ocrmypdf-download")

    filename = secure_filename(file.filename)
    up_file = os.path.join(uploaddir.name, filename)
    file.save(up_file)
    print(up_file)

    down_file = os.path.join(downloaddir.name, filename)

    # cmd_args = [arg for arg in shlex.split(request.form["params"])]
    # if "--sidecar" in cmd_args:
        # return Response("--sidecar not supported", 501, mimetype='text/plain')

    ocrmypdf_args = ["ocrmypdf","--force-ocr", up_file, down_file]
    proc = run(ocrmypdf_args, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    if proc.returncode != 0:
        stderr = proc.stderr
        return Response(stderr, 400, mimetype='text/plain')
    print("Returning pdf!")
    return send_from_directory(downloaddir.name, filename)



from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    Response,
    json)
from .ocr import allowed_file ,do_ocrmypdf
bp = Blueprint('main',__name__)

@bp.route('/',methods = ['GET'])
def root():
    return render_template("index.html",title="TexeT")
    

@bp.route('/uploadpdf',methods=['GET'])
def uploadpdf():
    return render_template("upload/upload.html")

@bp.route('/scan',methods=['GET'])
def scan():
    return render_template("scan.html",title="TeXeT")

def add_file_to_db(file):
    pass

def json_resp(msg,error=0,url=""):
    """add the message and return jsonobj as  string"""
    d = {"message":msg,
        "error":error,
    }
    if url:
        d["downloadUrl"]=url
    return json.dumps(d)
@bp.route("/pdf/upload",methods=['POST'])
def process_pdf():
    if request.method == "POST":
        if "file" not in request.files:
            return Response(json_resp("No file in POST",1), 400, mimetype='application/json')
        file = request.files["file"]
        if file.filename == "":
            return Response(json_resp("Empty filename",1), 400, mimetype='application/json')
        if not allowed_file(file.filename):
            return Response(json_resp("Invalid filename",1), 400, mimetype='application/json')
        if file and allowed_file(file.filename):
            add_file_to_db(file)   # set the status to upload
            url = url_for('main.download_pdf',uuid="unique")

            return Response(json_resp("File Uploaded!",0,url))
        return Response(json_resp("Some other problem",1), 400, mimetype='application/json')


@bp.route("/pdf/download/<uuid>" ,methods=['GET'])
def download_pdf(uuid):
    return "Downloading.."
    pass
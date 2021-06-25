from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for)
bp = Blueprint('main',__name__)

@bp.route('/',methods = ['GET'])
def root():
    return render_template("index.html",title="TexeT")
    

@bp.route('/uploadpdf',methods=['GET'])
def uploadpdf():
    return "<h1>UPLOAD PDF</h1> <a href='https://stackoverflow.com/questions/8659808/how-does-http-file-upload-work' >Click</a>"
    # print(request.form)
    # return redirect(url_for('main.root'))

@bp.route('/scan',methods=['GET'])
def scan():
    return render_template("scan.html",title="TeXeT")
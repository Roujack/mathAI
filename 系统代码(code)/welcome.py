# from flask import Flask,url_for
# application = Flask(__name__)
#
# @application.route('/')
# def hello_world():
#     return 'Hello, World!'
#
# with application.test_request_context():
#     print url_for('static', filename='1.png')

import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import time
import solver
# from import application as applicationlication
# from app import application
UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


application = Flask(__name__)
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = str(int(time.time()))+'.'+file.filename.rsplit('.', 1)[1]
            # print("filename=",filename)
            save_file_path = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            file.save(save_file_path)
            result_file = solver.solve(save_file_path)
            # return redirect(url_for('uploaded_file',filename=filename))
            # print('yessssssssssssss')
            return '''
                    <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>test</title>



                <style>
                body
                {
                    //background-color:RGB(0,255,0);
                    background-image:url('static/background.png');
                    background-size:150%,200%;
                    background-repeat:no-repeat;
                    background-position:center,top;

                }

                .logo{
                    //border-style:solid;
                    //border-width:5px;
                    margin: auto;
                    text-align: center;
                    margin-top:3%;
                    color:white;

                }
                . content{
                    text-align: center;
                    margin-top:3%;
                }
                img {
                    border-radius: 16px;
                    max-height: 300%;
                    max-width:300%;
                    height: auto;
                }
                p{
                    font-size:18px;
                }
                    div.img:hover {
                    border: 1px solid #777;
                }
                div.img {
                    margin: 5px;
                    border: 1px solid #ccc;
                    float: left;
                    width: 700px;
                }
                div.img img {
                    width: 100%;
                    height: auto;
                }

                div.desc {
                    padding: 15px;
                    text-align: center;
                    color:white;
                    font-size:18px;
                }
                </style>

                </head>
                <body>

                    <div class="logo" >
                        <img src="static/logo.png" >
                    </div>

                    <div class="logo" ><form action="" method=post enctype=multipart/form-data>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form></div>


            <div align="center">
                <div  align="left">
                <div class="img">
                <a target="_blank" href="'''+url_for('uploaded_file',filename=filename)+'''">
                  <img src="'''+url_for('uploaded_file',filename=filename)+'''" alt="输入的图片" width="1000" height="800">
                </a>
                <div class="desc">input image</div>
                </div>
                </div>

                <div align="right">
                <div class="img">
                <a target="_blank" href="assets/img/output.png">
                  <img src="/uploads/'''+result_file+'''.png" alt="输出的图片" width="1000" height="800">
                </a>
                <div class="desc">output image</div>
                </div>
                </div>
                </div>



                <div class="logo">
                    <p>这是手写数学计算题的识别与自动求解系统的demo，上传一张包含计算题的图片，输出识别结果、计算过程以及计算结果。</p>
                    <p>目前能够处理算术表达式、分式表达式、乘方表达式、根号表达式，还支持一元二次方程求解、求定积分、求导、求极限。</p>
                </div>
                </body>
                </html>

                    '''

    else:

        return '''
            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>test</title>


          
        <style>
        body
        {
            //background-color:RGB(0,255,0);
            background-image:url('static/background.png');
            background-size:150%,200%;
            background-repeat:no-repeat;
            background-position:center,top;

        }

        .logo{
            //border-style:solid;
            //border-width:5px;
            margin: auto;
            text-align: center;
            margin-top:3%;
            color:white;

        }
        . content{
            text-align: center;
            margin-top:3%;
        }
        img {
            border-radius: 16px;
            max-height: 300%;
            max-width:300%;
            height: auto;
        }
        p{
            font-size:18px;
        }
            div.img:hover {
            border: 1px solid #777;
        }
        div.img {
            margin: 5px;
            border: 1px solid #ccc;
            float: left;
            width: 700px;
        }
        div.img img {
            width: 100%;
            height: auto;
        }

        div.desc {
            padding: 15px;
            text-align: center;
            color:white;
            font-size:18px;
        }
        </style>

        </head>
        <body>

            <div class="logo" >
                <img src="static/logo.png" >
            </div>

            <div class="logo" ><form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form></div>


            



        <div class="logo">
                <p>这是手写数学计算题的识别与自动求解系统的demo，上传一张包含计算题的图片，输出识别结果、计算过程以及计算结果。</p>
                <p>目前能够处理算术表达式、分式表达式、乘方表达式、根号表达式，还支持一元二次方程求解、求定积分、求导、求极限。</p>
            </div>
        </body>
        </html>

            '''



@application.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(application.config['UPLOAD_FOLDER'],filename)
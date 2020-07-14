from flask import Flask,g,make_response,Response,url_for,request,render_template
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


import os
app = Flask(__name__)
app.debug = True

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,db)


# 기본페이지
@app.route("/")
def helloworld():
    return os.getcwd()


##################
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response",201,{'test':'tttt'})
    return make_response(custom_res)

@app.route('/test')
def test():
    return render_template('navbar.html',title='테스트 페이지')


# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if valid_login(request.form['username'],
#                        request.form['password']):
#             return log_the_user_in(request.form['username'])
#         else:
#             error = 'Invalid username/password'
#     # 아래의 코드는 요청이 GET 이거나, 인증정보가 잘못됐을때 실행된다.
#     return render_template('login.html', error=error)

# @app.route('/login',methods=['POST','GET'])
# def login():
#     if request.method =='POST':
#         return 'post'
#     else:
#         return 'get'

# *** GET 방식으로 넘어온 ?key=value 질의문자열 접근방법
# searchword = request.args.get('key', '')

@app.route('/arg/<int:send_int>')
def show_postint(send_int):
    return '숫자가 날라왔음 {}'.format(send_int)

# ***path : like the default but also accepts slashes

@app.route('/arg/<strings>')
def show_string(strings):
    return '글자가 날라왔음 {}'.format(strings)

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/test_wsgi')
def wsgi_test():
    # environ == Flask 환경변수를 담고있다.
    def application(environ,start_response):
        body='The request method was {}'.format(environ['REQUEST_METHOD'])
        headers =[('Content-Type','text/plain'),
                  ('Content-Length',str(len(body)))]
        start_response('200 OK',headers)
        return [body]
    return make_response(application)

@app.route('/index')
def index():
    sample = '이건 샘플 텍스트'
    g.title = 'This is Title'

    glist = ['a','b','c']

    posts = [
        {
            'name' : '이동기',
            'age' : 27,
            'job' : '취준생'
        },
        {
            'name': '삼동기',
            'age': 37,
            'job': '셀럽'
        }


    ]
    return render_template('index.html',sample=sample,glist=glist,posts=posts)



@app.errorhandler(404)
def page_not_found(error):
    return '이페이지 없는딩',404


@app.before_request # 요청 시작전에 실행
def before_request():
    print("before_request!! 난 무조건 처음에나와")
    g.str = '이동기'    # g는 application context(영역)이다.

# @app.route('/gtest')
# def helloworld2():
#     return 'global test' + getattr(g,'str','없으면이거')
#


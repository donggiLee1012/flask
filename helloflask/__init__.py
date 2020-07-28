from flask import Flask,g,make_response,Response,url_for,request,render_template,redirect
from config import Config



import os
app = Flask(__name__)
app.debug = True

posts_contain={

}
# 기본페이지
@app.route("/")
def helloworld():

    # 크롤링 결과의 수만큼 매개변수로받고
    # 받은 매개변수만큼 반복문을 돌리고
    # 돌릴 반복문은 태그 생성자

    #몇개의 댓글 몇개의댓글인지만
    colums = ['받아온값','또받아온값','한번더받아온값']
    rows =['행','행2']


    mk_colums='<thead><tr>'
    for i in colums:
        mk_colums += '<th>{columm}</th>'.format(columm=i)
    mk_colums += '</tr></thead>'


    mk_row='<tbody>'
    # for i in rows:
    #
    #     mk_row += '''
    #     <tr>
    #     <td><a href="{url}">{youtuber}</a></td>
    #     <td>{name}</td>
    #     <td>{comments}</td>
    #     <td>{like}</td>
    #     </tr>
    #     '''.format(i)

    mk_row += '</tbody>'


    return mk_colums


##################
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response",201,{'test':'tttt'})
    return make_response(custom_res)

@app.route('/test')
def test():



    return render_template('main.html',title='메인페이지',posts_contain = posts_contain)


@app.route('/crwaling')
def crwaling():


    return render_template('crawling.html',posts_contain=posts_contain)

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

# @app.route('/test_wsgi')
# def wsgi_test():
#     # environ == Flask 환경변수를 담고있다.
#     def application(environ,start_response):
#         body='The request method was {}'.format(environ['REQUEST_METHOD'])
#         headers =[('Content-Type','text/plain'),
#                   ('Content-Length',str(len(body)))]
#         start_response('200 OK',headers)
#         return [body]
#     return make_response(application)

@app.route('/youtube')
def youtube():
    return render_template('youtube.html')


@app.route('/youtube/comments', methods=['GET','POST'])
def testsmaple():

    if request.method == 'POST':
        # uname = request.form['youtubename']
        # cnt = request.form['cnt']
        # reple_cnt = request.form['reple_cnt']
        args = request.form['youtubename']
        cnt = request.form['cnt']
        reple_cnt = request.form['reple_cnt']

        return '{}{}{}'.format(args,cnt,reple_cnt)




    elif request.method == 'GET':

        # searchword = request.args.get('youtubename')
        # cnt = request.args.get('cnt')
        # reple_cnt = request.args.get('reple_cnt')
        args = request.args['youtubename']


        return args

    else :
        return redirect(url_for('page_not_found'))



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


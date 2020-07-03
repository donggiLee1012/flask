from flask import Flask,g,make_response,Response

app = Flask(__name__)
app.debug = True

# 기본페이지
@app.route("/")
def helloworld():
    return 'HI this is flask'
###################333
@app.route('/res1')
def res1():
    custom_res = Response("Custom Response",201,{'test':'tttt'})
    return make_response(custom_res)

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

#
# @app.before_request # 요청 시작전에 실행
# def before_request():
#     print("before_request!! 난 무조건 처음에나와")
#     g.str = '한글'    # g는 application context(영역)이다.
#
# @app.route('/gtest')
# def helloworld2():
#     return 'global test' + getattr(g,'str','없으면이거')
#


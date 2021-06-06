"""
spark streaming 程序，用于实时接收前端传过来的参数，并且计算结果返回
热词查询
"""
import logging.config
from optparse import OptionParser
import os
from sanic import Sanic
from sanic import response
from sanic.response import text, json, redirect
from src.controller.orm_controller import OrmController

workdir = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))  # nopep8
if "lib" == os.path.basename(workdir):
    workdir = os.path.dirname(workdir)
app = Sanic('给你的项目起个名')


def _handle_cmd_line(args=None):
    parser = OptionParser()

    parser.add_option("--id", dest="id", action="store",
                      type="string", default="0",
                      help="id use guard and create log file")
    parser.add_option("--logconfig", dest="logconfig", action="store",
                      type="string",
                      default=os.path.join(
                          workdir, 'etc',
                          'sanic_service.log.conf'),
                      help="log config file [%default]")
    (options, args) = parser.parse_args(args=args)
    return options, args


def _valid_options(_options):
    # TODO(lihongjie): 后面可能增加其他参数，用作参数检查
    return True


def process():
    pass


@app.route('/tag/<tag>')
async def tag_handler(request, tag):
    return text('Tag - {}'.format(tag))


@app.route('/number/<integer_arg:int>')
async def integer_handler(request, integer_arg):
    return text('Integer - {}'.format(integer_arg))


@app.route('/number/<number_arg:number>')
async def number_handler(request, number_arg):
    return text('Number - {}'.format(number_arg))


@app.route('/person/<name:[A-z]>')
async def person_handler(request, name):
    return text('Person - {}'.format(name))


@app.route('/folder/<folder_id:[A-z0-9]{0,4}>')
async def folder_handler(request, folder_id):
    return text('Folder - {}'.format(folder_id))


@app.route('/post', methods=['POST'])
async def post_handler(request):
    print(request.json)
    return text('POST request - {}'.format(request.json))


@app.route('/get', methods=['GET'], host='example.com')
async def get_handler(request):
    return text('GET request - {}'.format(request.args))


# if the host header doesn't match example.com, this route will be used
@app.route('/get', methods=['GET'])
async def get_handler(request):
    return text('GET request in default - {}'.format(request.args))


@app.route('/')
async def index(request):
    # generate a URL for the endpoint `post_handler`
    url = app.url_for('post_handler', post_id=5)
    # the URL is `/posts/5`, redirect to it
    return redirect(url)


# Sanic默认是使用GET的，想使用POST的话，需要在路由装饰器中修改methods选项
@app.route('/test-json', methods=['POST'])
async def test_json(request):
    # 使用request.json来接收json对象
    print(request.json)
    # Sanic内置json，直接使用这种形式就能返回json对象
    return json({'data': 'True'})


@app.route('/QueryData', methods=["POST"])
async def query_data(request):
    orm_controller = OrmController()
    query_result = orm_controller.query_data_controller(request.json)
    return json(query_result)


def main():
    try:
        options, _args = _handle_cmd_line()
        if options.logconfig:
            defaults = {"id": options.id}
            logging.config.fileConfig(options.logconfig, defaults)
        if not _valid_options(options):
            logging.error("options:\n" +
                          '\n'.join('%s = %s' %
                                    (d, getattr(options, d))
                                    for d in options.__dict__))
            return

        logging.info("start sanic service")
        # 和Flask很相似的启动方法，绑定IP，端口号，可以选择消息等级。
        app.run(host='0.0.0.0', port=8800, debug=True)

    except Exception as exception:
        logging.exception(exception)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
        exit(-1)

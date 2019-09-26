# @File  : tornadoTest.py
# @Author: LiuXingsheng
# @Date  : 2019/5/5
# @Desc  :

import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('你真好看呢')


if __name__ == '__main__':
    app = tornado.web.Application([(r'/', IndexHandler)])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

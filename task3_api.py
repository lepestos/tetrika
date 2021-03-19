import json

from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop

from task3 import appearance


"""
URL: '/'
Method: GET
Data parameters: object, corresponding to intervals dictionary
"""


class AppearanceHandler(RequestHandler):
    def get(self):
        self.write({'answer': appearance(json.loads(self.request.body))})


def make_app():
    urls = [("/", AppearanceHandler)]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3333)
    IOLoop.instance().start()

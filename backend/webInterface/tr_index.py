import os

import tornado.template

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Index(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render(os.path.join(BASE_PATH, 'dist/qa_ui/index.html'))

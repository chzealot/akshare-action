import os
import asyncio
import tornado
import mimetypes
import api

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

mimetypes.add_type('text/yaml; charset=utf-8', '.yaml')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/api/news_cctv', api.NewsCctvHandler),
        (r'/(openapi.yaml)', tornado.web.StaticFileHandler, {'path': STATIC_ROOT}),
    ])


async def main():
    app = make_app()
    app.listen(3024)
    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(main())

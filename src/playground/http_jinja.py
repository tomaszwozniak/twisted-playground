from datetime import datetime
import sys

from jinja2 import Environment, PackageLoader

from twisted.internet import reactor
from twisted.web import http
from twisted.python import log


env = Environment(loader=PackageLoader('playground', 'templates'))


def render_template(template_file, **kwargs):
    return env.get_template(template_file).render(**kwargs).encode('utf-8')


class HTTPRequestHandler(http.Request):
    resources = {
        '/': render_template('index.html', now=datetime.utcnow()),
        '/about/': render_template('about.html')
    }

    def process(self):
        self.setHeader('Content-Type', 'text/html')

        if self.path in self.resources.keys():
            self.write(self.resources[self.path])
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write('<h2>Not found</h2>')

        self.finish()


class MyHTTP(http.HTTPChannel):
    requestFactory = HTTPRequestHandler


class MyHTTPFactory(http.HTTPFactory):

    def buildProtocol(self, addr):
        return MyHTTP()


def main():
    log.startLogging(sys.stdout)

    reactor.listenTCP(8000, MyHTTPFactory())
    reactor.run()

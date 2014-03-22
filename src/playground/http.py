import sys

from twisted.internet import reactor
from twisted.web import http
from twisted.python import log


class HTTPRequestHandler(http.Request):
    resources = {
        '/': '<h2>Main page</h2>',
        '/about/': '<h2>About me</h2>'
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


if __name__ == '__main__':
    main()

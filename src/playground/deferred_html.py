from __future__ import print_function

from twisted.internet.defer import Deferred


def addBold(result):
    return '<b>{0}</b>'.format(result)


def addItalic(result):
    return '<i>{0}</i>'.format(result)


def printHTML(result):
    print(result)


def main():
    d = Deferred()

    d.addCallback(addBold)
    d.addCallback(addItalic)
    d.addCallback(printHTML)

    d.callback('Hello world!')


if __name__ == '__main__':
    main()

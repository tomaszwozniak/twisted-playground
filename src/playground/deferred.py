from __future__ import print_function

from twisted.internet.defer import Deferred


def onSucces(result):
    if 'foo' not in result.lower():
        raise Exception(result)
    return 'Success on: {0}'.format(result)


def onFailure(failure):
    return 'Failure on: {0}'.format(failure)


def getDeferred():
    d = Deferred()
    d.addCallback(onSucces)
    d.addErrback(onFailure)
    d.addBoth(print)

    return d


def main():
    getDeferred().callback('Foo Bar')
    getDeferred().callback('Wahoo')


if __name__ == '__main__':
    main()

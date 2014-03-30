import sys

from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.python import log
from twisted.words import service


def main():
    log.startLogging(sys.stdout)

    wordsRealm = service.InMemoryWordsRealm('twisted-playground.org')
    wordsRealm.createGroupOnRequest = True

    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(admin='admin')

    ircPortal = portal.Portal(wordsRealm, [checker])

    factory = service.IRCFactory(wordsRealm, ircPortal)

    reactor.listenTCP(6666, factory)
    reactor.run()

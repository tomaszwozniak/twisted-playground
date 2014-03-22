import sys

from twisted.conch import manhole, manhole_ssh
from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.python import log


def getManholeFactory(namespace, **passwords):
    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = (
        lambda _: manhole.Manhole(namespace)
    )

    p = portal.Portal(realm)
    p.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords)
    )

    f = manhole_ssh.ConchFactory(p)

    return f


def main():
    log.startLogging(sys.stdout)
    reactor.listenTCP(2222, getManholeFactory(globals(), admin='admin'))
    reactor.run()


if __name__ == '__main__':
    main()

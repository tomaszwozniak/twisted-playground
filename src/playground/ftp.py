import os
import sys

from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.protocols import ftp
from twisted.python import log


def main():
    log.startLogging(sys.stdout)

    ftpDir = os.environ['FTP_DIR']
    realm = ftp.FTPRealm(ftpDir, userHome=ftpDir)

    ftpFactory = ftp.FTPFactory()
    ftpFactory.portal = portal.Portal(realm)

    ftpFactory.portal.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(admin='admin')
    )

    reactor.listenTCP(8021, ftpFactory)
    reactor.run()


if __name__ == '__main__':
    main()

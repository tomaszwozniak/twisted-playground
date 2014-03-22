import os
import sys

from twisted.conch import avatar, interfaces, recvline
from twisted.conch.insults import insults
from twisted.conch.ssh import factory, keys, session
from twisted.cred import checkers, portal
from twisted.internet import reactor
from twisted.python import log

from zope.interface import implements


class SSHProtocol(recvline.HistoricRecvLine):

    def __init__(self, user):
        self.user = user

    def do_echo(self, *args):
        self.terminal.write(' '.join(args))

    def do_quit(self):
        self.terminal.loseConnection()

    def getCommand(self, cmd):
        return getattr(self, 'do_{0}'.format(cmd), None)

    def lineReceived(self, line):
        if line:
            line = line.strip().split()
            cmd = line[0]
            args = line[1:]

            command = self.getCommand(cmd)

            if command:
                try:
                    command(*args)
                except Exception, e:
                    self.terminal.write('Error: {0}'.format(e))
            else:
                self.terminal.write('No such command: {0}'.format(cmd))

        self.terminal.nextLine()
        self.terminal.write(self.ps[self.pn])


class SSHAvatar(avatar.ConchUser):
    implements(interfaces.ISession)

    def __init__(self, username):
        # cannot do super
        avatar.ConchUser.__init__(self)

        self.username = username
        self.channelLookup['session'] = session.SSHSession

    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(SSHProtocol, self)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, *args):
        return None

    def execCommand(self, *args):
        raise NotImplementedError()

    def closed(self):
        pass


class SSHRealm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], SSHAvatar(avatarId), lambda: None


def getRSAKeys():
    with open(
        os.path.join(os.environ['SSH_KEYS_DIR'], 'id_rsa')
    ) as privateBlobFile:
        privateBlob = privateBlobFile.read()
        privateKey = keys.Key.fromString(data=privateBlob)

    with open(
        os.path.join(os.environ['SSH_KEYS_DIR'], 'id_rsa.pub')
    ) as publicBlobFile:
        publicBlob = publicBlobFile.read()
        publicKey = keys.Key.fromString(data=publicBlob)

    return publicKey, privateKey


def main():
    log.startLogging(sys.stdout)

    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(SSHRealm())

    sshFactory.portal.registerChecker(
        checkers.InMemoryUsernamePasswordDatabaseDontUse(admin='admin')
    )

    publicKey, privateKey = getRSAKeys()
    sshFactory.publicKeys = {'ssh-rsa': publicKey}
    sshFactory.privateKeys = {'ssh-rsa': privateKey}

    reactor.listenTCP(2222, sshFactory)
    reactor.run()


if __name__ == '__main__':
    main()

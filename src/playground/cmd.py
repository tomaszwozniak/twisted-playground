import sys

from twisted.internet import protocol, reactor
from twisted.python import log


class CommandProtocol(protocol.Protocol):

    def write(self, msg):
        self.transport.write('{0}\n'.format(msg))

    def do_echo(self, *args):
        self.write(' '.join(args))

    def getCommand(self, cmd):
        return getattr(self, 'do_{0}'.format(cmd), None)

    def dataReceived(self, data):
        if not data:
            return

        data = data.strip().split()
        cmd = data[0]
        args = data[1:]

        command = self.getCommand(cmd)

        if not command:
            self.write('No such command: {0}'.format(cmd))
            return

        try:
            command(*args)
        except Exception, e:
            self.write('Error: {0}'.format(e))


class CommandFactory(protocol.Factory):

    def buildProtocol(self, addr):
        return CommandProtocol()


def main():
    log.startLogging(sys.stdout)

    reactor.listenTCP(8000, CommandFactory())
    reactor.run()


if __name__ == '__main__':
    main()

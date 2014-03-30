import sys

from twisted.internet import protocol, reactor
from twisted.words.protocols import irc
from twisted.python import log


class EchoBot(irc.IRCClient):

    def __init__(self, nickname, channel):
        self.nickname = nickname
        self.channel = channel

    def signedOn(self):
        self.join(self.channel)

    def privmsg(self, user, channel, msg):
        message = '{} wrote: {}'.format(user, msg)

        if channel == self.nickname:
            self.msg(user, message)
            return

        self.msg(channel, message)

    def action(self, user, channel, action):
        self.describe(channel, '{} with {}'.format(action, user))


class EchoBotFactory(protocol.ClientFactory):

    def __init__(self, nickname, channel):
        self.nickname = nickname
        self.channel = channel

    def buildProtocol(self, addr):
        proto = EchoBot(self.nickname, self.channel)
        proto.factory = self

        return proto

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()


def main():
    log.startLogging(sys.stdout)

    network, port, nickname, channel = sys.argv[1:]
    port = int(port)

    reactor.connectTCP(network, port, EchoBotFactory(nickname, channel))
    reactor.run()


if __name__ == '__main__':
    main()

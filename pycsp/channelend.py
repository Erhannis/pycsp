"""
Channelend module

Copyright (c) 2009 John Markus Bjoerndalen <jmb@cs.uit.no>,
      Brian Vinter <vinter@diku.dk>, Rune M. Friborg <runef@diku.dk>.
See LICENSE.txt for licensing details (MIT License). 
"""
import protocol
from exceptions import *
from pycsp.common.const import *

# Functions
def retire(*list_of_channelEnds):
    """ Retire reader or writer, to do auto-poisoning
    When all readers or writer of a channel have retired. The channel is retired.
    
    >>> from __init__ import *
    >>> C = Channel()
    >>> cout1, cout2 = C.writer(), C.writer()
    >>> retire(cout1)

    >>> Spawn(Process(cout2, 'ok'))

    >>> try:
    ...     cout1('fail')
    ... except ChannelRetireException:
    ...     True
    True

    >>> cin = C.reader()
    >>> retire(cin)
    """    
    for channelEnd in list_of_channelEnds:
        channelEnd.retire()

def poison(*list_of_channelEnds):
    """ Poison channel
    >>> from __init__ import *

    >>> @process
    ... def P1(cin, done):
    ...     try:
    ...         while True:
    ...             cin()
    ...     except ChannelPoisonException:
    ...         done(42)

    >>> C1, C2 = Channel(), Channel()
    >>> Spawn(P1(C1.reader(), C2.writer()))
    >>> cout = C1.writer()
    >>> cout('Test')

    >>> poison(cout)
    
    >>> cin = C2.reader()
    >>> cin()
    42
    """
    for channelEnd in list_of_channelEnds:
        channelEnd.poison()

# Classes
class ChannelEndWrite:
    def __init__(self, channel):
        self.channel = channel
        self.op = WRITE

        # Prevention against multiple retires
        self.isretired = False

        self.__call__ = self.channel._write
        self.poison = self.channel.poison

    def post_write(self, process, msg):
        protocol.post_write(self.channel, process, msg)

        
    def _retire(self, msg):
        raise ChannelRetireException()

    def retire(self):
        if not self.isretired:
            self.channel.retire_writer()
            self.__call__ = self._retire
            self.isretired = True

    def __repr__(self):
        if self.channel.name == None:
            return "<ChannelEndWrite wrapping %s>" % self.channel
        else:
            return "<ChannelEndWrite wrapping %s named %s>" % (self.channel, self.channel.name)

    def isWriter(self):
        return True

    def isReader(self):
        return False

class ChannelEndRead:
    def __init__(self, channel):
        self.channel = channel
        self.op = READ

        # Prevention against multiple retires
        self.isretired = False

        self.__call__ = self.channel._read
        self.poison = self.channel.poison

    def post_read(self, process):
        protocol.post_read(self.channel, process)

    def _retire(self):
        raise ChannelRetireException()

    def retire(self):
        if not self.isretired:
            self.channel.retire_reader()
            self.__call__ = self._retire
            self.isretired = True

    def __repr__(self):
        if self.channel.name == None:
            return "<ChannelEndRead wrapping %s>" % self.channel
        else:
            return "<ChannelEndRead wrapping %s named %s>" % (self.channel, self.channel.name)

    def isWriter(self):
        return False

    def isReader(self):
        return True

# Run tests
if __name__ == '__main__':
    import doctest
    doctest.testmod()

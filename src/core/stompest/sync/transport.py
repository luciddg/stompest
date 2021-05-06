from __future__ import unicode_literals

import errno
import select # @UnresolvedImport
import socket
import time

import sys
from stompest._backwards import binaryType
from stompest.error import StompConnectionError
from stompest.protocol import StompParser

class StompFrameTransport(object):
    factory = StompParser

    READ_SIZE = 4096

    def __init__(self, host, port, sslContext=None):
        self.host = host
        self.port = port
        self.sslContext = sslContext

        self._poll = None
        self._socket = None
        self._parser = self.factory()

    def __str__(self):
        return '%s:%d' % (self.host, self.port)

    def canRead(self, timeout=None):
        def retry():
            if timeout is None:
                return self.canRead()

            return self.canRead(max(0, timeout - (time.time() - startTime)))

        self._check()
        if self._parser.canRead():
            return True

        startTime = time.time()
        try:
            result = self._poll.poll(timeout)
        except OSError as e:
            # In Python 3.5+, select itself handles retries on EINTR so this
            # error should never be raised spuriously. We hence don't want to
            # mask it for those versions, only for older versions.
            if e.errno == errno.EINTR and sys.version_info[:2] <= (3, 4):
                return retry()
            raise
        except select.error as e:
            # In Python 3 select.error is just a alias for OSError so this clause
            # should only apply to Python 2.
            code, _ = e
            if code == errno.EINTR:
                return retry()
            raise

        return bool(result)

    def connect(self, timeout=None):
        try:
            self._socket = socket.socket()
            self._socket.settimeout(timeout)
            if self.sslContext:
                self._socket = self.sslContext.wrap_socket(self._socket, server_hostname=self.host)
            self._socket.connect((self.host, self.port))
            self._poll = select.poll()
            self._poll.register(self._socket)
        except IOError as e:
            raise StompConnectionError('Could not establish connection [%s]' % e)
        self._parser.reset()

    def disconnect(self):
        try:
            self._poll and self._socket and self._poll.unregister(self._socket)
        except:
            pass
        finally:
            self._poll = None

        try:
            self._socket and self._socket.close()
        except IOError as e:
            raise StompConnectionError('Could not close connection cleanly [%s]' % e)
        finally:
            self._socket = None

    def receive(self):
        while True:
            frame = self._parser.get()
            if frame is not None:
                return frame
            try:
                data = self._socket.recv(self.READ_SIZE)
                if not data:
                    raise StompConnectionError('No more data')
            except (IOError, StompConnectionError) as e:
                self.disconnect()
                raise StompConnectionError('Connection closed [%s]' % e)
            self._parser.add(data)

    def send(self, frame):
        self._write(binaryType(frame))

    def setVersion(self, version):
        self._parser.version = version

    def _check(self):
        if not self._connected():
            raise StompConnectionError('Not connected')

    def _connected(self):
        return self._socket is not None

    def _write(self, data):
        self._check()
        try:
            self._socket.sendall(data)
        except IOError as e:
            raise StompConnectionError('Could not send to connection [%s]' % e)

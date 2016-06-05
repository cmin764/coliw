import argparse
import os
import threading
import urllib2
from StringIO import StringIO

from coliw import exceptions


EOL = "\n"
ENCODING = "utf-8"

PACKAGE = os.path.abspath(
    os.path.normpath(
        os.path.join(
            __file__,
            os.path.pardir,
        )
    )
)

USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36"
              " (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")
TIMEOUT = 10

OPENER = urllib2.build_opener()
OPENER.addheaders = [("User-agent", USER_AGENT)]


class WebArgumentParser(argparse.ArgumentParser):

    SIOS = {}

    def __init__(self, *args, **kwargs):
        super(WebArgumentParser, self).__init__(*args, **kwargs)
        self._ident = threading.current_thread().ident

    @property
    def sio(self):
        return self.SIOS.setdefault(self._ident, StringIO())

    @sio.deleter
    def sio(self):
        del self.SIOS[self._ident]

    def _print_message(self, message, file=None):
        if message:
            self.sio.write(message)
            self.sio.flush()

    def error(self, message):
        self.print_usage()
        raise exceptions.ParseError(message)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message)
        if status:
            raise exceptions.ParseError()
        raise exceptions.SuccessError()    # just for making the interrupt

"""A generic API for contactology"""
from __future__ import print_function

from six.moves.urllib.parse import urlencode
from pprint import pformat
import json

from twisted.web.client import getPage
from twisted.internet import defer
from twisted.python import log

__version__ = "2.0"

class APIError(Exception):
    """Base class for all api errors from contactology"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super(APIError, self).__init__("API Error: %s (%s)" % (message, code))


class Contactology(object):
    """Proxy object"""
    host = "api.emailcampaigns.net"
    path = "/2/REST/"
    _logio = False
    
    def __init__(self, key, useHTTPS=True):
        self.key = key
        self.useHTTPS = useHTTPS

    def _log_query(self, method, r):
        log.msg("SENT: %s: %s" % (method, pformat(r)))
        return r

    def __getattr__(self, name):
        def call_wrapper(**args):
            return self._call(name, **args)
        return call_wrapper

    @defer.inlineCallbacks
    def _call(self, method, **kw):
        if self._logio:
            self._log_query(method, kw)
        # serialize non-strings using json
        for k, v in list(kw.items()):
            if isinstance(v, str):
                kw[k] = v = v.encode('utf-8')
            if not isinstance(v, str):
                v = json.dumps(v)
                kw[k] = v
        # add our preset arguments
        kw.update({'key': self.key, 'method': method})
        # construct request data
        postdata = urlencode(kw)
        schema = self.useHTTPS and 'https' or 'http'
        url = '%s://%s%s' % (schema, self.host, self.path)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "User-Agent": "Twisted Wrapper %s" % __version__}
        resp = yield getPage(url, method='POST', headers=headers, postdata=postdata)
        # de-serialize response
        resp = json.loads(resp)
        if self._logio:
            log.msg("RECEIVED: %s" % pformat(resp))
        # check for errors
        if isinstance(resp, dict):
            if resp.get('result', None) == 'error':
                raise APIError(resp['code'], resp['message'])
        yield defer.returnValue(resp)

if __name__ == '__main__':
    from twisted.internet import reactor
    from pprint import pprint
    proxy = Contactology('Your API key here')
    @defer.inlineCallbacks
    def test():
        try:
            resp = yield proxy.List_Get_Active_Lists()
            print(resp)
            resp = yield proxy.List_Get_Active_Lists(optionalParameters={'offset': 1})
            print(resp)
            resp = yield proxy.List_Get_Info(listId=1)
            print(resp)
        finally:
            reactor.stop()
    reactor.callWhenRunning(test)
    reactor.run()

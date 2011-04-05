"""A generic API for contactology"""

import urllib
from pprint import pformat
try:
    import json
except ImportError:
    import simplejson as json

from twisted.web.client import getPage
from twisted.internet import defer
from twisted.python import log


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
    version = "0.2.1"
    _logio = False
    
    def __init__(self, key, useHTTPS=True):
        self.key = key
        self.useHTTPS = useHTTPS

    def _log_query(self, r):
        log.msg("SENT: %s" % pformat(r))
        return r

    def __getattr__(self, name):
        def call_wrapper(**args):
            return self._call(name, **args)
        return call_wrapper

    @defer.inlineCallbacks
    def _call(self, method, **kw):
        kw.update({'key': self.key, 'method': method})
        if self._logio:
            self._log_query(kw)
        # serialize non-strings using json
        for k, v in kw.items():
            if not isinstance(v, str):
                v = json.dumps(v)
                kw[k] = v
        # construct request data
        postdata = urllib.urlencode(kw)
        schema = self.useHTTPS and 'https' or 'http'
        url = '%s://%s%s' % (schema, self.host, self.path)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain",
                   "User-Agent": "Twisted Wrapper %s" % self.version}
        resp = yield getPage(url, method='POST', headers=headers, postdata=postdata)
        # de-serialize response
        resp = json.loads(resp)
        if self._logio:
            log.msg("RECEIVED: %s" % pformat(resp))
        # check for errors
        if not isinstance(resp, dict):
            raise Exception("Expected dict from contactology, got %s" % resp)
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
            print resp
            resp = yield proxy.List_Get_Active_Lists(optionalParameters={'offset': 1})
            print resp
            resp = yield proxy.List_Get_Info(listId=1)
            print resp
        finally:
            reactor.stop()
    reactor.callWhenRunning(test)
    reactor.run()

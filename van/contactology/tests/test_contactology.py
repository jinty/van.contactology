import unittest
from cgi import parse_qsl
from twisted.trial.unittest import TestCase
from twisted.internet import defer

from mock import patch, Mock
from van.contactology import Contactology, APIError, __version__

try:
    from json import dumps
except ImportError:
    from simplejson import dumps

def _parse_post(callargs):
    return sorted(parse_qsl(callargs['postdata'].decode('utf-8'), True, True))

class TestProxy(TestCase):

    @defer.inlineCallbacks
    def _call_once(self, api_key, result, method, *args, **kw):
        patcher = patch('van.contactology.getPage')
        getPage = patcher.start()
        try:
            getPage.return_value = dumps(result).encode('ascii')
            proxy = Contactology(api_key)
            method = getattr(proxy, method)
            out = yield method(*args, **kw)
        finally:
            patcher.stop()
        defer.returnValue((getPage, out))

    @defer.inlineCallbacks
    def test_list_return(self):
        getPage, out = yield self._call_once('API Key', [], 'Campaign_Find')
        self.assertEquals(out, [])

    @defer.inlineCallbacks
    def test_call_args(self):
        getPage, out = yield self._call_once('API Key', [], 'Campaign_Find')
        self.assertEquals(getPage.call_count, 1)
        self.assertEquals(getPage.call_args, ((b'https://api.emailcampaigns.net/2/REST/',),
                                                 {'headers': {b'Content-type': b'application/x-www-form-urlencoded',
                                                              b'User-Agent': b'Twisted Wrapper %s' % str(__version__).encode('ascii')},
                                                  'method': b'POST',
                                                  'postdata': b'key=API+Key&method=Campaign_Find'}))

    @defer.inlineCallbacks
    def test_api_error(self):
        d = self._call_once('API Key', {'code': 221, 'message': 'Key not found', 'result': 'error'}, 'List_Get_Active_Lists')
        yield self.failUnlessFailure(d, APIError)

    @defer.inlineCallbacks
    def test_unicode_api_key(self):
        getPage, out = yield self._call_once(u'unicode API Key', [], 'Campaign_Find')
        self.assertEquals(getPage.call_args[1]['postdata'], b'key=unicode+API+Key&method=Campaign_Find')

    @defer.inlineCallbacks
    def test_unicode_argument(self):
        getPage, out = yield self._call_once('API Key', [], 'Contact_Get', email=u"a@b.c")
        self.assertEquals(_parse_post(getPage.call_args[1]), [('email', 'a@b.c'), ('key', 'API Key'), ('method', 'Contact_Get')])

import unittest
from simplejson import dumps
from twisted.trial.unittest import TestCase
from twisted.internet import defer

from mock import patch, Mock
from van.contactology import Contactology, APIError

class TestProxy(TestCase):

    @defer.inlineCallbacks
    def test_list_return(self):
        patcher = patch('van.contactology.getPage')
        getPage = patcher.start()
        try:
            proxy = Contactology('API Key')
            getPage.return_value = dumps([])
            out = yield proxy.Campaign_Find()
            yield self.assertEquals(out, [])
        finally:
            patcher.stop()
    
    @defer.inlineCallbacks
    def test_api_error(self):
        patcher = patch('van.contactology.getPage')
        getPage = patcher.start()
        try:
            proxy = Contactology('API Key')
            getPage.return_value = dumps({'code': 221, 'message': 'Key not found', 'result': 'error'})
            yield self.failUnlessFailure(proxy.List_Get_Active_Lists(), APIError)
        finally:
            patcher.stop()

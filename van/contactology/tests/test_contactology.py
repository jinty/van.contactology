import unittest
from simplejson import dumps
from twisted.trial.unittest import TestCase
from twisted.internet import defer

from mock import patch, Mock
from van.contactology import Contactology

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

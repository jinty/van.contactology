import unittest
from twisted.trial.unittest import TestCase

from van.contactology import Contactology

class TestProxy(TestCase):

    def test_conn(self):
        conn = Contactology('API Key')

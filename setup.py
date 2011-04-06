import os
import re
from setuptools import setup, find_packages

_here = os.path.dirname(__file__)
_init = os.path.join(_here, 'van', 'contactology', '__init__.py')
_init = open(_init, 'r').read()

VERSION = re.search(r'^__version__ = "(.*)"', _init, re.MULTILINE).group(1)

setup(name="van.contactology",
      version=VERSION,
      packages=find_packages(),
      description="Contactology API for Twisted",
      namespace_packages=["van"],
      install_requires=[
          'pyOpenSSL',
          'setuptools',
          'Twisted',
          'simplejson',
                        ],
      test_suite="van.contactology.tests",
      tests_require=['mock'],
      include_package_data=True,
      zip_safe=False,
      )

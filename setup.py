import os
from setuptools import setup, find_packages

setup(name="van.contactology",
      version='1.0dev',
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

import os
from setuptools import setup, find_packages

setup(name="van.contactology",
      version='1.0dev',
      packages=find_packages(),
      description="Contactology API for Twisted",
      namespace_packages=["van"],
      install_requires = [
          'setuptools',
          'Twisted',
          'simplejson',
                        ],
      include_package_data = True,
      zip_safe = False,
      )

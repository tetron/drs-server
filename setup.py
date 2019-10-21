#!/usr/bin/env python

import os
from setuptools import setup

SETUP_DIR = os.path.dirname(__file__)

long_description = ""

# with open("README.pypi.rst") as readmeFile:
#     long_description = readmeFile.read()

setup(name='drs-service',
      version='1.0',
      license='Apache 2.0',
      packages=["drs_service"],
      package_data={'drs_service': ['openapi/data_repository_service.swagger.yaml']},
      include_package_data=True,
      install_requires=[
          'future',
          'connexion >= 2.0.2, < 3',
          'ruamel.yaml >= 0.12.4, <= 0.15.77',
      ],
      entry_points={
          'console_scripts': ["drs-server=drs_service.main:main"]
      },
      extras_require={},
      zip_safe=False,
      platforms=['MacOS X', 'Posix'],
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Software Development :: Libraries :: Python Modules'
        ]
      )

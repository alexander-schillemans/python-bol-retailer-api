from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-bol-retailer-api',         
  packages=['bol', 'bol.models', 'bol.constants', 'bol.cache', 'bol.endpoints'],
  version = '1.1.0',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the bol.com Retailer API (v10)',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@lhs.global',
  url = 'https://github.com/alexanderlhsglobal/python-bol-retailer-api',
  download_url = 'https://github.com/alexanderlhsglobal/python-bol-retailer-api/archive/refs/tags/v1.1.0.tar.gz',
  keywords = ['bol.com', 'api', 'bol', 'wrapper'],
  install_requires=[
          'requests',
          'python-dateutil',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
  ],
)
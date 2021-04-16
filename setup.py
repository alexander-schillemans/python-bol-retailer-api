from distutils.core import setup

setup(
  name = 'bol',         
  packages = ['bol'],
  version = '0.1',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the bol.com Retailer API (v5)',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@lhs.global',
  url = 'https://github.com/alexanderlhsglobal/python-bol-retailer-api',
  download_url = 'https://github.com/alexanderlhsglobal/python-bol-retailer-api/archive/refs/tags/v0.1.tar.gz',
  keywords = ['bol.com', 'api'],
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
  ],
)
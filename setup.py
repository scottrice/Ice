import os
import re
import sys

from distutils.sysconfig import get_python_lib
from pip.req import parse_requirements
from setuptools import setup, find_packages

WINDOWS_SPECIFIC_OPTIONS = dict(
  setup_requires=[
    'py2exe',
  ],
)

MAC_SPECIFIC_OPTIONS = dict(
  setup_requires=[
    'py2app',
  ],
)

LINUX_SPECIFIC_OPTIONS = dict(
)

DATA_FILES = [
  'config.txt',
  'consoles.txt',
  'emulators.txt',
]

EXCLUDE_FROM_PACKAGES = [
]

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt')]

def extra_options(platform):
  if platform.startswith('win'):
    return WINDOWS_SPECIFIC_OPTIONS
  elif platform.startswith('darwin'):
    return MAC_SPECIFIC_OPTIONS
  else:
    return LINUX_SPECIFIC_OPTIONS

setup(
  name='Ice',
  version='0.1.0',
  url='http://scottrice.github.io/Ice',
  author='Scott Rice',
  author_email='meris608@gmail.com',
  description='An application to automatically add ROMs to Steam as playable games',
  long_description=open('README.md').read(),
  license='MIT',
  packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
  include_package_data=True,
  data_files=DATA_FILES,
  app=['ice.py'],
  scripts=['ice.py'],
  console=['ice.py'],
  entry_points={'console_scripts': [
  ]},
  install_requires=requirements,
  extras_require={
    'tests': [
      'mock',
      'nose',
    ],
  },
  zip_safe=False,
  classifiers=[
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
  ],
  argv_emulation=False,

  **extra_options(sys.platform)
)

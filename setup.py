import os
import re
import sys
import uuid

from distutils.sysconfig import get_python_lib
from pip.req import parse_requirements
from setuptools import setup, find_packages

def is_windows(platform):
  return platform.startswith('win')

def is_mac(platform):
  return platform.startswith('darwin')

if "py2exe" in sys.argv:
  import py2exe

WINDOWS_SPECIFIC_OPTIONS = dict(
  argv_emulation=False,
  setup_requires=[
    'py2exe',
  ],
  options = dict(
    py2exe = {
      # TODO: Can we generate this list automatically from requirements.txt?
      "includes": [
        "appdirs",
        "psutil",
      ],
    }
  ),
)

MAC_SPECIFIC_OPTIONS = dict(
  app=[ os.path.join('bin', 'ice.py') ],
  setup_requires = [
    'py2app',
  ],
  options = dict(
    py2app = {
      "argv_emulation": True,
      "iconfile": "icon.icns",
      "includes": [
        "appdirs",
        "psutil",
      ],
    },
  ),
)

LINUX_SPECIFIC_OPTIONS = dict(
)

DATA_FILES = [
  'config.txt',
  'consoles.txt',
  'emulators.txt',
]

EXCLUDE_FROM_PACKAGES = [
  "tests",
  "tests.*",
  "*.tests",
  "*.tests.*",
]

DEPENDENCY_LINKS = [
]

requirements = [str(ir.req) for ir in parse_requirements('requirements.txt', session=uuid.uuid1())]

def extra_options(platform):
  if is_windows(platform):
    return WINDOWS_SPECIFIC_OPTIONS
  elif is_mac(platform):
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
  packages=find_packages('.', exclude=EXCLUDE_FROM_PACKAGES),
  include_package_data=True,
  data_files=DATA_FILES,
  console=[ os.path.join('ice', '__main__.py') ],
  entry_points={'console_scripts': [
  ]},
  dependency_links = DEPENDENCY_LINKS,
  install_requires=requirements,
  test_suite='nose.collector',
  tests_require=[
    'nose',
    'nose-parameterized',
    'mockito',
  ],
  zip_safe=False,
  classifiers=[
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
  ],

  **extra_options(sys.platform)
)

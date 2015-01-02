#!/usr/bin/env python

import os
import subprocess
import sys

relative_root_path = subprocess.check_output(["git", "rev-parse", "--show-cdup"]).strip()
setup_py_path = os.path.join(".", relative_root_path, "setup.py")
sys.exit(subprocess.call(["python", setup_py_path, "test"]))
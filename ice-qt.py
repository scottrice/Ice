#!/usr/bin/env python

# gui
import sys
from ice.gui import qtApp, qtWindow

def main():
    qtWindow.show()
    sys.exit(qtApp.exec_())

if __name__ == "__main__":
    main()
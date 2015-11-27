
import argparse
import subprocess
import sys

def argparser():
  parser = argparse.ArgumentParser(description='Packages a python application with Pyinstaller')
  parser.add_argument('-o', '--out', dest='out', type=str, help='final binary location')
  parser.add_argument('main', help='the entry point of the app')
  return parser

def main(args):
  failure = subprocess.call([g
    'pyinstaller $(location //:Ice) -p `dirname $(location //:Ice)`',
    'pyinstaller',
    args.main,
    '-p',
    '`dirname %s`' % args.main,
  ])
  if failure:
    exit(failure)

  # Symlink

if __name__ == '__main__':
  print sys.argv
  main(argparser().parse_args(sys.argv[1:]))

# encoding: utf-8

import os

import pastebin

import filesystem
import paths
import settings

def debug_log_contents():
  fs = filesystem.RealFilesystem()
  return "\n".join([
    debug_string_for_file(settings.settings_file_path('config.txt', fs)),
    debug_string_for_file(settings.settings_file_path('consoles.txt', fs)),
    debug_string_for_file(settings.settings_file_path('emulators.txt', fs)),
    debug_string_for_file(paths.log_file_location()),
  ])
  return log_file_contents()

def debug_string_for_file(path):
  template = """\
======= {} ({}) =======

{}\
"""
  return template.format(os.path.basename(path), path, file_contents(path))

def file_contents(path):
  with open(path, 'r') as f:
    return f.read()

def make_paste(contents):
  api = pastebin.PastebinAPI()
  return api.paste(
    '50de643bdfa229b7488a663091fedf59',
    contents,
    paste_name = 'Ice Debug Logs',
    paste_private = 'unlisted',
  )

def paste_debug_logs():
  url = make_paste(debug_log_contents())
  print "You can find your logs at:\n"
  print "\t%s\n" % url
  print "Please include this link in any bug reports."

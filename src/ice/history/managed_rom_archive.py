
import json
import os

class ManagedROMArchive(object):
  def __init__(self, archive_path):
    self.archive_path = archive_path

    self.archive_data = self.load_archive(archive_path)

  def load_archive(self, path):
    if not os.path.exists(path):
      return {}

    with open(path) as archive_file:
      return json.load(archive_file)

  def previous_managed_ids(self, user):
    uid = str(user.id32)
    return self.archive_data[uid] if uid in self.archive_data else []

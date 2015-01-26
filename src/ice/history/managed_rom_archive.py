
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

  def archive_key(self, user):
    return str(user.id32)

  def previous_managed_ids(self, user):
    key = self.archive_key(user)
    return self.archive_data[key] if key in self.archive_data else []

  def set_managed_ids(self, user, managed_ids):
    # `dict` makes a copy of `archive_data` so I can modify it freely
    new_archive_data = dict(self.archive_data)
    # Overwrite the old data
    new_archive_data[self.archive_key(user)] = managed_ids
    # Save the data to disk
    archive_json = json.dumps(new_archive_data)
    with open(self.archive_path, "w+") as f:
      f.write(archive_json)
    # At this point if an exception wasnt thrown then we know the data
    # save successfully, so overwrite our local data with what we just saved
    self.archive_data = new_archive_data

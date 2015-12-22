
import json
import os

class ManagedROMArchive(object):
  def __init__(self, archive_path):
    self.archive_path = archive_path

    self.archive = self.load_archive(archive_path)

  def load_archive(self, path):
    if not os.path.exists(path):
      return None

    with open(path) as archive_file:
      return json.load(archive_file)

  def archive_key(self, user):
    return str(user.user_id)

  def previous_managed_ids(self, user):
    if self.archive is None:
      return None

    key = self.archive_key(user)
    return self.archive[key] if key in self.archive else []

  def set_managed_ids(self, user, managed_ids):
    # `dict` makes a copy of `archive` so I can modify it freely
    new_archive = dict(self.archive) if self.archive else {}
    # Overwrite the old data
    new_archive[self.archive_key(user)] = managed_ids
    # Save the data to disk
    archive_json = json.dumps(new_archive)
    with open(self.archive_path, "w+") as f:
      f.write(archive_json)
    # At this point if an exception wasnt thrown then we know the data
    # save successfully, so overwrite our local data with what we just saved
    self.archive = new_archive

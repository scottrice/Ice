# encoding: utf-8

import os
import shutil

import paths

VALID_EXTENSIONS = [
    '.png',
    '.jpg',
    '.jpeg',
    '.tga',
]

VALID_EXTENSIONS_WITHOUT_DOT = map(lambda ext: ext[1:], VALID_EXTENSIONS)


def is_valid_extension(extension):
    """Returns True is `extension` is a valid image extension to be used with
    custom Steam grid images. There are only 4 such extensions - `.png`, `.jpg`,
    `.jpeg`, and `.tga`.

    This function will return true even if the parameter `expression` does not
    include the leading '.'"""
    return extension in VALID_EXTENSIONS or \
           extension in VALID_EXTENSIONS_WITHOUT_DOT


def _valid_custom_image_paths(user_context, app_id):
    parent_dir = paths.custom_images_directory(user_context)
    possible_filenames = map(lambda ext: str(app_id) + ext, VALID_EXTENSIONS)
    return map(lambda f: os.path.join(parent_dir, f), possible_filenames)


def has_custom_image(user_context, app_id):
    """Returns True if there exists a custom image for app_id."""
    possible_paths = _valid_custom_image_paths(user_context, app_id)
    return any(map(os.path.exists, possible_paths))


def get_custom_image(user_context, app_id):
    """Returns the custom image associated with a given app. If there are
    multiple candidate images on disk, one is chosen arbitrarily."""
    possible_paths = _valid_custom_image_paths(user_context, app_id)
    existing_images = filter(os.path.exists, possible_paths)
    if len(existing_images) > 0:
        return existing_images[0]


def set_custom_image(user_context, app_id, image_path):
    """Sets the custom image for `app_id` to be the image located at
    `image_path`. If there already exists a custom image for `app_id` it will
    be deleted. Returns True is setting the image was successful."""
    if image_path is None:
        return False

    if not os.path.exists(image_path):
        return False

    (root, ext) = os.path.splitext(image_path)
    if not is_valid_extension(ext):
        # TODO: Maybe log that this happened?
        return False
    # If we don't remove the old image then theres no guarantee that Steam will
    # show our new image when it launches.
    if has_custom_image(user_context, app_id):
        img = get_custom_image(user_context, app_id)
        assert (img is not None)
        os.remove(img)

    # Set the new image
    parent_dir = paths.custom_images_directory(user_context)
    new_path = os.path.join(parent_dir, app_id + ext)
    shutil.copyfile(image_path, new_path)
    return True
import magic


def get_mimetype(file):
    """ Uses python-magic to read mimetype from bytes.\n
    Will return image/png or image/jpeg if file is jpg or png """
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(initial_pos)
    return mime_type


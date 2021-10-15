import magic
from PIL import Image


def get_mimetype(file):
    """ Uses python-magic to read mimetype from bytes.\n
    Will return image/png or image/jpeg if file is jpg or png """
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(initial_pos)
    return mime_type



def resize_crop_image(file, square_width):
    """ Resizes a square image and crops an unsquared image
    (if for some reason javascript has been disabled in the
    browser and user managed to upload anyway) \n\n
    Returns PIL Image """

    im = Image.open(file)
    width, height = im.size   # Get dimensions
    original_format = im.format
    desired_width = square_width
    desired_height = square_width

    # Resize a square
    if width == height:
        if width > desired_width:
            im = im.resize((desired_height, desired_width))

    # Crop a rectangle:
    else:
        if width > desired_width or height > desired_height:

            if width < desired_width:
                desired_width = width
            if height < desired_height:
                desired_height = height

            left = (width - desired_width)/2
            top = (height - desired_height)/2
            right = (width + desired_width)/2
            bottom = (height + desired_height)/2

            # Crop the center of the image
            im = im.crop((left, top, right, bottom))

    im.format = original_format

    return im


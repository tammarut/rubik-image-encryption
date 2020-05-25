from PIL import Image


def resize_img(filename):
    im = Image.open("./input/" + filename)
    new_size = im.resize((64, 64))

    new_size.save("./input/" + filename)
    return new_size

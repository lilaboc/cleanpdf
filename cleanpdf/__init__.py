import sys
import pathlib
import os
from typing import List

from PIL import ImageGrab
from pdf2image import convert_from_path


def process(filename):
    try:
        pages = convert_from_path(filename)
        pages = [page.convert("L").point(lambda p: 255 if p > 230 else p) for page in pages]
        path = pathlib.Path(filename)
        path = path.with_stem(path.stem + "_cleaned")
        pages[0].save(
            path, "PDF", resolution=100.0, save_all=True, append_images=pages[1:]
        )
        for i in [filename, path]:
            os.system('start "{}"'.format(i))
    except Exception as exp:
        print(exp)
        input()


def main():
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        im = ImageGrab.grabclipboard()
        if isinstance(im, List) and isinstance(im[0], str) and os.path.exists(im[0]):
            process(im[0])


if __name__ == '__main__':
    main()
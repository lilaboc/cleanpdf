import sys
import pathlib
import os
from typing import List

import numpy as np
from PIL import ImageGrab
from PIL import Image
from pdf2image import convert_from_path
from glob import glob


# https://zhuanlan.zhihu.com/p/444684653
def otsu(page):
    img = np.array(page)
    h, w = img.shape[:2]
    threshold_t = 0
    max_g = 0
    for t in range(255):
        print(t)
        front = img[img < t]
        back = img[img >= t]
        front_p = len(front) / (h * w)
        back_p = len(back) / (h * w)
        front_mean = np.mean(front) if len(front) > 0 else 0.
        back_mean = np.mean(back) if len(back) > 0 else 0.
        g = front_p * back_p * ((front_mean - back_mean) ** 2)
        if g > max_g:
            max_g = g
            threshold_t = t
    print('thredshold is {}'.format(threshold_t))
    return threshold_t


def process(filename):
    if filename.endswith('.pdf'):
        process_pdf(filename)
    else:
        process_image(filename)


def process_image(filename):
    img = Image.open(filename)
    threshold = otsu(img.convert("L"))
    img = img.point(lambda p: 255 if p > threshold else p)
    path = pathlib.Path(filename)
    path = path.with_stem(path.stem + "_cleaned")
    img.save(path, img.format)
    os.system('start "" "{}"'.format(path))


def process_pdf(filename):
    try:
        pages = convert_from_path(filename)
        # pages = [page.convert("L").point(lambda p: 255 if p > 230 else p) for page in pages]
        result = []
        for page in pages:
            page = page.convert("L")
            threshold = otsu(page)
            page = page.point(lambda p: 255 if p > threshold else p)
            result.append(page)
        path = pathlib.Path(filename)
        path = path.with_stem(path.stem + "_cleaned")
        result[0].save(
            path, "PDF", resolution=100.0, save_all=True, append_images=result[1:]
        )
        for i in [filename, path]:
            os.system('start "" "{}"'.format(i))
    except Exception as exp:
        print(exp)
        input()


def combine():
    if len(sys.argv) > 2:
        pages = []
        for i in sys.argv[1:-1]:
            for filename in glob(i):
                if filename.endswith('.pdf'):
                    pages.extend(convert_from_path(filename))
                else:
                    pages.extend([Image.open(filename)])
        pages[0].save(
            sys.argv[-1], "PDF", resolution=100.0, save_all=True, append_images=pages[1:]
        )






def main():
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            for o in glob(i):
                process(o)
    else:
        im = ImageGrab.grabclipboard()
        if isinstance(im, List) and isinstance(im[0], str) and os.path.exists(im[0]):
            for i in im:
                process(i)


if __name__ == '__main__':
    main()
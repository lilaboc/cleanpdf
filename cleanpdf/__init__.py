import sys
import pathlib
import os
from typing import List

import numpy as np
from PIL import ImageGrab
from pdf2image import convert_from_path


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
            pages.extend(convert_from_path(i))
        pages[0].save(
            sys.argv[-1], "PDF", resolution=100.0, save_all=True, append_images=pages[1:]
        )






def main():
    if len(sys.argv) > 1:
        process(sys.argv[1])
    else:
        im = ImageGrab.grabclipboard()
        if isinstance(im, List) and isinstance(im[0], str) and os.path.exists(im[0]):
            process(im[0])


if __name__ == '__main__':
    main()
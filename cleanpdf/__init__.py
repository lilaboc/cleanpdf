import multiprocessing
import sys
import pathlib
import os
import time
from functools import partial
from typing import List

import numpy as np
from PIL import ImageGrab
from PIL import Image
from pdf2image import convert_from_path
from glob import glob


def find_g(img, t):
    h, w = img.shape[:2]
    front = img[img < t]
    back = img[img >= t]
    front_p = len(front) / (h * w)
    back_p = len(back) / (h * w)
    front_mean = np.mean(front) if len(front) > 0 else 0.0
    back_mean = np.mean(back) if len(back) > 0 else 0.0
    return front_p * back_p * ((front_mean - back_mean) ** 2)


# 优化版本：使用直方图预计算，复杂度从 O(256*H*W) 降到 O(H*W + 256)
def otsu(page):
    img = np.array(page)
    
    # 计算直方图
    hist, _ = np.histogram(img.flatten(), bins=256, range=[0, 256])
    
    total_pixels = img.size
    sum_total = np.sum(np.arange(256) * hist)
    sum_background = 0
    weight_background = 0
    
    max_g = 0
    threshold_t = 0
    
    for t in range(256):
        weight_background += hist[t]
        if weight_background == 0:
            continue
            
        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break
            
        sum_background += t * hist[t]
        
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        
        # 类间方差
        g = weight_background * weight_foreground * ((mean_background - mean_foreground) ** 2)
        
        if g > max_g:
            max_g = g
            threshold_t = t
    
    return threshold_t


# multiprocess version (慢版本，仅作参考)
def otsu_multiprocess(page):
    img = np.array(page)
    threshold_t = 0
    max_g = 0
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    max_g = 0
    for t, g in zip(range(255), pool.map(partial(find_g, img), range(255))):
        if g > max_g:
            max_g = g
            threshold_t = t
    # print('thredshold is {}'.format(threshold_t))
    return threshold_t



# https://zhuanlan.zhihu.com/p/444684653
# single thread version (慢版本，仅作参考)
def otsu_single(page):
    img = np.array(page)
    h, w = img.shape[:2]
    threshold_t = 0
    max_g = 0
    for t in range(255):
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
    # print('thredshold is {}'.format(threshold_t))
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
    start = time.time()
    if len(sys.argv) > 1:
        for i in sys.argv[1:]:
            for o in glob(i):
                process(o)
    else:
        im = ImageGrab.grabclipboard()
        if isinstance(im, List) and isinstance(im[0], str) and os.path.exists(im[0]):
            for i in im:
                process(i)
    print(time.time() - start)


if __name__ == '__main__':
    main()
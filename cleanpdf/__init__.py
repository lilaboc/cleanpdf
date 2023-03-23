import sys
import pathlib
import os
from pdf2image import convert_from_path


def main():
    if len(sys.argv) > 1:
        pages = convert_from_path(sys.argv[1])
        pages = [page.convert("L").point(lambda p: 255 if p > 230 else p) for page in pages]
        path = pathlib.Path(sys.argv[1])
        path = path.with_stem(path.stem + "_cleaned")
        pages[0].save(
            path, "PDF", resolution=100.0, save_all=True, append_images=pages[1:]
        )
        for i in [sys.argv[1], path]:
            os.system('start {}'.format(i))


if __name__ == '__main__':
    main()
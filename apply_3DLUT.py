from __future__ import print_function
from __future__ import division

from PIL import Image
import numpy as np
import argparse
import os
import glob
from scipy.interpolate import RegularGridInterpolator


def parser():
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('img_path', type=str,
                        help='path to image')
    parser.add_argument('lut_path',  type=str,
                        help='path to 3DLUT')
    parser.add_argument('--save_name',  type=str, default=None,
                        help='save name')
    parser.add_argument('--lut_size',  type=int, default=64,
                        help='lut size (default 64)')
    parser.add_argument('--batch', action='store_true',
                        help='apply batch (default False)')
    parser.add_argument('--method',  type=str, default=('linear'), choices=['linear', 'nearest'],
                        help='interpolation methods (defualt linear')
    args = parser.parse_args()
    return args


def load_lut(path):
    lut = np.zeros((LUT_SIZE**3, 3))
    with open(path, 'r') as f:
        for num, l in enumerate(f.readlines()[-LUT_SIZE**3:]):
            l = np.array(l.strip().split(' ')).astype(np.float32)
            lut[num] = l
    return lut


if __name__ == "__main__":
    args = parser()
    LUT_SIZE = args.lut_size

    print('Loading 3DLUT')
    lut = load_lut(args.lut_path)

    x = np.arange(0, 64)
    interpolation_func = RegularGridInterpolator(
        (x, x, x), lut.reshape(64, 64, 64, 3), method=args.method)

    if args.batch:
        img_paths = glob.glob(args.img_path+'*')
    else:
        img_paths = [args.img_path]

    extentions = ['.png', '.jpg']
    for num, path in enumerate(img_paths):
        print('\r{}/{}'.format(num+1, len(img_paths)), end='')
        if not True in [e in path for e in extentions]:
            continue
        if '_lut' in path:
            continue

        if args.save_name is None:
            f_name, ext = os.path.splitext(args.img_path)
            save_name = ''.join([f_name, '_lut', ext])
        else:
            save_name = args.save_name
        if os.path.exists(save_name):
            print('\nFile already exists: {}'.format(save_name))
            print('Skipping...')
            continue

        img = np.array(Image.open(path))[:, :, ::-1]
        new_image = np.round(interpolation_func((img/255.*63)))
        new_image *= 255
        new_image_pil = Image.fromarray(new_image.astype(np.uint8))

        new_image_pil.save(save_name)
    print('')

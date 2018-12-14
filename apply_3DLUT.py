from __future__ import print_function
from __future__ import division

from PIL import Image
import numpy as np
import argparse
import os
import glob


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
    args = parser.parse_args()
    return args


def load_lut(path):
    lut = np.zeros((LUT_SIZE**3, 3))
    with open(path, 'r') as f:
        for num, l in enumerate(f.readlines()[-LUT_SIZE**3:]):
            l = np.array(l.strip().split(' ')).astype(np.float32)
            lut[num] = l
    return lut


def apply_lut(img, lut):
    h, w = img.shape[:2]
    idx = np.round((img/255.)*(LUT_SIZE-1)).astype(np.int32)
    idx *= np.array([1, LUT_SIZE, LUT_SIZE**2])
    idx = idx.sum(2).reshape(-1)
    return (lut[idx].reshape(h, w, 3)*255).astype(np.uint8)


if __name__ == "__main__":
    args = parser()
    LUT_SIZE = args.lut_size

    print('Loading 3DLUT')
    lut = load_lut(args.lut_path)

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
            continue

        img = np.array(Image.open(path))
        new_image = apply_lut(img, lut)
        new_image_pil = Image.fromarray(new_image)

        new_image_pil.save(save_name)
    print('')

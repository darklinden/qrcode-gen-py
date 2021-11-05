#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys

import qrcode
from PIL import Image


def clip_img(img, clip_inset):
    x = img.size[0]
    y = img.size[1]

    dx = x - clip_inset['left'] - clip_inset['right']
    dy = y - clip_inset['top'] - clip_inset['bottom']

    new_img = Image.new('RGBA', (dx, dy), (0, 0, 0, 0))
    new_img.paste(img, (-clip_inset['left'], -clip_inset['top']))
    return new_img


def resize_img(img, des_rect):
    x = des_rect['width']
    y = des_rect['height']

    new_img = img.resize((x, y), Image.BILINEAR)
    return new_img


def add_img(bg_img, img, des_rect):
    new_img = bg_img
    new_img.paste(img, (des_rect['x'], des_rect['y']))
    return new_img


def main():
    _path = ""

    if len(sys.argv) > 1:
        _path = sys.argv[1]

    if len(_path) == 0:
        print('need path')
        return

    config_path = os.path.join(_path, 'config.json')
    with open(config_path, 'r') as fp:
        config = json.load(fp)

    img = qrcode.make(config['url'])
    with open('qrcode.png', 'wb') as f:
        img.save(f)

    img = clip_img(img, config['qrcode-clip-inset'])

    with open('qrcode-cliped.png', 'wb') as f:
        img.save(f)

    img = resize_img(img, config['qrcode-des-rect'])

    with open('qrcode-cliped-scaled.png', 'wb') as f:
        img.save(f)

    # work
    for root, dirs, files in os.walk(_path):
        sub_files = os.listdir(root)
        for fn in sub_files:
            file_path = root + "/" + fn
            if os.path.isfile(file_path):
                if fn.lower().endswith(".qr.png"):
                    continue

                if fn.lower().endswith(".png") or fn.lower().endswith(".jpg") or fn.lower().endswith(
                        ".gif") or fn.lower().endswith(".bmp") or fn.lower().endswith(".jpeg"):
                    try:
                        bg_img = Image.open(file_path)
                    except:
                        print("file [" + file_path + "] is not valid image, skipped.")
                        continue

                    qr_path = file_path + '.qr.png'
                    qr_img = add_img(bg_img, img, config['qrcode-des-rect'])
                    with open(qr_path, 'wb') as f:
                        qr_img.save(f)


if __name__ == "__main__":
    main()

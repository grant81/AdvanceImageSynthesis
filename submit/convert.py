#!/usr/bin/env python

import sys
import numpy as np
import OpenEXR
import Imath
import math
from PIL import Image
import argparse


def convert_exr(input_file, output_file, filetype='PNG'):
    """Convert OpenEXR to PNG/JPG file."""

    # Read OpenEXR file
    src = OpenEXR.InputFile(input_file)
    pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)
    dw = src.header()['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # Convert linear to sRGB (gamma correction)
    rgb = [np.frombuffer(src.channel(c, pixel_type), dtype=np.float32) for c in 'RGB']
    for i in range(3):
        rgb[i] = np.where(rgb[i] <= 0.0031308,
                (rgb[i] * 12.92) * 255.,
                (1.055 * (rgb[i] ** (1. / 2.4)) - 0.055) * 255.)

    # Write to file
    rgb8 = [Image.frombytes('F', size, c.tostring()).convert('L') for c in rgb]
    Image.merge('RGB', rgb8).save(output_file, filetype, quality=100)


def gamma_correct(x):
    """Gamma correction (unscaled)."""

    if x <= 0.0031308:
        return x * 12.92
    else:
        return 1.055 * (value ** (1. / 2.4)) - 0.055


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='EXR to PNG/JPG converter')
    parser.add_argument('input', help='input filename', type=str)
    parser.add_argument('output', help='output filename (with desired format)', type=str)
    args = parser.parse_args()

    # Check input format
    if not args.input.lower().endswith('.exr'):
        raise ValueError('Source file must be an OpenEXR file.')

    # Check output format
    if args.output.lower().endswith('.png'):
        args.filetype = 'PNG'
    elif args.output.lower().endswith('.jpg') or args.output.lower().endswith('.jpeg'):
        args.filetype = 'JPEG'
    else:
        raise ValueError('PNG and JPG formats supported only.')

    # Convert
    convert_exr(args.input, args.output, args.filetype)

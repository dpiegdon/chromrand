#!/usr/bin/python3

import argparse
import numpy
import os
import random
import skimage.io


def get_colors(image):
    """ return a set of used colors (r,g,b) in @image """
    width, height, depth = image.shape
    x = image.reshape((width*height, depth))
    colors = {(c[0], c[1], c[2]) for c in numpy.unique(x, axis=0)}
    return colors


def randomize_chroma(color, jitter=10):
    """ given a @color return another color with similar brightness but
    different chroma, with an allowed @jitter in brightness of """
    brightness = sum(color)
    lower = brightness - jitter//2
    if lower < 0:
        lower = 0
    upper = brightness + jitter//2
    if upper > 255*3:
        upper = 255*3

    targetbrightness = random.randrange(lower, upper+1)

    c = [random.random() for _ in range(3)]
    d = tuple((int(x/sum(c)*targetbrightness) for x in c))
    return d


def randomize_image_chroma(image):
    """ return copy of @image with chroma-randomized palette """
    colors = get_colors(image)
    colormap = {c: randomize_chroma(c) for c in colors}

    copy = numpy.copy(image)
    width, height, depth = copy.shape
    strip = copy.reshape((width*height, depth))
    for i in range(len(strip)):
        c = colormap[(strip[i][0], strip[i][1], strip[i][2])]
        strip[i][0], strip[i][1], strip[i][2] = c
    return copy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Randomize chroma of "
                                                  + "image palette"))
    parser.add_argument("--count", "-c", type=int, required=True,
                        help="number of images to generate")
    parser.add_argument("--output", "-o", type=str, default="out",
                        help="output file prefix")
    parser.add_argument("INPUT", type=str,
                        help="input file")
    args = parser.parse_args()

    image = skimage.io.imread(args.INPUT)
    for i in range(args.count):
        outname = f"{args.output}{i}.png"
        if not os.path.exists(outname):
            print(outname)
            skimage.io.imsave(outname, randomize_image_chroma(image))
        else:
            print(f"skipping existing {outname}")

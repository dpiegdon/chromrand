#!/usr/bin/python3

import argparse
import numpy
import os
import random
import skimage.io


def palette(image):
    """ return a set of used colors (r,g,b) in @image """
    width, height, depth = image.shape
    strip = image.reshape((width*height, depth))
    return {(c[0], c[1], c[2]) for c in numpy.unique(strip, axis=0)}


def randomize_chroma(color, jitter=10):
    """ given a @color return another color with similar brightness but
    different chroma, with an allowed @jitter in brightness """
    brightness = sum(color)
    lower_brightness = max(brightness - jitter//2, 3*0)
    upper_brightness = min(brightness + jitter//2, 3*255)
    target_brightness = random.randrange(lower_brightness, upper_brightness+1)

    c = [random.random() for _ in range(3)]
    d = tuple((int(x/sum(c)*target_brightness) for x in c))
    return d


def randomize_image_chroma(image):
    """ return copy of @image with chroma-randomized palette """
    colormap = {c: randomize_chroma(c) for c in palette(image)}

    copy = numpy.copy(image)
    width, height, depth = copy.shape
    strip = copy.reshape((width*height, depth))
    for pixel in strip:
        pixel[0:3] = colormap[tuple(pixel[0:3])]
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

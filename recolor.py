#!/usr/bin/python3

import argparse
import numpy
import os
import random
import skimage.io


def randomize_chroma(brightness, jitter=15):
    """ given a @brightness return a random color with similar brightness
    up to a certain @jitter """
    lower_brightness = max(brightness - jitter//2, 3*0)
    upper_brightness = min(brightness + jitter//2, 3*255)
    target_brightness = random.randrange(lower_brightness, upper_brightness+1)

    c = numpy.random.rand(3)
    c = c / sum(c) * target_brightness
    return c.astype(int)


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
    width, height, depth = image.shape

    # we only care about r/g/b color, so use a one-dimensional view into image
    strip = image.reshape((width*height, depth))[:, 0:3]
    palette = numpy.unique(strip, axis=0)

    # split image into regions of same color and remember their brightness
    brightness_regions = [(numpy.all(strip == c, axis=1), sum(c))
                          for c in palette]

    for i in range(args.count):
        outname = f"{args.output}{i}.png"
        if not os.path.exists(outname):
            print(outname)
            for region, brightness in brightness_regions:
                strip[region] = randomize_chroma(brightness)
            skimage.io.imsave(outname, image)
        else:
            print(f"skipping existing {outname}")

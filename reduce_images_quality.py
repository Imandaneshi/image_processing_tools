import argparse
import os
import sys
import time
from multiprocessing import Process, Value
from pathlib import Path

from PIL import Image, ExifTags

parser = argparse.ArgumentParser(description="copies all the images inside the input_dir and pastes them"
                                             " into output_dir while reducing their qualities")
parser.add_argument("input_dir", help="Input folder")
parser.add_argument("output_dir", help="Destination folder")
parser.add_argument("--quality", help="Image quality from 50 to 100",
                    type=lambda x: int(x) if 50 <= int(x) <= 100 else 75, required=False, default=75),
parser.add_argument("--max_width", help="Maximum width for each image from 600 to 1500",
                    type=lambda x: int(x) if 600 <= int(x) <= 1500 else 800, required=False, default=800),
parser.add_argument("--max_height", help="Maximum height for each image from 600 to 1500",
                    type=lambda x: int(x) if 600 <= int(x) <= 1500 else 800, required=False, default=800),
parser.add_argument("--processors", help="Number of processors to be used", required=False, default=2,
                    type=lambda x: int(x) if 2 <= int(x) <= 30 else 2)
args = parser.parse_args()


def get_image_size(max_width, max_height, width, height):
    # Function to calculate image size
    if width > max_width or height > max_height:
        if width > height:
            reduce_factor = max_width / float(width)
            reduced_width = int(width * reduce_factor)
            reduced_height = int(height * reduce_factor)
        else:
            reduce_factor = max_height / float(height)
            reduced_width = int(width * reduce_factor)
            reduced_height = int(height * reduce_factor)
        return reduced_width, reduced_height
    else:
        return width, height


def reduce_image_quality(name):
    img = Image.open(Path(args.input_dir).joinpath(name))
    if hasattr(img, '_getexif'):  # only present in JPEGs
        try: # try to rotate image if rotation is wrong
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(img._getexif().items())
            if exif[orientation] == 3:
                img = img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img = img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img = img.rotate(90, expand=True)
        except:
            pass
    new_size = get_image_size(args.max_width, args.max_height, img.size[0], img.size[1])
    new_photo = img.resize(new_size, Image.ANTIALIAS)
    new_photo.save(Path(args.output_dir).joinpath(name), "JPEG", quality=args.quality, optimize=True)


def process_images(images, counter):
    for image in images:
        reduce_image_quality(image)
        with counter.get_lock():
            counter.value += 1


if __name__ == "__main__":
    start_time = time.time()
    all_images = []
    shared_counter = Value('i', lock=True)
    for p in os.walk(args.input_dir):
        for l in p[2]:
            if l.endswith("jpg") or l.endswith("jpeg") or l.endswith("png"):
                all_images.append(l)
    remaining = len(all_images) % args.processors
    count = int(len(all_images) / args.processors)
    for k in range(args.processors):
        k += 1
        x1 = (k - 1) * count
        x2 = k * count
        _images = []
        if k + 1 == args.processors and remaining:
            for w in all_images[0 if x1 == 1 else x1:]:
                _images.append(w)
        else:
            for w in all_images[0 if x1 == 1 else x1:x2]:
                _images.append(w)
        Process(target=process_images, args=(_images, shared_counter)).start()
    while shared_counter.value != len(all_images):
        sys.stdout.write('\r' + str(shared_counter.value) + "/" + str(len(all_images)) + " | " + str(
            int((int(shared_counter.value) * 100) / len(all_images))) + "% ")
    sys.stdout.write("\rReduced quality of " + str(len(all_images)) +
                     " images in " + str(time.time() - start_time) + " seconds")

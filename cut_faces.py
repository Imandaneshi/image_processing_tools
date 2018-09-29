import argparse
import os
import random
import string
import sys
import time
from multiprocessing import Process, Value
from pathlib import Path

import face_recognition
from PIL import Image, ExifTags

parser = argparse.ArgumentParser(description="Cuts all the faces on images and saves them in output_dir")
parser.add_argument("input_dir", help="Input folder")
parser.add_argument("output_dir", help="Destination folder")
parser.add_argument("--upsample", help="How many times to upsample the image looking for faces."
                                       " Higher numbers find smaller faces.",
                    type=lambda x: int(x) if 1 <= int(x) <= 5 else 1, required=False, default=1),
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


def cut_faces(name, face_counter):
    image = face_recognition.load_image_file(Path(args.input_dir).joinpath(name))
    face_locations = face_recognition.face_locations(image, args.upsample)
    for f in face_locations:
        top, right, bottom, left = f
        face_image = image[top:bottom, left:right]
        cropped_face = Image.fromarray(face_image)
        cropped_face.save(Path(args.output_dir).joinpath(
            ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=10)) + ".jpg"),
            quality=90, optimize=True)
        with face_counter.get_lock():
            face_counter.value += 1


def process_images(images, counter, face_counter):
    for image in images:
        cut_faces(image, face_counter)
        with counter.get_lock():
            counter.value += 1


if __name__ == "__main__":
    start_time = time.time()
    all_images = []
    shared_counter = Value('i', lock=True)
    shared_face_counter = Value('i', lock=True)
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
        Process(target=process_images, args=(_images, shared_counter, shared_face_counter)).start()
    while shared_counter.value != len(all_images):
        sys.stdout.write('\r' + str(shared_counter.value) + "/" + str(len(all_images)) + " | " + str(
            int((int(shared_counter.value) * 100) / len(all_images))) + "% ")
    sys.stdout.write("\rDone cutting " + str(shared_face_counter.value) + " faces from " + str(len(all_images)) +
                     " images in " + str(time.time() - start_time) + " seconds")

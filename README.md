# image_processing_tools
My set of image processing functions and scripts

## reduce_images_quality.py
```text
usage: reduce_images_quality.py [-h] [--quality QUALITY]
                                [--max_width MAX_WIDTH]
                                [--max_height MAX_HEIGHT]
                                [--processors PROCESSORS]
                                input_dir output_dir

Copies all the images inside the input_dir and pastes them into output_dir
while reducing their qualities

positional arguments:
  input_dir             Input folder
  output_dir            Destination folder

optional arguments:
  -h, --help            Show this help message and exit
  --quality QUALITY     Image quality from 50 to 100
  --max_width MAX_WIDTH
                        Maximum width for each image from 600 to 1500
  --max_height MAX_HEIGHT
                        Maximum height for each image from 600 to 1500
  --processors PROCESSORS
                        Number of processors to be used
```

## cut_faces.py
```text
usage: cut_faces.py [-h] [--upsample UPSAMPLE] [--processors PROCESSORS]
                    input_dir output_dir

Cuts all the faces on images and saves them in output_dir

positional arguments:
  input_dir             Input folder
  output_dir            Destination folder

optional arguments:
  -h, --help            show this help message and exit
  --upsample UPSAMPLE   How many times to upsample the image looking for
                        faces. Higher numbers find smaller faces.
  --processors PROCESSORS
                        Number of processors to be used
```

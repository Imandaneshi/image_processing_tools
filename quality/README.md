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

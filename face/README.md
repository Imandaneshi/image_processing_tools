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

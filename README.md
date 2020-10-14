# Hiveopolis Video Analyser

Code pieces to extract pixel change of defined region of interest and ocr text of display.

## custom_ocr.py

Logic to extract text from display. These helps us to connect frames and currently playing frequencies. Open source [tesseract](https://github.com/tesseract-ocr/tesseract).

## custom_roi.py

Simple script to define region of interest.

## read_videos.py

Read video, calculate pixel change over n number of frames. Outputs a `csv` file with frame number, relative pixel change of region of interest and the ocr text of each frame.

## License

Copyright (c) 2020 Hannes Oberreiter, Martin Stefanec

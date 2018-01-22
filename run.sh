#!/bin/bash

# docker build -t booj/listing_xml_parse .
pip install -r requirements.txt
python xml_parser.py --url-file urls.txt --csv-out output.csv

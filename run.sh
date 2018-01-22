#!/bin/bash

# docker build -t booj/listing_xml_parse .

# NOTE: you may need to install with root priveleges. or use virtualenv.
pip install -r requirements.txt
python xml_parser.py --url-file urls.txt --csv-out output.csv --csv-out-dir outputs

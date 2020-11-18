#! /bin/bash
python3 raw_data_processing.py 
python3 preprocessing-labeled.py 1 1830
python3 preprocessing-unlabeled.py 1 9000

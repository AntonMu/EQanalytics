Logos in the Wild dataset

# General remarks
This dataset consists of web images which were crawled via Google 
image search and according logo annotions. It was collected at 
Fraunhofer IOSB in Karlsruhe, Germany. 
For dataset related matters please contact Christian Herrmann: 
christian.herrmann@iosb.fraunhofer.de.


# Structure
Each folder contains the raw Pascal VOC style xml annotation files and a 
urls.txt file containing a list of URLs where the images can be 
downloaded. Each row in the list contains the image ID and the URL
of the image file.

A folder includes all images resulting from the Google image search for 
this brand. Because images can show a large variety of logos beyond the 
keyword search, there are a lot logos of different brands within each 
folder or sometimes even within a single image.
The bounding box name denotes the actual brand for each logo. When 
necessary, separation is made between graphical and textual logos via 
additional specifiers of the brand name (e.g. 'porsche-logo', 
'porsche-text'). Visually different logos of one brand are separated by 
enumeration if distinction by graphical/textual is impossible (e.g. 
'adidas1', 'adidas2'). There are some misspellings and inconsistencies 
with the labels and specifiers in the raw annotation files. We opt not to 
alter the raw files provided by the annotation crew but instead fix the 
issues by the create_clean_dataset.py script (see Scripts section below).

List of cleaned specifiers:
- 'text': pure textual logo
- 'symbol': graphical logo

Additional specifiers in raw annotations:
- 'partial','teilsichtbar': logo is significantly occluded and thus only 
partially visible, this information is only included in the raw annotations
- 'schrift','schriftzug': same as 'text'
- 'logo': same as 'symbol'


# Scripts
To ease processing, the scripts folder contains a Python scripts to 
preprocess the dataset.
create_clean_dataset.py corrects labeling mistakes and can create 
different versions of the dataset:

1.) Clean Pascal VOC dataset structure which is straight-forward readable 
by a lot of object detector frameworks. This is created in all cases:
python create_clean_dataset.py --in ./data --out ./cleaned-data

2.) Cropped logos sorted into seperate brand folders. This addresses 
classification or verification tasks. Parameter: --roi.

3.) Logo classes from FlickrLogos32 can be excluded from 1) and 2) via 
--wofl32. This allows training on Logos in the Wild and testing on 
FlickrLogos32 if brand overlap is undesired, such as for open-set 
evalutation.


# How to get started
1.) Download the images from the provided URLs.
2.) Execute create_clean_dataset.py script.

# Dataset usage
If you use this dataset in your work please cite:

@INPROCEEDINGS{,
author = {T{\"u}zk{\"o}, Andras and Herrmann, Christian and Manger, Daniel 
and J{\"u}rgen Beyerer},
title = {{O}pen {S}et {L}ogo {D}etection and {R}etrieval},
booktitle = {Proceedings of the 13th International Joint Conference on 
Computer Vision, Imaging and Computer Graphics Theory and Applications: 
VISAPP},
year = {2018}}


# Copyright, Licenses and legal information
See license.txt.
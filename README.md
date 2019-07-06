

# EQanalytics: Detection of Vulnerable Buildings

Machine learning project developed at Insight Data Science, 2019 AI session.

## Project description
In August 2018, [**AB-2681 Seismic safety: potentially vulnerable buildings**]([https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180AB2681](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180AB2681)) was passed. This bill requires the state of California to identify all potentially vulnerable buildings before Jan 1, 2021. 

### Soft Story Buildings
One important type of vulnerable buildings are those with soft stories. A [soft story](https://en.wikipedia.org/wiki/Soft_story_building) is classified as a level that is less than 70% as stiff as the floor immediately above it.

In this project, I built an application that uses Google Street View images and computer vision techniques as well as classical machine learning to determine whether a given building address has a soft story. 

### Training
On a high level, the model training consists of four seperate steps:

 1. Obtain Training Images
	 - Download Street View images from all buildings in the [San Francisco soft story property list](https://sfdbi.org/soft-story-properties-list).
 2. Object Segmentation
 
	 2.1 Detect Houses
	- Manually label houses using [VoTT](https://github.com/Microsoft/VoTT).
	- Use transfer learning to train a YOLOv3 detector.
	- Crop and save houses.

    2.2 Detect Openings 
	 - Train a YOLO detector based on the [CMP facade dataset](http://cmp.felk.cvut.cz/~tylecr1/facade/).
	 - Detect all openings in set of cropped out houses.
 4. Compute "softness score" to classify building
	 -  Use K-means clustering to identify number of stories.
	 - Compute quotient of the total width of openings on the second story over the total width of openings on the first story.
### Inference
Model inference consists of four similar steps. After entering an address (or list of addresses), the corresponding street view images will be downloaded. For all images, the housing model first segments and crops one house per address. Then the opening detector labels all openings and creates a csv file with all dimensions and positions of the openings. Finally, the softness score is determined and used to classify the building as "soft", "non_soft" or "undetermined". 

## Repo structure
+ `1_Pre_Processing`: All Preprocessing Tasks
+ `2_Computer_Vision`: Both Image Segmentation Tasks
+ `3_Final_Classification`: Final Classicfication Task
+ `Built`: Scripts to get started, train and evaluate

## Getting Started

#### Requisites
The code uses python 3.6, Keras with Tensorflow backend, and a conda environment to keep everything together. Training was performed on an AWS *p2.xlarge* instance (Tesla K80 GPU with 12GB memory). Inference is faster on a GPU (~5 images per second on the same setup), but also works fine on a modest CPU setup (~0.3 images per second on an AWS *t2.medium* with a 2 VCPUs and 4GB of memory).

#### Installation [Linux or Mac]

##### Clone Repo and Install Requirements
Clone this repo with:
```
git clone https://github.com/AntonMu/eqanalytics
cd eqanalytics/
```

Create Virtual Environment ([Venv](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) needs to be installed on your system). 
```
python3 -m venv env
source env/bin/activate
```
Install required packages:

```
pip3 install -r requirements.txt
```

#### Build Environment For Inference

To hit the ground running, download the pre-trained YOLOv3 model weights (235MB) for the housing detector and the pre-trained YOLOv3 weights (236MB) for the opening detector. 
```
bash build/build_inference.sh
```
#### Build Environment For Training
To re-train the housing detector and/or opening detector follow the following steps. 

##### Re-train Housing Detector
To retrain the housing detector, either download your own street view housing image dataset or use the SF vulnerable buildings data set. Once you have created an image folder, install [VoTT](https://github.com/Microsoft/VoTT) on your local machine and segment houses. Alternatively, use the already segmented dataset. Next, download the default YOLOv3 weights to start transfer learning from.  
```
bash build/build_housing_detector.sh --download_images --download_segments
```
The flag, `download_images` indicates that the SF housing image dataset should be downloaded.  The flag, `download_segments` indicates that the manually labeled dataset with houses segmented should be downloaded.
![VoTT Housing](/VOTT_houses.png)
##### Re-train Opening Detector

To retrain the opening detector, either download the [CMP facade dataset](http://cmp.felk.cvut.cz/~tylecr1/facade/) or provide your own data set of segmented building openings (e.g. by using [VoTT](https://github.com/Microsoft/VoTT)) . Also download the default YOLOv3 weights to start transfer learning from.   
```
bash build/build_opening_detector.sh --download_cmp
```
The flag, `download_cmp` indicates that the [CMP facade dataset](http://cmp.felk.cvut.cz/~tylecr1/facade/) should be downloaded. 
<!-- 
## Usage
The script doing the work is [logohunter.py](src/logohunter.py) in the `src/` directory. It first uses a custom-trained YOLOv3 to find logo candidates in an image, and then looks for matches between the candidates and a user input logo.

Execute it with the `-h` option to see all of the possible command line inputs. A simple test to match 20 sample input
images in the [data/test/sample_in/](data/test/sample_in/) directory to logos in [data/test/test_brands/](data/test/test_brands/) can be executed with:
```
cd src/
python logohunter.py --test
```

Typical ways to run the program involve specifying one input brand and a folder of sample images:
```
python logohunter.py  --image --input_brands ../data/test/test_brands/test_lexus.png \
                              --input_images ../data/test/lexus/ \
                              --output ../data/test/test_lexus --outtxt

python logohunter.py  --image --input_brands ../data/test/test_brands/test_golden_state.jpg  \
                              --input_images ../data/test/goldenstate/  \
                              --output ../data/test/test_gs --outtxt

python logohunter.py  --image --input_images data_test.txt  \
                              --input_brands ../data/test/test_brands/test_lexus.png  \
                              --outtxt --no_save_img
```

In the first two use cases, we test a folder of images for a single brand ([lexus logo](data/test/test_brands/test_lexus.png) or [golden state logo](data/test/test_brands/test_golden_state.jpg)). The input images were downloaded from Google Images for test purposes. Running LogoHunter saves images with bounding box annotations in the folder specified (`test_lexus`, `test_gs`). Because each of these images contains the logo we are looking for, this is a way to estimate the false negative rate (and the recall).

In the third example, we test a text file containing paths to 2590 input images from the LogosInTheWild dataset against a single brand, without saving the annotated images. Because the brand is new to the dataset, this is a way to estimate the false positive rate (and the precision). (**Note:** this will not run out of the box, as you will need to separately download the LogosInTheWild dataset - follow the instructions below to download the dataset).



#### Data
This project uses the [Logos In The Wild dataset](https://www.iosb.fraunhofer.de/servlet/is/78045/) which can be requested via email directly from the authors of the paper, [arXiv:1710.10891](https://arxiv.org/abs/1710.10891). This dataset includes 11,054 images with 32,850 bounding boxes for a total of 871 brands.

See below for LICENSE information of this dataset.

#### Optional: download, process and clean dataset

Follow the directions in [data/](data/README.md) to download the Logos In The Wild dataset.

#### Optional: train object detection model
After the previous step, the `data_train.txt` and `data_test.txt` files have all the info necessary to train the model. We then follow the instructions of the [keras-yolo3](https://github.com/qqwweee/keras-yolo3) repo: first we download pre-trained YOLO weights from the YOLO official website, and then we convert them to the HDF5 format used by keras.
```
cd src/keras_yolo3
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5

cd ../
python train.py
```
Training detail such as paths to train/text files, log directory, number of epochs, learning rates and so on are specified in `src/train.py`. The training is performed in two runs, first with all the layers except the last three frozen, and then with all layers trainable.

On an AWS EC2 p2.xlarge instance, with a Tesla K-80 GPU with 11GB  of GPU memory and 64GB of RAM, training YOLOv3 for logo detection took approximately 10 hours for 50+50 epochs.
 -->

## License

Unless explicitly stated at the top of a file, all code is licensed under the MIT license.

<!-- 
The Logos In The Wild dataset (links to images, bounding box annotations, clean_dataset.py script) is licensed under the CC-by-SA 4.0 license. The images themselves were crawled from Google Images and are property of their respective copyright owners. For legal reasons, raw images other than the ones in `data/test` are not provided: while this project would fall in the "fair use" category, any commercial application would likely need to generate their own dataset.
 -->
The model files for the YOLO weights and the extracted logo features are derivative work based off of the Logos In The Wild dataset, and are therefore also licensed under the CC-by-SA 4.0 license.

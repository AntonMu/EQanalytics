# EQanalytics: Housing Detector
Using the training images downloaded previously (`EQanalytics/Data/Street_View_Images`) we train a detector that can segment houses. 

## Creating a Training Data Set for House Segmentation
To generate our training (and validation) set we use use Microsoft's [VoTT](https://github.com/Microsoft/VoTT) to label training images. 

### Using VoTT
After installing VoTT, connect the local database to a selection of images from the folder `EQanalytics/Data/Street_View_Images` and name the database `Houses`.

#### Settings
Under export settings, as `Provider` chose `Comma Seperated Values (CSV)`. Then hit `Save Export Settings`. Make sure the `Include Images` checkbox is checked.

![VoTT Settings](/2_Computer_Vision/2.1_Housing_Detector/0_Training/Screenshots/VoTT_Export_Settings.png)

#### Labeling
Now start labeling all houses. One class called `house` is enough for this task. I recommend to label at least 300 images. The more the better!

![VoTT Houses](/2_Computer_Vision/2.1_Housing_Detector/0_Training/Screenshots/VoTT_Houses.png)

 Once you are done, export the project. 
 
![VoTT Saving](/2_Computer_Vision/2.1_Housing_Detector/0_Training/Screenshots/VoTT_Save.jpg)

#### Collecting the Result
You should see a folder called `vott-csv-export` which contains all segmented images and a `*.csv` file called `Houses-export.csv`. Copy the content of this folder to `EQanalytics/Data/vott-csv-export`. 

![VoTT Folder](/2_Computer_Vision/2.1_Housing_Detector/0_Training/Screenshots/VoTT_Export.png)

#### Convert to Yolo Format
As a final step, we convert the `VoTT csv` format to the `YOLOv3` format. To do so, run the `Prepare_Houses_for_Yolo.py` script with:

```
python Prepare_Houses_for_Yolo.py
```

If you have completed all previous steps on your local machine but want to train on AWS, use the flag `--AWS` so the file paths are updated correctly. If you are doing all steps on the same machine, no flags are needed. 

## Starting the Training

Before getting started we need to download the pre-trained YOLOv3 weights. To do so, navigate to `EQanalytics/2_Computer_Vision/src/keras_yolo3`. Next, download the weights and convert them to Keras format:

```
wget https://pjreddie.com/media/files/yolov3.weights
python convert.py yolov3.cfg yolov3.weights model_data/yolo.h5
```

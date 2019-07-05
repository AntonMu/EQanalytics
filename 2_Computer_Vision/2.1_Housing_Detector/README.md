

# EQanalytics: Housing Detector
Using the training images downloaded previously (`EQanalytics/Data/Street_View_Images`) we train a detector that can segment houses. 

## Creating a Training Data Set for House Segmentation
To generate our training (and validation) set we use use Microsoft's [VoTT](https://github.com/Microsoft/VoTT) to label training images. 

### Using VoTT
After installing VoTT, connect the local database to a selection of images from the folder `EQanalytics/Data/Street_View_Images` and name the database `Houses`.

#### Settings
Under export settings, as `Provider` chose `Comma Seperated Values (CSV)`. Then hit `Save Export Settings`. Make sure the `Include Images` checkbox is checked.

 ![VoTT Settings](/2_Computer_Vision/2.1_Housing_Detector/VoTT_Export_Settings.png)

#### Labeling
Now start labeling all houses. One class called `house` is enough for this task. I recommend to label at least 300 images. The more the better!
![VoTT Housing](/2_Computer_Vision/2.1_Housing_Detector/VoTT_Houses.png)

 Once you are done, export the project. 
![VoTT Housing](/2_Computer_Vision/2.1_Housing_Detector/VoTT_Save.png)

#### Collecting the Result
You should see a folder called `vott-csv-export` which contains all segmented images and a `*.csv` file called `Houses-export.csv`. Please the content of this folder under `EQanalytics\Data\vott-csv-export`. 
![VoTT Housing](/2_Computer_Vision/2.1_Housing_Detector/VoTT_Export.png)

#### Convert to Yolo Format
As a final step, we convert the `VoTT csv` format to the `YOLOv3` format. 

This step obtains street view images for a provided `*.csv` file of buildings addresses such as the one from the [San Francisco soft story property list](https://sfdbi.org/soft-story-properties-list). Note that the `*.csv` file must contain a `PROPERTY` and `STATUS` column. Entries in the `PROPERTY` column must be of the form `house number` `␣` `street name`.

## Usage
To run the script you first need to obtain a Google Street View Static API key on the [gcp](https://console.cloud.google.com/) website. To start downloading street view images run:
```
python Download_Images.py --G_API_key <your Google API key>
```
To get started on a small test set of 62 buildings run:
```
python Download_Images.py --G_API_key <your Google API key> --test
```
By default, addresses in `eqanalytics/1_Pre_Processing/Locations/SF.csv` are used. Downloaded images will be saved in `EQanalytics/Data/Street_View_Images` and the index file under  `EQanalytics/Data/Street_View_Images/results.csv`. Use the flags `--address_file`, `--result_folder` and `--result_file` to change this behavior. In all cases by provide an absolute path. 

Other possible flags are `--city`, which is set to `SAN FRANCISCO` by default, and `--pitch`, which determines the angle of the street view camera. The default pitch value is set to `10` and `0` would mean a completely horizontal picture.

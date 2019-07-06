
# EQanalytics: Pre-Processing
This step obtains street view images for a provided `*.csv` file of buildings addresses such as the one from the [San Francisco soft story property list](https://sfdbi.org/soft-story-properties-list). Note that the `*.csv` file must contain a `PROPERTY` and `STATUS` column. Entries in the `PROPERTY` column must be of the form `house number␣street name`.

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

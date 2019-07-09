# EQanalytics: Classification
In this final step, we use our opening segmentation results from `EQanalytics/Data/Opening_Detection_Results/Opening_Results.csv` to determine a softness score. To execute the classification run
```
python Classifier.py
```
## Pre-Processing
As a first step, the classifier filters all elements which are not labeled `door`, `window` or `shop`. Then it removes element thats have large overlap and keeps the elements with the bigger area. 
## Level Detection
Next, the classifier uses K-mean clustering to determine the number of stories. To do so, the algorithm looks at the y-coordinates of all segmented objects and finds an ideal fit of clusters. The results of the level detection will be saved to `EQanalytics/Data/Level_Detection_Results`. By using the flag `--no_save_img` the detected level images will not be saved as separate images. 
## Softness Computation
Finally, once all segmented objects are determined, we calculate a quotient of the total width of openings on the second level over the total width of openings on the first level. To avoid double counting only the interval union of all widths are considered. The results, along with their street address, are saved to `EQanalytics/Data/Softness_Scores.csv`. 

| Score x       | Class           
| ------------- |:-------------:
| 0.3 < x <= 0.75      | soft |
| 0.75 < x <= 1.5      | non_soft
| x > 1.5 \| x <= 0.3 | undetermined      |

If the softness score is too high or too low, then there may be some issues with obstructed views and we err on the side of caution and return **undetermined**. Otherwise, if it is less than 75%, we classify the building as **soft** and **non_soft** otherwise.

### That's all!
This completes our vulnerable building detection model. The `Softness_Score.csv` file contains the classification for all images that were processed.
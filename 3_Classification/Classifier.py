#
# SCRIPT TO DETECT HOUSES IN IMAGES AND RETURN A CSV FILE WITH BOUDING BOXES
#

import os
import sys

def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

utils_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'Utils')
sys.path.append(utils_path)
import argparse
# from keras_yolo3.yolo import YOLO
# from PIL import Image
# from timeit import default_timer as timer
# from logos import detect_logo, match_logo
# from similarity import load_brands_compute_cutoffs
# from utils import load_extractor_model, load_features, model_flavor_from_name, parse_input
# import test
# import utils
import pandas as pd
import numpy as np
from Filter_Tools import get_features, remove_overlaps, find_levels, draw_levels, calcuate_softness, get_address
import random

data_folder = os.path.join(get_parent_dir(n=1),'Data')

openings_result_folder = os.path.join(data_folder,'Opening_Detection_Results') 
openings_result_file =  os.path.join(openings_result_folder, 'Opening_Results.csv')
openings_classes = os.path.join(data_folder,'Model_Weights','Openings','data_all_classes.txt')

level_folder =  os.path.join(data_folder,'Level_Detection_Results')

softness_score_file =  os.path.join(data_folder, 'Softness_Scores.csv')


FLAGS = None

if __name__ == '__main__':
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''

    parser.add_argument(
        "--output_file", type=str, default=softness_score_file,
        help = "File to save classification results to. Default value is Data/Softness_Scores.csv."
    )


    parser.add_argument(
        "--input_file", type=str, default=openings_result_file,
        help = "Path to csv file with detected openings and image path references. Default value is Data/Opening_Detection_Results/Opening_Results.csv."
    )

    parser.add_argument(
        "--no_save_img", default=False, action="store_true",
        help = "do not save output images with annotated boxes"
    )

    parser.add_argument(
        "--level_folder", type=str, default=level_folder,
        help = "Output path for level results. Default value is Data/Level_Detection_Results."
    )


    parser.add_argument(
        '--classes', type=str, dest='classes_path', default = openings_classes,
        help='path to YOLO class specifications. Default value is Data/Model_Weights/Openings/data_all_classes.txt.'
    )

    
    parser.add_argument(
        '--postfix', type=str, dest = 'postfix', default = '_levels',
        help='Specify the postfix for images with bounding boxes'
    )

    parser.add_argument(
        '--iou_threshold', type=float, dest = 'iou', default = .75,
        help='Specifies the IoU threshold for which overlapping objects will be merged'
    )

    parser.add_argument(
        '--metric', type=str, dest = 'metric', default = 'x_len',
        help='Specifies the metric to use to calculate softness score. Possible values are "x_len", "y_len", "area".'
    )
    

    FLAGS = parser.parse_args()
    label_dict = pd.read_csv(FLAGS.classes_path,header=None).to_dict()[0]
    opening_df = pd.read_csv(FLAGS.input_file).sort_values('image')

    #Now calculate features such as the width of windows and doors. Also filter everythin that is not a door, window, blind or shop
    opening_df = get_features(opening_df,label_dict,label_names = ['door', 'window', 'shop'])

    #Next remove all objects that have more than 75% IoU (and keep the bigger one)

    unique_opening_df = remove_overlaps(opening_df,iou_threshold=FLAGS.iou)

    #Next we use K-means clustering to find the number of stories

    level_df = find_levels(unique_opening_df,threshold=2e-3)

    if not FLAGS.no_save_img:
	    if not os.path.exists(FLAGS.level_folder):
	        os.makedirs(FLAGS.level_folder)
	    draw_levels(level_df,FLAGS.level_folder)

    #Finally we compute the softness score based on the width of the openings

    softness_df = calcuate_softness(level_df,metric=FLAGS.metric)

    get_address(softness_df).to_csv(FLAGS.output_file,index=False)

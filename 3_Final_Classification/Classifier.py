#
# SCRIPT TO DETECT HOUSES IN IMAGES AND RETURN A CSV FILE WITH BOUDING BOXES
#

import os
import sys

def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.getcwd()
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path

utils_path = os.path.join(os.getcwd(),'Utils')
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

model_folder =  os.path.join(data_folder,'Model_Weights')
openings_classes = os.path.join(model_folder,'Openings','data_all_classes.txt')

level_folder =  os.path.join(data_folder,'Level_Detection_Results')

softness_score_file =  os.path.join(data_folder, 'Softness_Scores.csv')


FLAGS = None

if __name__ == '__main__':
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''

    # parser.add_argument(
    #     "--input_images", type=str, default=image_folder,
    #     help = "Path to image directory. All subdirectories will be included."
    # )

    # parser.add_argument(
    #     '--test', default=False, action="store_true",
    #     help='Test routine on 10 images in /Data/Street_View_Images'
    # )

    # parser.add_argument(
    #     "--output", type=str, default=houses_result_folder,
    #     help = "Output path for detection results."
    # )

    # parser.add_argument(
    #     "--detection_mode", type=str, default='houses',
    #     help = "If set to openings, use the pre-trained weights for openings. Otherwise use the pre-trained weights for houses. This overrides all other settings."
    # )

    # parser.add_argument(
    #     "--no_save_img", default=False, action="store_true",
    #     help = "do not save output images with annotated boxes"
    # )

    # parser.add_argument(
    #     '--yolo_model', type=str, dest='model_path', default = houses_weights,
    #     help='Use your own pre-trained weights. This option does NOT overide the --model_type flag setting.'
    # )

    # parser.add_argument(
    #     '--anchors', type=str, dest='anchors_path', default = 'src/keras_yolo3/model_data/yolo_anchors.txt',
    #     help='path to YOLO anchors'
    # )

    # parser.add_argument(
    #     '--classes', type=str, dest='classes_path', default = houses_classes,
    #     help='path to YOLO class specifications'
    # )

    # parser.add_argument(
    #     '--gpu_num', type=int, default = 1,
    #     help='Number of GPU to use'
    # )

    # parser.add_argument(
    #     '--confidence', type=float, dest = 'score', default = 0.1,
    #     help='YOLO object confidence threshold above which to show predictions'
    # )
    
    # parser.add_argument(
    #     '--box_file', type=str, dest = 'box', default = houses_result_file,
    #     help='Specify the destination to save bounding boxes'
    # )
    
    # parser.add_argument(
    #     '--postfix', type=str, dest = 'postfix', default = '_house',
    #     help='Specify the postfix for images with bounding boxes'
    # )
    

    FLAGS = parser.parse_args()
    label_dict = pd.read_csv(openings_classes,header=None).to_dict()[0]
    opening_df = pd.read_csv(openings_result_file).sort_values('image')

    #Now calculate features such as the width of windows and doors. Also filter everythin that is not a door, window, blind or shop
    opening_df = get_features(opening_df,label_dict,label_names = ['door', 'window', 'blind', 'shop'])

    #Next remove all objects that have more than 75% IoU (and keep the bigger one)

    unique_opening_df = remove_overlaps(opening_df,iou_threshold=.75)

    #Next we use K-means clustering to find the number of stories

    level_df = find_levels(unique_opening_df,threshold=2e-3)

    if not os.path.exists(level_folder):
        os.makedirs(level_folder)
    draw_levels(level_df,level_folder)

    #Finally we compute the softness score based on the width of the openings

    softness_df = calcuate_softness(level_df,metric='x_len')

    get_address(softness_df).to_csv(softness_score_file,index=False)

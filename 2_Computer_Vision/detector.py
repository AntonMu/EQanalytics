#
# SCRIPT TO DETECT HOUSES IN IMAGES AND RETURN A CSV FILE WITH BOUDING BOXES
#

import os
import sys

#Check the postifx!!!!!!!!!!!!!!!!!! in the csv file

def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.getcwd()
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path
src_path = os.path.join(os.getcwd(),'src')
sys.path.append(src_path)

utils_path = os.path.join(os.getcwd(),'Utils')
sys.path.append(utils_path)
import argparse
from keras_yolo3.yolo import YOLO
from PIL import Image
from timeit import default_timer as timer
from logos import detect_logo #, match_logo
# from similarity import load_brands_compute_cutoffs
from utils import load_extractor_model, load_features, parse_input
# from utils import load_extractor_model, load_features, model_flavor_from_name, parse_input
import test
import utils
import pandas as pd
import numpy as np
from Get_File_Paths import GetFileList
import random

data_folder = os.path.join(get_parent_dir(n=1),'Data')
image_folder = os.path.join(data_folder,'Street_View_Images')

houses_result_folder = os.path.join(data_folder,'House_Detection_Results') 
houses_result_file =  os.path.join(houses_result_folder, 'Housing_Results.csv')

openings_result_folder = os.path.join(data_folder,'Opening_Detection_Results') 
openings_result_file =  os.path.join(openings_result_folder, 'Opening_Results.csv')


model_folder =  os.path.join(data_folder,'Model_Weights')

houses_weights = os.path.join(model_folder,'Houses','trained_weights_final.h5')
houses_classes = os.path.join(model_folder,'Houses','data_classes.txt')

openings_input_folder = os.path.join(data_folder,'House_Cropping_Results')
openings_weights = os.path.join(model_folder,'Openings','trained_weights_final.h5')
openings_classes = os.path.join(model_folder,'Openings','data_all_classes.txt')

FLAGS = None

if __name__ == '__main__':
    # Delete all default flags
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''

    parser.add_argument(
        "--input_images", type=str, default=image_folder,
        help = "Path to image directory. All subdirectories will be included."
    )

    parser.add_argument(
        '--test', default=False, action="store_true",
        help='Test routine on 10 images in /Data/Street_View_Images'
    )

    parser.add_argument(
        "--output", type=str, default=houses_result_folder,
        help = "Output path for detection results."
    )

    parser.add_argument(
        "--detection_mode", type=str, default='houses',
        help = "If set to openings, use the pre-trained weights for openings. Otherwise use the pre-trained weights for houses. This overrides all other settings."
    )

    parser.add_argument(
        "--no_save_img", default=False, action="store_true",
        help = "do not save output images with annotated boxes"
    )

    parser.add_argument(
        '--yolo_model', type=str, dest='model_path', default = houses_weights,
        help='Use your own pre-trained weights. This option does NOT overide the --model_type flag setting.'
    )

    parser.add_argument(
        '--anchors', type=str, dest='anchors_path', default = 'src/keras_yolo3/model_data/yolo_anchors.txt',
        help='path to YOLO anchors'
    )

    parser.add_argument(
        '--classes', type=str, dest='classes_path', default = houses_classes,
        help='path to YOLO class specifications'
    )

    parser.add_argument(
        '--gpu_num', type=int, default = 1,
        help='Number of GPU to use'
    )

    parser.add_argument(
        '--confidence', type=float, dest = 'score', default = 0.1,
        help='YOLO object confidence threshold above which to show predictions'
    )
    
    parser.add_argument(
        '--box_file', type=str, dest = 'box', default = houses_result_file,
        help='Specify the destination to save bounding boxes'
    )
    
    parser.add_argument(
        '--postfix', type=str, dest = 'postfix', default = '_house',
        help='Specify the postfix for images with bounding boxes'
    )
    

    FLAGS = parser.parse_args()



    if FLAGS.detection_mode == 'openings' or FLAGS.detection_mode == 'opening':
        FLAGS.input_images = openings_input_folder
        FLAGS.model_path = openings_weights
        FLAGS.classes_path = openings_classes
        FLAGS.output = openings_result_folder
        FLAGS.box = openings_result_file
        FLAGS.postfix = '_opening'

    save_img = not FLAGS.no_save_img

    if FLAGS.test:
        input_image_paths = random.choices(GetFileList(image_folder),k=10)
    else:
        input_image_paths = GetFileList(FLAGS.input_images)

    print('Found {} input images: {}...'.format(len(input_image_paths), [ os.path.basename(f) for f in input_image_paths[:5]]))

    output_path = FLAGS.output
    if not os.path.exists(output_path):
        os.makedirs(output_path)


    # define YOLO logo detector
    yolo = YOLO(**{"model_path": FLAGS.model_path,
                "anchors_path": FLAGS.anchors_path,
                "classes_path": FLAGS.classes_path,
                "score" : FLAGS.score,
                "gpu_num" : FLAGS.gpu_num,
                "model_image_size" : (640, 640),
                }
               )

    # Make a dataframe for the prediction outputs
    out_df = pd.DataFrame(columns=['image', 'image_path','xmin', 'ymin', 'xmax', 'ymax', 'label','confidence','x_size','y_size'])

    # labels to draw on images
    class_file = open(FLAGS.classes_path, 'r')
    input_labels = [line.rstrip('\n') for line in class_file.readlines()]
    print('Found {} input labels: {}...'.format(len(input_labels), input_labels))



    start = timer()
    text_out = ''

    for i, img_path in enumerate(input_image_paths):
        print(img_path)
        prediction, image = detect_logo(yolo, img_path, save_img = save_img,
                                          save_img_path = FLAGS.output,
                                          postfix=FLAGS.postfix)
        y_size,x_size,_ = np.array(image).shape
        for single_prediction in prediction:
            out_df=out_df.append(pd.DataFrame([[os.path.basename(img_path.rstrip('\n')),img_path.rstrip('\n')]+single_prediction + [y_size,x_size]],columns=['image','image_path', 'xmin', 'ymin', 'xmax', 'ymax', 'label','confidence','x_size','y_size']))
    end = timer()
    print('Processed {} images in {:.1f}sec - {:.1f}FPS'.format(
         len(input_image_paths), end-start, len(input_image_paths)/(end-start)
         ))
    out_df.to_csv(FLAGS.box,index=False)
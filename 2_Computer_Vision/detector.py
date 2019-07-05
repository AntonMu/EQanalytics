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
src_path = os.path.join(os.getcwd(),'src')
sys.path.append(src_path)

utils_path = os.path.join(os.getcwd(),'Utils')
sys.path.append(utils_path)
import argparse
from keras_yolo3.yolo import YOLO
from PIL import Image
from timeit import default_timer as timer
from logos import detect_logo, match_logo
from similarity import load_brands_compute_cutoffs
from utils import load_extractor_model, load_features, model_flavor_from_name, parse_input
import test
import utils
import pandas as pd
import numpy as np
from Get_File_Paths import GetFileList

sim_threshold = 0.95
output_txt = 'out.txt'

data_folder = os.path.join(get_parent_dir(n=1),'Data')
image_folder = os.path.join(data_folder,'Street_View_Images')

houses_result_folder = os.path.join(data_folder,'House_Detection_Results') 
houses_result_file =  os.path.join(houses_result_folder, 'Housing_Results.csv')

openings_result_folder = os.path.join(data_folder,'Opening_Detection_Results') 
openings_result_file =  os.path.join(openings_result_folder, 'Opening_Results.csv')


model_folder =  os.path.join(data_folder,'Model_Weights')

houses_weights = os.path.join(model_folder,'Houses','trained_weights_final.h5')
houses_classes = os.path.join(model_folder,'Houses','data_classes.txt')

openings_weights = os.path.join(model_folder,'Openings','trained_weights_final.h5')
openings_classes = os.path.join(model_folder,'Openings','data_all_classes.txt')

FLAGS = None

if __name__ == '__main__':
    # class YOLO defines the default value, so suppress any default here
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''

    # parser.add_argument(
    #     '--image', default=False, action="store_true",
    #     help='Image detection mode'
    # )

    parser.add_argument(
        "--input_images", type=str, default=image_folder,
        help = "Path to image directory. All subdirectories will be included."
    )

    parser.add_argument(
        '--test', default=False, action="store_true",
        help='Test routine: run on few images in /Data/Street_View_Images'
    )

    parser.add_argument(
        "--output", type=str, default=result_folder,
        help = "Output path for detection results."
    )

    parser.add_argument(
        "--detection_mode", type=str, default='houses',
        help = "If set to openings, use the pre-trained weights for openings. Otherwise use the pre-trained weights for houses."
    )

    parser.add_argument(
        "--no_save_img", default=False, action="store_true",
        help = "do not save output images with annotated boxes"
    )

    parser.add_argument(
        '--yolo_model', type=str, dest='model_path', default = houses_weights,
        help='Use your own pre-trained weights. This option overides the --model_type flag.'
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

    if FLAGS.test:
        test.test(FLAGS.features)
        exit()


    # save_img_logo, save_img_match = not FLAGS.no_save_img, not FLAGS.no_save_img

    # if FLAGS.input_brands == 'input':
    #     print('Input logos to search for in images: (file-by-file or entire directory)')

    #     FLAGS.input_brands = parse_input()

    # elif os.path.isfile(FLAGS.input_brands):
    #     print("Loading input brands from text file: reading "+FLAGS.input_brands)
    #     if FLAGS.input_brands.endswith('.txt'):
    #         with open(FLAGS.input_brands, 'r') as file:
    #             FLAGS.input_brands = [os.path.abspath(f) for f in file.read().splitlines()]

    #     else:
    #         FLAGS.input_brands = [ os.path.abspath(FLAGS.input_brands)  ]

    # elif os.path.isdir(FLAGS.input_brands):
    #     FLAGS.input_brands = [ os.path.abspath(os.path.join(FLAGS.input_brands, f)) for f in os.listdir(FLAGS.input_brands) if f.endswith(('.jpg', '.png')) ]
    # else:
    #     exit('Error: path not found:{}'.format(FLAGS.input_brands))


    # if FLAGS.input_images.endswith('.txt'):
    #     print("Batch image detection mode: reading "+FLAGS.input_images)
    #     output_txt = FLAGS.input_images.split('.txt')[0]+'_pred.txt'
    #     FLAGS.save_to_txt = True
    #     with open(FLAGS.input_images, 'r') as file:
    #         file_list = [line.split(' ')[0] for line in file.read().splitlines()]
    #     FLAGS.input_images = [os.path.abspath(f) for f in file_list]


    # elif FLAGS.input_images == 'input':
    #     print('Input images to be scanned for logos: (file-by-file or entire directory)')
    #     FLAGS.input_images = parse_input()

    # elif os.path.isdir(FLAGS.input_images):
    #     FLAGS.input_images = [ os.path.abspath(os.path.join(FLAGS.input_images, f)) for f in os.listdir(FLAGS.input_images) if f.endswith(('.jpg', '.png')) ]
    # elif os.path.isfile(FLAGS.input_images):
    #     FLAGS.input_images = [ os.path.abspath(FLAGS.input_images)  ]
    # else:
    #     exit('Error: path not found: {}'.format(FLAGS.input_images))


    # print('Found {} input brands: {}...'.format(len(FLAGS.input_brands), [ os.path.basename(f) for f in FLAGS.input_brands[:5]]))
    print('Found {} input images: {}...'.format(len(FLAGS.input_images), [ os.path.basename(f) for f in FLAGS.input_images[:5]]))

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
    out_df = pd.DataFrame(columns=['image', 'xmin', 'ymin', 'xmax', 'ymax', 'label','confidence','x_size','y_size'])
    
    # input_paths = sorted(FLAGS.input_brands)
    
    # labels to draw on images - could also be read from filename
    input_labels = [ os.path.basename(s).split('test_')[-1].split('.')[0] for s in input_paths]

    # get Inception/VGG16 model and flavor from filename
    # model_name, flavor = model_flavor_from_name(FLAGS.features)
    ## load pre-processed LITW features database
    # features, brand_map, input_shape = load_features(FLAGS.features)

    ## load inception model
    # model, preprocess_input, input_shape = load_extractor_model(model_name, flavor)
    # my_preprocess = lambda x: preprocess_input(utils.pad_image(x, input_shape))

    # compute cosine similarity between input brand images and all LogosInTheWild logos
    # ( img_input, feat_input, sim_cutoff, (bins, cdf_list)
    # ) = load_brands_compute_cutoffs(input_paths, (model, my_preprocess), features, sim_threshold)

    start = timer()
    # cycle trough input images, look for logos and then match them against inputs
    text_out = ''
    for i, img_path in enumerate(FLAGS.input_images):
        text = img_path
        prediction, image = detect_logo(yolo, img_path, save_img = save_img_logo,
                                          save_img_path = FLAGS.output,
                                          postfix=FLAGS.postfix)

        # text = match_logo(image, prediction, (model, my_preprocess), text,
        #           (feat_input, sim_cutoff, bins, cdf_list, input_labels),
        #           save_img = save_img_match, save_img_path=FLAGS.output)
        
        # print(text)
        y_size,x_size,_ = np.array(image).shape
        for single_prediction in prediction:
#                 row = [text]
#                 row.append(prediction)
#                 print('row',row)
#                 print(type(prediction))
#                 print([text]+single_prediction)
            out_df=out_df.append(pd.DataFrame([[text[:-1]]+single_prediction + [y_size,x_size]],columns=['image', 'xmin', 'ymin', 'xmax', 'ymax', 'label','confidence','x_size','y_size']))
#             print(prediction)
        # text_out += (text)

        # if FLAGS.save_to_txt:
        #     with open(output_txt,'w') as txtfile:
        #         txtfile.write(text_out)

        end = timer()
        print('Processed {} images in {:.1f}sec - {:.1f}FPS'.format(
             len(FLAGS.input_images), end-start, len(FLAGS.input_images)/(end-start)
             ))
        out_df.to_csv(FLAGS.box,index=False)

    # video mode
    # # elif FLAGS.video:
    # else:
    #     print("Must specify either --image or --video.  See usage with --help.")

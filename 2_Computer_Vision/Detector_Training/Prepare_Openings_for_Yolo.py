from PIL import Image
from os import path, makedirs
import os
import re 
import pandas as pd
import sys
import argparse
def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.getcwd()
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path
sys.path.append(os.path.join(get_parent_dir(1),'Utils'))
from Convert_Format import convert_vott_csv_to_yolo, csv_from_xml
from Get_File_Paths import ChangeToOtherMachine

Data_Folder = os.path.join(get_parent_dir(2),'Data')
CMP_Folder = os.path.join(Data_Folder,'CMP_Facade_DB')
CSV_filename = os.path.join(CMP_Folder,'Annotations.csv')
labels_filename = os.path.join(CMP_Folder,'label_names.txt')
classes_filename = os.path.join(CMP_Folder,'data_all_classes.txt')
YOLO_filename = os.path.join(CMP_Folder,'data_all_train.txt')
AWS_path = '/home/ubuntu/'

if __name__ == '__main__':
    # surpress any inhereted default values
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    # parser.add_argument(
    #     "--VoTT_Folder", type=str, default=VoTT_Folder,
    #     help = "absolute path to the exported files from the image tagging step with VoTT."
    # )

    # parser.add_argument(
    #     "--VoTT_csv", type=str, default=VoTT_csv,
    #     help = "absolute path to the *.csv file exported from VoTT. The default name is 'Houses-export.csv'."
    # )
    parser.add_argument(
        "--YOLO_filename", type=str, default=YOLO_filename,
        help = "absolute path to the file where the annotations in YOLO format should be saved. The default name is 'data_train.txt' and is saved in the VoTT folder."
    )

    # parser.add_argument(
    #     "--item_name", type=str, default='house',
    #     help = "The name of the annotated item. The default is 'house'."
    # )


    parser.add_argument(
        '--AWS', default=True, action="store_true",
        help='Enable this flag if you plan to train on AWS but did your pre-processing on a local machine.'
    )

    FLAGS = parser.parse_args()

    df_csv = csv_from_xml(CMP_Folder)
    if FLAGS.AWS:
        df_csv['image_path']=ChangeToOtherMachine(df_csv['image_path'].values,remote_machine=AWS_path)
    df_csv.to_csv(CSV_filename,index=False)

    #Get label names and sort 
    file = open(labels_filename,"r")
    label_df = pd.read_csv(labels_filename,sep=' ',header=None)
    labellist = sorted(zip(label_df.iloc[:,2].values,label_df.iloc[:,1].values))
    sorted_names = [x[1] for x in labellist]

    #Write sorted names to file to make classes file
    with open(classes_filename, 'w') as f:
        for name in sorted_names:
            f.write("%s\n" % name)
    # Convert Vott csv format to YOLO format
    convert_vott_csv_to_yolo(df_csv,abs_path = True,target_name=FLAGS.YOLO_filename)



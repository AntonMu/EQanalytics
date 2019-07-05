from os import path, makedirs
import pandas as pd
import numpy as np
import re
import os
from PIL import Image

def get_files(directory,ending='.jpg'):
    result=[]
    for file in os.listdir(directory):
        if file.endswith(ending):
            result.append(file)
    return result

def convert_vott_csv_to_yolo(vott_df,labeldict,path='',target_name='data_all_train.txt'):
    
    #Encode labels according to labeldict 
    vott_df['code']=vott_df['label'].apply(lambda x: labeldict[x])
    #Round float to ints
    for col in vott_df[['xmin', 'ymin', 'xmax', 'ymax']]:
        vott_df[col]=(vott_df[col]).apply(lambda x: round(x))
        
    #Crete Yolo Text file
    last_image = ''
    txt_file = ''

    for index,row in vott_df.iterrows():
        if not last_image == row['image']:
            txt_file +='\n'+os.path.join(path,row['image']) + ' '
            txt_file += ','.join([str(x) for x in (row[['xmin', 'ymin', 'xmax', 'ymax','code']].tolist())])
        else:
            txt_file += ' '
            txt_file += ','.join([str(x) for x in (row[['xmin', 'ymin', 'xmax', 'ymax','code']].tolist())])
        last_image = row['image']
    file = open(target_name,"w") 
    file.write(txt_file[1:]) 
    file.close() 
    return True


def csv_from_xml(directory,path_name=''):
    #First get all images and xml files from path
    image_paths=get_files(directory,'.jpg')
    xml_paths=get_files(directory,'.xml')
    result_df = pd.DataFrame()
    if not len(image_paths)==len(xml_paths):
        print('number of annotations doesnt match number of images')
        return False
    for image in image_paths:
        target_filename = path_name + '/'+image if path_name else image
        source_filename = directory + '/'+image
        y_size,x_size,_ = np.array(Image.open(source_filename)).shape
        source_xml = directory + '/'+image.replace('.jpg','.xml')
        txt= open(source_xml,"r").read()
        y_vals = re.findall(r'(?:x>\n)(.*)(?:\n</)',txt)
        ymin_vals = y_vals[::2]
        ymax_vals = y_vals[1::2]
        x_vals = re.findall(r'(?:y>\n)(.*)(?:\n</)',txt)
        xmin_vals = x_vals[::2]
        xmax_vals = x_vals[1::2]
        label_vals = re.findall(r'(?:label>\n)(.*)(?:\n</)',txt)
        label_name_vals = re.findall(r'(?:labelname>\n)(.*)(?:\n</)',txt)
        df = pd.DataFrame()
        df['xmin']=xmin_vals
        df['xmin']= df['xmin'].astype(float)*x_size
        df['ymin']=ymin_vals
        df['ymin']= df['ymin'].astype(float)*y_size
        df['xmax']=xmax_vals
        df['xmax']= df['xmax'].astype(float)*x_size
        df['ymax']=ymax_vals
        df['ymax']= df['ymax'].astype(float)*y_size
        df['label']=label_name_vals
        df['label_id']=label_vals
        df['image']=target_filename
        result_df=result_df.append(df)
#     Bring image column first
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    result_df = result_df[cols]
    return result_df
if __name__ == '__main__':
    #Prepare the houses dataset for YOLO
    labeldict = dict(zip(['house'],[0,]))
    multi_df = pd.read_csv('C:/Users/Anton/Documents/Insight/eq/EQ_new/Train_Housing_detector/2/vott-csv-export/Housing_cropping-export.csv')
    multi_df.drop_duplicates(subset=None, keep='first', inplace=True)
    convert_vott_csv_to_yolo(multi_df,labeldict,path = '/home/ubuntu/logohunter/data/houses/',target_name='data_train.txt')

    #Prepare the windows dataset for YOLO
    path = 'C:/Users/Anton/Documents/Insight/eq/EQ_new/Train_Window_Detector/base'
    csv_from_xml(path,'/home/ubuntu/logohunter/data/windows').to_csv('C:/Users/Anton/Documents/Insight/eq/EQ_new/Train_Window_Detector/base/annotations.csv')   

    label_names = ['background', 'facade', 'molding', 'cornice', 'pillar', 'window', 'door', 'sill', 'blind', 'balcony', 'shop', 'deco']
    labeldict = dict(zip(label_names,list(range(12))))
    convert_vott_csv_to_yolo(csv_from_xml(path,'/home/ubuntu/logohunter/data/windows'),labeldict)
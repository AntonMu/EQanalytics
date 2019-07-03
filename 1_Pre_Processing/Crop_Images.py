from PIL import Image
from os import path, makedirs
import re 
import pandas as pd

def crop_and_save(image_df,source_path = '',target_path = 'cropped', one =True):
    """Takes a vott_csv file with image names, labels and crop_boxes
    and crops the images accordingly
    
    Input csv file format:
    
    image   xmin ymin xmax ymax label
    im.jpg  0    10   100  500  house

    
    Parameters
    ----------
    df : pd.Dataframe 
        The input dataframe with file_names, bounding box info
        and label
    source_path : str
        Path of source images
    target_path : str, optional
        Path to save cropped images
    one : boolean, optional
        if True, only the most central house will be returned

    Returns
    -------
    True if completed succesfully
    """
    target_path = os.path.join(os.getcwd(), target_path)
    if not path.isdir(target_path):
        makedirs(target_path)
    source_path = os.path.join(os.getcwd(),source_path)
    previous_name = ''
    counter = 0
    def find_rel_position(row):
        current_name = row['image']
        x_size,_ = (Image.open(os.path.join(source_path, current_name)).size)
        x_centrality = abs((row['xmin']+ row['xmax'])/2/x_size-.5)
        return x_centrality        
    if one:
        centrality = []
        for index, row in image_df.iterrows():
            centrality.append(find_rel_position(row))
        image_df['x_centrality'] = pd.Series(centrality)
        image_df.sort_values(['image','x_centrality'], inplace = True) 
        image_df.drop_duplicates(subset ="image", keep = 'first', inplace = True) 
        
    for index, row in image_df.iterrows():
        current_name = row['image']
        if current_name == previous_name:
            counter+=1
        else:
            counter =0
        image_path = os.path.join(source_path, current_name)
        imageObject  = Image.open(image_path)
        cropped = imageObject.crop((row['xmin'],row['ymin'],row['xmax'],row['ymax']))
        image_name_cropped = '_'.join([current_name[:-4],'cropped',row['label'],str(counter)])+'.jpg'

        cropped.save(os.path.join(target_path,image_name_cropped))
        previous_name = current_name
    return True

image_df = pd.read_csv("./vott-csv-export/Houses-export.csv")
crop_and_save(image_df,source_path = 'vott-csv-export',target_path = 'cropped_one')            
from PIL import Image
import numpy as np
from os import path, makedirs
import numpy as np
import re
import os
import pandas as pd
def get_files(directory,ending='.jpg'):
    result=[]
    for file in os.listdir(directory):
        if file.endswith(ending):
            result.append(file)
    return result

def load_and_filter_df(df_path,file_path,label_dict):
    file_list = get_files(file_path)
    file_list=[x[:-14]+'.jpg' for x in file_list]
    df=pd.read_csv(df_path)
    df['file']=df['image'].apply(lambda x: (x.split('/'))[-1])
    df['label_name']=df['label'].apply(lambda x: label_dict[x])
    return df[df['file'].isin(file_list)]    
    
def prepare_df(df, label_names = ['door', 'window', 'blind', 'shop']):
    df.loc[:,'x_len']=(df['xmax']-df['xmin'])
    df.loc[:,'y_len']=(df['ymax']-df['ymin'])
    df.loc[:,'rel_y_center']=(df['ymin']+df['ymax'])/2/df['y_size']
    df.loc[:,'area']=df['x_len']*df['y_len']
    return df[df['label_name'].isin(['door', 'window', 'blind', 'shop'])]

def get_iou(re1, re2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    bb1 = dict(zip(['x1','x2','y1','y2'],re1))
    bb2 = dict(zip(['x1','x2','y1','y2'],re2))
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou

def find_index_to_keep(rect,rects,areas,iou_threshold=.75):
    rects=np.asarray(rects)
    ious = []
    for re in rects:
        ious.append(get_iou(rect,re))
    intersect=(np.array(ious)>iou_threshold)
    overlaps = np.argwhere(intersect)
    #We only keep the one with the biggest area and return it
    return overlaps[np.argmax(areas[overlaps])]

def remove_overlaps(df):
    image_names = df['image'].unique()
    result_df = pd.DataFrame()
    for image_name in image_names:
        current_df = df[df['image']==image_name].copy()
        rects = current_df[['xmin','xmax','ymin','ymax']].values
        areas = np.array(current_df['area'].tolist())
        indices_to_keep = []
        for index, row in current_df.iterrows():
            indices_to_keep.append(find_index_to_keep(list(row[['xmin','xmax','ymin','ymax']]),rects,areas))
        result_df=result_df.append(current_df.iloc[np.unique(np.array(indices_to_keep))])
    return result_df

from sklearn.cluster import KMeans
def add_levels(df,threshold=2e-3):
    image_names = df['image'].unique()
    result_df = pd.DataFrame()
    for image_name in image_names:
        current_df = df[df['image']==image_name].copy()
        y=np.array(current_df['rel_y_center'])
        data = np.array([0*y,y]).T
        scores = np.array([KMeans(n_clusters=n, random_state=42,n_init=2).fit(data).score(data) for n in range(1,min(8,len(data)))])/(len(y))
        number_of_stories = sum(((np.diff(scores))>threshold))+1
        kmeans = KMeans(n_clusters=number_of_stories, random_state=42,n_init=2).fit(data)
        order_dict = dict(zip(kmeans.predict(np.sort(kmeans.cluster_centers_.T).T),list(range(number_of_stories,0,-1))))
        current_df.loc[:,'level']=kmeans.predict(data)
        current_df['level'] = current_df['level'].apply(lambda x: order_dict[x] )
        result_df=result_df.append(current_df)
    return result_df

# Calculate soft score
def calcuate_softness(df,metric='x_len'):
    image_names = df['image'].unique()
    result_df = pd.DataFrame(columns = ['image','score'])
    for image_name in image_names:
        current_df = df[df['image']==image_name].copy()
        result_df=result_df.append(pd.DataFrame([[image_name,sum(current_df[current_df['level']==2][metric])/sum(current_df[current_df['level']==1][metric])]], columns = ['image','score']))
    result_df.reset_index(inplace=True,drop=True)
    result_df['type'] = result_df['score'].apply(lambda x: 'soft' if x<.75 else 'unknown' if x>1.5 else 'non_soft')
    return result_df


# df_path = 'C:/Users/Anton/Documents/Insight/eq/EQ_new/Final_Segmentation/multi.csv'
# file_path = 'C:/Users/Anton/Documents/Insight/eq/EQ_new/Final_Segmentation/Selection/'
df_path = 'multi.csv'
file_path = 'Selection/'
label_names = ['background', 'facade', 'molding', 'cornice', 'pillar', 'window', 'door', 'sill', 'blind', 'balcony', 'shop', 'deco']
label_dict = dict(zip(list(range(12)),label_names))
calcuate_softness(add_levels(remove_overlaps(prepare_df(remove_overlaps(prepare_df(prepare_df(load_and_filter_df(df_path,file_path,label_dict)))))).sort_values('image'))).to_csv('Softness_Results.csv',index=False)
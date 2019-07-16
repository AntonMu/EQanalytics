import os
import sys

#Check the postifx!!!!!!!!!!!!!!!!!! in the csv file

from PIL import Image
import numpy as np
from os import path, makedirs
import numpy as np
import re
import pandas as pd
from sklearn.cluster import KMeans
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from sympy import Interval, Union

def ChangeToOtherMachine(filelist,repo='EQanalytics',remote_machine =''):
    '''
    Takes a list of file_names located in a repo and changes it to the local machines file names. File must be executed from withing the repository

    Example:

    '/home/ubuntu/EQanalytics/Data/Street_View_Images/vulnerable/test.jpg'

    Get's converted to
    
    'C:/Users/Anton/EQanalytics/Data/Street_View_Images/vulnerable/test.jpg'

    '''
    filelist = [x.replace("\\","/") for x in filelist]
    if repo[-1]=='/':
        repo=repo[:-1]
    if remote_machine:
        prefix = remote_machine.replace("\\","/")
    else:
        prefix = ((os.path.dirname(os.path.abspath(__file__)).split(repo))[0]).replace("\\","/")
    new_list = []

    for file in filelist:
        suffix = (file.split(repo))[1]
        if suffix[0]=='/':
            suffix = suffix[1:]
        new_list.append(os.path.join(prefix,repo+'/',suffix).replace("\\","/"))
    return new_list

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
    
def get_features(df, label_dict, label_names = ['door', 'window', 'blind', 'shop']):
    df['label_name'] = df['label'].apply(lambda x: label_dict[x])
    df.loc[:,'x_len']=(df['xmax']-df['xmin'])
    df.loc[:,'y_len']=(df['ymax']-df['ymin'])
    df.loc[:,'rel_y_center']=(df['ymin']+df['ymax'])/2/df['y_size']
    df.loc[:,'area']=df['x_len']*df['y_len']
    return df[df['label_name'].isin(label_names)]

def get_intervall_union(data):
    """
    Given a list of intervals, i.e. a = [(7, 10), (11, 13), (11, 15), (14, 20), (23, 39)],
    this function return the length of the interval union. In the example it takes the union 
    as [Interval(7, 10), Interval(11, 20), Interval(23, 39)] and computes the length as 28
    """
    #Convert to list of tuples if the input is list of list:
    if not data:
        return 0
    if type(data[0])==type([]):
        data = [tuple(l) for l in data]
    intervals = [Interval(begin, end) for (begin, end) in data]
    u = Union(*intervals)
    union_list =  [list(u.args[:2])] if isinstance(u, Interval) else list(u.args)
    length=0
    if type(union_list[0])==type([]):
        union_list = [tuple(l) for l in union_list]
        union_list = [Interval(begin, end) for (begin, end) in union_list]
    for item in union_list:
        length+=item.end- item.start
    return length

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

def remove_overlaps(df,iou_threshold=.75):
    image_names = df['image'].unique()
    result_df = pd.DataFrame()
    for image_name in image_names:
        current_df = df[df['image']==image_name].copy()
        rects = current_df[['xmin','xmax','ymin','ymax']].values
        areas = np.array(current_df['area'].tolist())
        indices_to_keep = []
        for index, row in current_df.iterrows():
            indices_to_keep.append(find_index_to_keep(list(row[['xmin','xmax','ymin','ymax']]),rects,areas,iou_threshold=iou_threshold))
        result_df=result_df.append(current_df.iloc[np.unique(np.array(indices_to_keep))])
    return result_df

def find_levels(df,threshold=2e-3,save_levels=False):
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

def draw_levels(df, target_path, colors = ['#fdfe02','#0bff01','#fe0000','#fe00f6','#011efe'],suffix='_levels'):
    image_names = ChangeToOtherMachine(df['image_path'].unique())
    for image_name in image_names:
        current_df = df[df['image']==os.path.basename(image_name)].copy()
        source_img = Image.open(image_name).convert("RGBA")
        draw = ImageDraw.Draw(source_img)
        levels = current_df['level'].unique()
        for level in levels:
            for index,row in current_df[current_df['level']==level].iterrows():
                draw.rectangle(((row['xmin'], row['ymin']), (row['xmax'], row['ymax'])),outline=colors[level%len(colors)],width = 2)
                try:
                    #There are some issues with loading fonts
                    draw.text((row['xmin']+2, row['ymin']), str(level),fill=colors[level%len(colors)],font=ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),'Utils','arial.ttf'),16 ))
                except:
                    draw.text((row['xmin']+2, row['ymin']), str(level),fill=colors[level%len(colors)])
        source_img.convert("RGB").save(os.path.join(target_path,''.join([os.path.basename(image_name)[:-4],suffix,".jpg"])), "JPEG")
    return True

# Calculate soft score
def calcuate_softness(df,metric='x_len'):
    def score(x):
        if x>.75:
            return 'non_soft'
        else:
            return 'soft'
    image_names = df['image'].unique()
    result_df = pd.DataFrame(columns = ['image','score'])
    for image_name in image_names:
        current_df = df[df['image']==image_name].copy()
        if metric == 'area':
            result_df=result_df.append(pd.DataFrame([[image_name,sum(current_df[current_df['level']==2]['area'])/sum(current_df[current_df['level']==1]['area'])]], columns = ['image','score']))
        else:
            #In this case we take the interval union of all x-widths
            scores=[]
            for level in [1,2]:
                #metric[0]+'min' equals xmin for metric = 'x_len' and ymin for metric = 'y_len'
                scores.append(current_df[metric[0]+'_size'].iloc[0]-get_intervall_union(list(zip(current_df[current_df['level']==level][metric[0]+'min'].values,current_df[current_df['level']==level][metric[0]+'max'].values))))
            # To avoid divsion by 0 we take the max of scores[1] and 1.
            result_df=result_df.append(pd.DataFrame([[image_name,float(scores[0])/max(float(scores[1]),1.)]], columns = ['image','score']))
    result_df.reset_index(inplace=True,drop=True)
    result_df['type'] = result_df['score'].apply(lambda x: score(x))
    return result_df

def get_address(df,column = 'image'):
    df['address']=df[column].apply(lambda x: ((re.findall(r'_\d{1,}?\+.*\+', x))[0][1:]).replace('+',' '))
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    return df
import pandas as pd
import difflib
from os import path, makedirs
import time
import json
import requests
import os


def get_parent_dir(n=1):
    """ returns the n-th parent dicrectory of the current
    working directory """
    current_path = os.path.dirname(os.path.abspath(__file__))
    for k in range(n):
        current_path = os.path.dirname(current_path)
    return current_path


def ignore_non_int(df, column="NUMBER"):
    """Returns a df with all rows removed that 
    do not have integers in 'column'
    
    Parameters
    ----------
    df : pd.Dataframe 
        The input dataframe that contains
        'column'
    column : str, optional
        The name of the column that should
        only contain integers

    Returns
    -------
    pd.DataFrame
        The dataframe with rows removed
    """

    def to_int(x):
        try:
            return int(x)
        except:
            return x

    df[column] = df[column].apply(lambda x: to_int(x))
    df["dtypes"] = df[column].apply(lambda x: type(x))
    df = df.loc[df["dtypes"] == type(1)]
    df.drop("dtypes", axis=1, inplace=True)
    df[column] = df[column].apply(lambda x: to_int(x))
    return df


def seperate_house_numbers(df, column="address", city="SAN FRANCISCO"):
    """Returns a df that splits the 'address'
    column in house number, street number and 
    building
    
    Parameters
    ----------
    df : pd.Dataframe 
        The input dataframe that contains an
        'address' column

    Returns
    -------
    pd.DataFrame
        The dataframe with seperate columns
        for NUMBER, STREET, BUILDING
    """
    # Seperate Street and number
    df[["NUMBER", "STREET"]] = pd.DataFrame(
        df[column].str.split(" ", 1).tolist(), columns=["NUMBER", "STREET"]
    )
    df["CITY"] = city
    return df


# Split the odd numbers into seperate columns
def tidy_split(df, column, sep="|", keep=False):
    """
    Split the values of a column and expand so the new DataFrame has one split
    value per row. Filters rows where the column is missing.
    
    https://github.com/cognoma/genes/blob/721204091a96e55de6dcad165d6d8265e67e2a48/2.process.py

    Params
    ------
    df : pandas.DataFrame
        dataframe with the column to split and expand
    column : str
        the column to split and expand
    sep : str
        the string used to split the column's values
    keep : bool
        whether to retain the presplit value as it's own row

    Returns
    -------
    pandas.DataFrame
        Returns a dataframe with the same columns as `df`.
    """
    indexes = list()
    new_values = list()
    df = df.dropna(subset=[column])
    for i, presplit in enumerate(df[column].astype(str)):
        values = presplit.split(sep)
        if keep and len(values) > 1:
            indexes.append(i)
            new_values.append(presplit)
        for value in values:
            indexes.append(i)
            new_values.append(value)
    new_df = df.iloc[indexes, :].copy()
    new_df[column] = new_values
    return new_df


def find_similar_clusters(df, column_name, cutoff=0.8):
    """Returns a clusters of similar terms in column_name of the
    DataFrame df. The cut_off variable determines the threshold
    for similarity
    
    Parameters
    ----------
    df : pd.Dataframe 
        The input dataframe with a column 'column_name'
    column_name : str
        The name of the columns of categories to be clustered
    cutoff : float, optional
        Value betweeen 0 and 1 that gives the similarity threshol

    Returns
    -------
    list of list of expressions that are similar.
        
    """
    #     Make a list of all unique items in column
    cats = list(pd.DataFrame(df[column_name].value_counts()).index)

    # Find similar clusters
    logical_sets = []
    for cat in cats:
        cluster = difflib.get_close_matches(cat, cats, n=10, cutoff=cutoff)
        cluster.sort()
        logical_sets.append(cluster)

        # Delete duplicates
    unique_list = []
    for logical_set in logical_sets:
        if not logical_set in unique_list:
            unique_list.append(logical_set)
    return unique_list


## Download Street View Images for Datasets via Google API
def download_images(
    df,
    filelist_df,
    api_key="",
    dir_path="images",
    class_name="vulnerable",
    title="view",
    category="",
    pitch=10,
    save_tier=False,
):
    """Downloads all Street view for all rows with addresses in df. 
    Parameters
    ----------
    df : pd.Dataframe 
        The df with rows that contain at least the columns
        'CITY', 'STREET', 'NUMBER', 'LAT', 'LON'
    api_key : str, optional
        Google Maps Street View API key, without the key only 
        the request url is returned
    dir_path : str, optional
        The path of the download folder
    class_name : str, optional
        The label of the data to download
    title : str, optional
        The name of the image file
    category : str, optional
        An additional layer of nesting within
        the class
    pitch : int, optional
        the camera angle of the street view image,
        0 is horizontal
    output: str, optional
        'first': returns rows that are only in df1
        'both': returns rows that are both in df1 and df2
        'second': returns rows that are only in df2

    Returns
    -------
    Downloads all images to their respective folders as jpg 
    and saves all other info in a json file with the same name.
    returns True once completed. 
        
    """

    def empty_str(x):
        if str(x) == "nan":
            return ""
        else:
            return x

    total_path = ("/").join([dir_path, class_name])
    tier_root = ("/").join([dir_path, class_name])
    if not path.isdir(total_path):
        makedirs(total_path)
    if category:
        category = (
            category.replace(" ", "-")
            .replace("/", "-")
            .replace(",", "-")
            .replace("--", "-")
        )
        total_path = ("/").join([total_path, category])
        if not path.isdir(total_path):
            makedirs(total_path)
    for index, row in df.iterrows():
        address_str = (
            ("+")
            .join([str(row["NUMBER"]), row["STREET"], row["CITY"],])
            .replace(" ", "+")
        )

        tier = 0 if row["TIER"] == " " else row["TIER"]
        try:
            unit = empty_str(row["UNIT"])
            address_str += "+" + unit
        except:
            pass
        try:
            postcode = str(row["POSTCODE"])
            address_str += "+" + postcode
        except:
            pass
        file_name = ("_").join(
            [
                title,
                class_name,
                # str(int(time.time())),
                str(pitch),
                str(tier),
                address_str,
            ]
        )
        if category:
            file_name += "+" + category

        url = "https://maps.googleapis.com/maps/api/streetview?source=outdoor&size=640x640"
        url += "&pitch=" + str(pitch)
        url += "&key=" + api_key
        url += "&location=" + address_str

        file_path = path.join(total_path, file_name)
        filelist_df = filelist_df.append(
            pd.DataFrame(
                [[file_name + ".jpg", file_path + ".jpg", category, tier, class_name]],
                columns=["image", "full_path", "category", "tier", "class"],
            )
        )
        if api_key:
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path + ".jpg", "wb") as f:
                    f.write(response.content)
                with open(file_path + ".json", "w") as f:
                    f.write(str(row.to_json()))
                if save_tier:
                    tier_path = ("/").join([tier_root, str(tier)])
                    if not path.isdir(tier_path):
                        makedirs(tier_path)
                    tier_file_path = path.join(tier_path, file_name)
                    with open(tier_file_path + ".jpg", "wb") as f:
                        f.write(response.content)
    return filelist_df

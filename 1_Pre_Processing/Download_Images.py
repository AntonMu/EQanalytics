#
# MASTER SCRIPT TO CLEAN UP ADDRESS FILE AND DOWNLOAD IMAGES VIA GOOGLE API
# for each adress in the address list we download the google street view images
#

import argparse
import os
from Location_Utils import get_parent_dir, ignore_non_int, seperate_house_numbers,tidy_split,find_similar_clusters,download_images
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

result_folder = os.path.join(get_parent_dir(n=1),'Data','Street_View_Images')
result_file = os.path.join(result_folder,'results.csv')
address_file = os.path.join(os.getcwd(),'Locations','SF.csv')
test_address_file = os.path.join(os.getcwd(),'Locations','Test_SF.csv')
FLAGS = None

if __name__ == '__main__':
    # surpress any inhereted default values
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    '''
    Command line options
    '''
    parser.add_argument(
        "--address_file", type=str, default=address_file,
        help = "absolute path to address_file. Please make sure the table structure is correct."
    )

    parser.add_argument(
        "--result_folder", type=str, default=result_folder,
        help = "absolute path to output directory"
    )
    parser.add_argument(
        "--result_file", type=str, default=result_file,
        help = "absolute path to result file"
    )

    parser.add_argument(
        "--city", type=str, default='SAN FRANCISCO',
        help = "The city of the provided addresses"
    )

    parser.add_argument(
        "--G_API_key", type=str, default='',
        help = "Google maps API key. Key is required to download images. Go to https://console.cloud.google.com/ to obtain a key for up to 30,000 free requests."
    )

    parser.add_argument(
        '--test', default=False, action="store_true",
        help='Test routine: run on addresses in ../Locations/Test_SF.csv'
    )

    parser.add_argument(
        "--pitch", type=int, default=10,
        help = "Pitch angle of Google Street View Images."
    )

    FLAGS = parser.parse_args()

    if FLAGS.test:
        df_vul = seperate_house_numbers(pd.read_csv(test_address_file),column = 'PROPERTY',city = FLAGS.city)
    else:
        df_vul = seperate_house_numbers(pd.read_csv(address_file),column = 'PROPERTY',city = FLAGS.city)
    df_vul=tidy_split(df_vul,'NUMBER',sep='+')
    df_vul=ignore_non_int(df_vul)
    df_vul.dropna(axis=0,subset=['TIER'], inplace=True)
    df_vul_clusters = find_similar_clusters(df_vul, column_name ='STATUS',cutoff=.97)


    ## Download buildings by category
    if not FLAGS.G_API_key:
        print('No Google API key provided. Downloading images will only be simulated.','\n')
    results_df = pd.DataFrame(columns = ['image','full_path','category','tier','class'])
    for cluster in df_vul_clusters:
        print('Currently Downloading Images for', cluster[0], 'Category')
        results_df= download_images(df_vul[df_vul['STATUS'].isin(cluster)],results_df,dir_path = result_folder,
                               class_name='vulnerable',
                               category = cluster[0],api_key=FLAGS.G_API_key,save_tier=False)
    results_df.to_csv(result_file,index=False)
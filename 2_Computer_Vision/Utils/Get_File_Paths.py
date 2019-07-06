from os import path, makedirs
import os
'''
For the given path, get the List of all files in the directory tree 
https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
'''
def GetFileList(dirName,ending='.jpg'):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + GetFileList(fullPath)
        else:
            if entry.endswith(ending):
                allFiles.append(fullPath)
                
    return allFiles        
 
def Change_Local_Machine(filelist,repo='EQanalytics'):
    '''
    Takes a list of file_names located in a repo and changes it to the local machines file names. File must be executed from withing the repository

    Example:

    '/home/ubuntu/EQanalytics/Data/Street_View_Images/vulnerable/test.jpg'

    Get's converted to
    
    'C:/Users/Anton/EQanalytics/Data/Street_View_Images/vulnerable/test.jpg'

    '''
    current_directory = os.getcwd()
    home_folder = os.getcwd().split(repo)[0]
    print(home_folder)
    new_list = []

    for file in filelist:
        print(file.split(repo))
        
        
if __name__ == '__main__':
    filelist = ['/home/ubuntu/EQanalytics/Data/Street_View_Images/vulnerable/test.jpg', '/home/ubuntu/EQanalytics/Data/Street_View_Images/vulnerable/test1.jpg']

    Change_Local_Machine(filelist)
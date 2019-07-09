import os
import subprocess
import time

# First get the references to all folders
Data_Folder = os.path.join(os.getcwd(),'Data')
Model_Folder = os.path.join(Data_Folder,'Model_Weights')

#Next download the pre-trained weights
download_script = os.path.join(Model_Folder,'Download_Weights.py')

print('Downloading Pretrained Weights')
start = time.time()
# call_string = ' '.join(['python',download_script,'1aPCwYXFAOmklmNMLMh81Yduw5UrbHqkN', os.path.join(Model_Folder,'Houses','trained_weights_final.h5') ])

# subprocess.call(call_string , shell=True)

# call_string = ' '.join(['python',download_script, '1FbvHzQWCjucXPbTbI4S1MnBLkAi58Mxv', os.path.join(Model_Folder,'Openings','trained_weights_final.h5') ])

# subprocess.call(call_string , shell=True)
end = time.time()
print('Downloaded Pretrained Weights in {0:.1f} seconds'.format(end-start))

# Data_Folder = os.path.join(get_parent_dir(2),'Data',Min)
# Facade_Folder = os.path.join(Data_Folder,'CMP_Facade_DB')
# YOLO_filename = os.path.join(Facade_Folder,'data_all_train.txt')
# log_dir = os.path.join(Data_Folder,'Model_Weights','Openings')
# YOLO_classname = os.path.join(log_dir,'data_all_classes.txt')

# def make_call_string(arglist):
# 	result_string = ''
# 	for arg in arglist:
# 		result_string+= ''.join(['--',arg[0],' ', arg[1],' '])
# 	return result_string

# arglist = [['annotation_file',YOLO_filename],['classes_file',YOLO_classname],['log_dir',log_dir]]
# call_string = ' '.join(['python Train.py',make_call_string(arglist)])

# print('Calling', call_string)
# subprocess.call(call_string, shell=True)
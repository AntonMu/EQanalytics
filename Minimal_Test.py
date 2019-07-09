import os
import subprocess
import time

def make_call_string(arglist):
    result_string = ''
    for arg in arglist:
        result_string+= ''.join(['--',arg[0],' ', arg[1],' '])
    return result_string

# First get the references to all folders
Data_Folder = os.path.join(os.getcwd(),'Data')
Model_Folder = os.path.join(Data_Folder,'Model_Weights')
Test_Folder =  os.path.join(Data_Folder,'Minimal_Test')
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

# Now run the housing detector
detector_script = os.path.join(os.getcwd(),'2_Computer_Vision','detector.py')


image_folder = Test_Folder
houses_result_file =  os.path.join(Test_Folder, 'Housing_Results.csv')
model_folder =  os.path.join(data_folder,'Model_Weights')
houses_weights = os.path.join(model_folder,'Houses','trained_weights_final.h5')
houses_classes = os.path.join(model_folder,'Houses','data_classes.txt')


arglist = [['input_images',Test_Folder],['classes_file',houses_classes],['output',Test_Folder],['yolo_model',houses_weights],['box_file',houses_result_file]]
call_string = ' '.join(['python', detector_script,make_call_string(arglist)])

print('Detecting Houses by calling \n', call_string)
start = time.time()
subprocess.call(call_string, shell=True)
end = time.time()
print('Detected Houses in {0:.1f} seconds'.format(end-start))

#Next, we crop out the houses
cropping_script = os.path.join(os.getcwd(),'2_Computer_Vision','Crop_Images.py')


cropping_result_file = os.path.join(Test_Folder,'Cropping_Results.csv') 


arglist = [['input_file',houses_result_file],['classes',houses_classes],['output_folder',Test_Folder],['output_file',cropping_result_file]]


call_string = ' '.join(['python', cropping_script,make_call_string(arglist)])

print('Cropping Houses Houses by calling \n', call_string)
start = time.time()
subprocess.call(call_string, shell=True)
end = time.time()
print('Cropped Houses in {0:.1f} seconds'.format(end-start))


# Next run the opening detector

model_folder =  os.path.join(data_folder,'Model_Weights')
opening_weights = os.path.join(model_folder,'Openings','trained_weights_final.h5')
opening_classes = os.path.join(model_folder,'Openings','data_all_classes.txt')
detector_script = os.path.join(os.getcwd(),'2_Computer_Vision','detector.py')
openings_result_file =  os.path.join(Test_Folder, 'Opening_Results.csv')

arglist = [['input_images',Test_Folder],['classes_file',opening_classes],['output',Test_Folder],['yolo_model',opening_weights],['box_file',openings_result_file]]
call_string = ' '.join(['python', detector_script,make_call_string(arglist)])

print('Detecting Openings by calling \n', call_string)
start = time.time()
subprocess.call(call_string, shell=True)
end = time.time()
print('Detected Openings in {0:.1f} seconds'.format(end-start))

#Finally run the classification

classifier_script = os.path.join(os.getcwd(),'3_Classification','Classifier.py')

level_folder =  os.path.join(data_folder,'Level_Detection_Results')
softness_score_file =  os.path.join(Test_Folder, 'Softness_Scores.csv')

arglist = [['output_file',softness_score_file],['input_file',openings_result_file],['level_folder',Test_Folder],['classes',opening_classes]]

call_string = ' '.join(['python', detector_script,make_call_string(arglist)])


print('Calculating Softness Scores by calling \n', call_string)
start = time.time()
subprocess.call(call_string, shell=True)
end = time.time()
print('Calculated Softness Scores in {0:.1f} seconds'.format(end-start))

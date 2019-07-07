import subprocess
call_string = 'python detector.py --detection_mode opening'
print('Calling', call_string)
subprocess.call(call_string, shell=True)
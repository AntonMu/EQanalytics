import os
import subprocess
import time
import sys

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_folder = os.path.join(root_folder, "Data")
model_folder = os.path.join(data_folder, "Model_Weights")

# First download the pre-trained weights
download_script = os.path.join(model_folder, "Download_Weights.py")

print("Downloading Pretrained Weights")
start = time.time()
call_string = " ".join(
    [
        "python",
        download_script,
        "1aPCwYXFAOmklmNMLMh81Yduw5UrbHqkN",
        os.path.join(model_folder, "Houses", "trained_weights_final.h5"),
    ]
)

subprocess.call(call_string, shell=True)

call_string = " ".join(
    [
        "python",
        download_script,
        "1FbvHzQWCjucXPbTbI4S1MnBLkAi58Mxv",
        os.path.join(model_folder, "Openings", "trained_weights_final.h5"),
    ]
)

subprocess.call(call_string, shell=True)
end = time.time()
print("Downloaded Pretrained Weights in {0:.1f} seconds".format(end - start))

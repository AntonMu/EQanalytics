Using TensorFlow backend.
WARNING:tensorflow:From /home/ubuntu/anaconda3/lib/python3.6/site-packages/tensorflow/python/framework/op_def_library.py:263: colocate_with (from tensorflow.python.framework.ops) is deprecated and will be removed in a future version.
Instructions for updating:
Colocations handled automatically by placer.
2019-06-28 06:48:52.533978: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
2019-06-28 06:48:52.540449: I tensorflow/core/platform/profile_utils/cpu_utils.cc:94] CPU Frequency: 2300065000 Hz
2019-06-28 06:48:52.541667: I tensorflow/compiler/xla/service/service.cc:150] XLA service 0x560dba201990 executing computations on platform Host. Devices:
2019-06-28 06:48:52.541698: I tensorflow/compiler/xla/service/service.cc:158]   StreamExecutor device (0): <undefined>, <undefined>
2019-06-28 06:48:52.626394: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:998] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2019-06-28 06:48:52.627123: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1433] Found device 0 with properties: 
name: Tesla K80 major: 3 minor: 7 memoryClockRate(GHz): 0.8235
pciBusID: 0000:00:1e.0
totalMemory: 11.17GiB freeMemory: 11.11GiB
2019-06-28 06:48:52.627159: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1512] Adding visible gpu devices: 0
2019-06-28 06:48:52.628285: I tensorflow/core/common_runtime/gpu/gpu_device.cc:984] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-06-28 06:48:52.628311: I tensorflow/core/common_runtime/gpu/gpu_device.cc:990]      0 
2019-06-28 06:48:52.628322: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1003] 0:   N 
2019-06-28 06:48:52.628901: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 10805 MB memory) -> physical GPU (device: 0, name: Tesla K80, pci bus id: 0000:00:1e.0, compute capability: 3.7)
2019-06-28 06:48:52.631694: I tensorflow/compiler/xla/service/service.cc:150] XLA service 0x560dba77bc50 executing computations on platform CUDA. Devices:
2019-06-28 06:48:52.631722: I tensorflow/compiler/xla/service/service.cc:158]   StreamExecutor device (0): Tesla K80, Compute Capability 3.7
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_59 due to mismatch in shape ((1, 1, 1024, 18) vs (255, 1024, 1, 1)).
  weight_values[i].shape))
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_59 due to mismatch in shape ((18,) vs (255,)).
  weight_values[i].shape))
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_67 due to mismatch in shape ((1, 1, 512, 18) vs (255, 512, 1, 1)).
  weight_values[i].shape))
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_67 due to mismatch in shape ((18,) vs (255,)).
  weight_values[i].shape))
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_75 due to mismatch in shape ((1, 1, 256, 18) vs (255, 256, 1, 1)).
  weight_values[i].shape))
/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/saving.py:1140: UserWarning: Skipping loading of weights for layer conv2d_75 due to mismatch in shape ((18,) vs (255,)).
  weight_values[i].shape))
Create YOLOv3 model with 9 anchors and 1 classes.
Load weights keras_yolo3/model_data/yolo.h5.
Freeze the first 249 layers of total 252 layers.
Train on 203 samples, val on 22 samples, with batch size 32.
Epoch 1/51
Traceback (most recent call last):
  File "train.py", line 196, in <module>
    _main()
  File "train.py", line 71, in _main
    callbacks=[logging, checkpoint])
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/legacy/interfaces.py", line 91, in wrapper
    return func(*args, **kwargs)
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/training.py", line 1418, in fit_generator
    initial_epoch=initial_epoch)
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/engine/training_generator.py", line 181, in fit_generator
    generator_output = next(output_generator)
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/utils/data_utils.py", line 709, in get
    six.reraise(*sys.exc_info())
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/six.py", line 693, in reraise
    raise value
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/utils/data_utils.py", line 685, in get
    inputs = self.queue.get(block=True).get()
  File "/home/ubuntu/anaconda3/lib/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
  File "/home/ubuntu/anaconda3/lib/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/keras/utils/data_utils.py", line 626, in next_sample
    return six.next(_SHARED_SEQUENCES[uid])
  File "train.py", line 181, in data_generator
    image, box = get_random_data(annotation_lines[i], input_shape, random=True)
  File "/home/ubuntu/logohunter/src/keras_yolo3/yolo3/utils.py", line 40, in get_random_data
    image = Image.open(line[0])
  File "/home/ubuntu/anaconda3/lib/python3.6/site-packages/PIL/Image.py", line 2580, in open
    fp = builtins.open(filename, "rb")
FileNotFoundError: [Errno 2] No such file or directory: '~/logohunter/data/houses/view_vulnerable_1561685165_10_3_1803+BROADWAY++SAN+FRANCISCO+Work-Complete-CFC-Issued.jpg'

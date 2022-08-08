# README of MNIST MODEL with Local Debug Version

## Summary
This is a local debug version of MNIST model that classifies hand-written digits.

## Input Generation
```python
import numpy as np
import json
img_shape = (28,28,1)
input_test =np.random.random_sample((1,) + img_shape)
input_test = input_test.tolist()
data = {'id': 0, 'data': input_test}

with open('input.json','w') as fp:
    json.dump(data,fp)
```

## How to change the import to ibm_wmla_client.redhare
Replace `from redhareapi import Kernel` with `from ibm_wmla_client.redhareapi import Kernel`

## How to run on local computer
The following input.json, model.json, and model weight(ex. mnist_model.h5) are required in the same folder.
```
.
├── local_debug_example
│   ├── README.md
│   ├── input.json
│   ├── kernel.py
│   ├── mnist_model.h5
│   └── model.json
```

```
cd wmla-python-client/examples/mnist_example/local_debug_example
python kernel.py
```

## Show test results

```
2022-08-08 13:17:22.240937: I kernel input: {"name": "mnisttest", "tag": "test", "weight_path": "mnist_model.h5", "runtime": "dlipy3", "kernel_path": "kernel.py", "schema_version": "1", "model_path": "/Users/kiyeonj/Projects/wmla/wmla-python-client/examples/mnist_example/mnist"}
2022-08-08 13:17:22.241207: I currect dir/Users/kiyeonj/Projects/wmla/wmla-python-client/examples/mnist_example/mnist
2022-08-08 13:17:22.266372: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX2 AVX512F AVX512_VNNI FMA
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
1/1 [==============================] - 0s 126ms/step
1/1 [==============================] - 0s 15ms/step
2022-08-08 13:17:22.558882: I Keras time : 0.037053823471069336 s
2022-08-08 13:17:22.558966: I >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
2022-08-08 13:17:22.559009: I on_task_invoke
1/1 [==============================] - 0s 15ms/step
Response data: {"key": 0, "data": [[-8.15404224395752, -15.543219566345215, 2.557469129562378, 7.9756245613098145, -21.370929718017578, 8.467974662780762, -3.259269952774048, -0.943429172039032, 1.4426156282424927, -3.821748733520508]]}
1/1 [==============================] - 0s 15ms/step
Response data: {"key": 0, "data": [[-8.15404224395752, -15.543219566345215, 2.557469129562378, 7.9756245613098145, -21.370929718017578, 8.467974662780762, -3.259269952774048, -0.943429172039032, 1.4426156282424927, -3.821748733520508]]}
1/1 [==============================] - 0s 16ms/step
Response data: {"key": 0, "data": [[-8.15404224395752, -15.543219566345215, 2.557469129562378, 7.9756245613098145, -21.370929718017578, 8.467974662780762, -3.259269952774048, -0.943429172039032, 1.4426156282424927, -3.821748733520508]]}
1/1 [==============================] - 0s 15ms/step
Response data: {"key": 0, "data": [[-8.15404224395752, -15.543219566345215, 2.557469129562378, 7.9756245613098145, -21.370929718017578, 8.467974662780762, -3.259269952774048, -0.943429172039032, 1.4426156282424927, -3.821748733520508]]}
1/1 [==============================] - 0s 14ms/step
Response data: {"key": 0, "data": [[-8.15404224395752, -15.543219566345215, 2.557469129562378, 7.9756245613098145, -21.370929718017578, 8.467974662780762, -3.259269952774048, -0.943429172039032, 1.4426156282424927, -3.821748733520508]]}
2022-08-08 13:17:22.754067: I exit on_task_invoke, using time 0.20
2022-08-08 13:17:22.754113: I <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
```



import numpy as np
import json
img_shape = (28,28,1)
input_test =np.random.random_sample((1,) + img_shape)
input_test = input_test.tolist()
data = {'id': 0, 'data': input_test}

with open('input.json','w') as fp:
    json.dump(data,fp)
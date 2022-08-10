# README of MNIST MODEL

## Summary

This is a MNIST model built with Keras that classifies hand-written digits.


## Input

* Input format: json
* Input body:

```
{
    "id" : 0,
    "data": list
}
```

## Output
* Output format: json
* Output body (if there is no error)
```
{
    'key': 0, 
    'data': [[-5.415988922119141, -17.939651489257812, 0.7941587567329407, 5.815486431121826, -24.95937728881836, 9.760404586791992, -0.9046012163162231, -1.0441383123397827, 1.9513847827911377, -3.5598299503326416]]
}
```

## Caller example


```python
img_shape = (28, 28, 1)
x_test = np.random.random_sample((1,) + img_shape)
x_test = x_test.tolist()

data = {'id': 0, 'data': x_test}

response = conn.run_inference(model_name, data)
```
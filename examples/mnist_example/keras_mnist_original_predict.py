import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np

(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)
def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label


ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = ds_test.batch(1)
ds_test = ds_test.cache()
ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

# def create_model():

#     model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(128, activation='relu'),
#     tf.keras.layers.Dense(10)
#     ])
#     model.compile(
#         optimizer=tf.keras.optimizers.Adam(0.001),
#         loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#         metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
#     )
#     return model

# mnist_model = create_model()
mnist_model = tf.keras.models.load_model('mnist_model.h5')


for example in ds_test.take(1):
    print(type(example))
    image, label = example
    print(image.shape)
    print(label)

img_shape = (28, 28, 1)
x_test = np.random.random_sample((1,) + img_shape)
print(x_test.shape)
l = np.random.random_sample(2,)
results = mnist_model.predict(x_test)
print(results)
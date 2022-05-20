import tensorflow as tf
from tensorflow import keras
import config
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import postprocessing

songLength = 600

def make_generator_model():
    model = tf.keras.Sequential()
    y = int(songLength/4)
    x = int(config.MIDI_NOTE_RANGE/4)
    model.add(layers.Dense(x*y*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((y, x, 256)))
    # assert model.output_shape == (None, 7, 7, 256)  # Note: None is the batch size

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    # assert model.output_shape == (None, 7, 7, 128)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(32, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    # assert model.output_shape == (None, songLength/2, midiNotes/2, 64)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))
    print(model.output_shape)
    assert model.output_shape == (None, songLength,config.MIDI_NOTE_RANGE, 1)

    return model

model = make_generator_model()

model_path = "models/gan_50_generator.h5"
model.load_weights(model_path)

noise = tf.random.normal([1, 100])
generated_image = model(noise, training=False)

# plt.imshow(generated_image[0, :, :, 0], cmap='gray')
# plt.show()

midi = postprocessing.vecToMidi(generated_image[0, :, :, 0])
midi.save("generated.mid")
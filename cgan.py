import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import preprocessing
import sys
data = preprocessing.loadData()

# convert to float for dl model
data = data.astype('float32')
plt.scatter(data[:,0], data[:, 1])

# convert your data into tensorflow data type.
train_data = tf.data.Dataset.from_tensor_slices(data)
train_data = train_data.batch(64).prefetch(32)

# discriminator model
def build_discriminator(n=2):
    inps = layers.Input(shape=(n,))
    x = layers.Dense(25, activation='relu', kernel_initializer='he_uniform')(inps)
    outs = layers.Dense(1)(x)
    model = keras.Model(inps, outs, name='discriminator')
    return model
# generator model
def build_generator(latent_dim=5):
    inps = layers.Input(shape=(latent_dim,))
    x = layers.Dense(25, activation='relu', kernel_initializer='he_uniform')(inps)
    outs = layers.Dense(2, activation='tanh')(x)
    model = keras.Model(inps, outs, name='generator')
    return model
discriminator = build_discriminator()
generator = build_generator()
print(discriminator.summary(), generator.summary())

class GAN(keras.Model):
    
    # initialize models with latent dimensions
    def __init__(self, disc, gen, latent_dim=5):
        super(GAN, self).__init__()
        self.discriminator = disc
        self.generator = gen
        self.latent_dim = latent_dim
  
    # compile with optimizers and loss function
    def compile(self, optD, optG, loss_fn):
        super(GAN, self).compile()
        self.optD = optD
        self.optG = optG
        self.loss_fn = loss_fn
    
    # custom training function
    def train_step(self, real_data):
        if isinstance(real_data, tuple):
            real_data = real_data[0]
    
        # get current batch size
        bs = tf.shape(real_data)[0]
        z = tf.random.normal(shape=(bs, self.latent_dim))
        fake_data = self.generator(z)
        
        # combine real and fake images in a single vector along with their labels
        combined_data = tf.concat([real_data, fake_data], axis=0)
        labels = tf.concat([tf.ones((bs, 1)), tf.zeros((bs, 1))], axis=0)
        
        # train your discriminator
        with tf.GradientTape() as tape:
            preds = self.discriminator(combined_data)
            d_loss = self.loss_fn(labels, preds)

        grads = tape.gradient(d_loss, self.discriminator.trainable_weights)
        self.optD.apply_gradients(zip(grads, self.discriminator.trainable_weights))
        
        # misleading labels for generator
        misleading_labels = tf.ones((bs, 1))
        z = tf.random.normal(shape=(bs, self.latent_dim))
        
        # train your generator
        with tf.GradientTape() as tape:
            fake_preds = self.discriminator(self.generator(z))
            g_loss = self.loss_fn(misleading_labels, fake_preds)
        grads = tape.gradient(g_loss, self.generator.trainable_weights)
        self.optG.apply_gradients(zip(grads, self.generator.trainable_weights))
        return {"d_loss": d_loss, "g_loss": g_loss}

# create GAN model using already built D and G
gan = GAN(discriminator, generator)
# compile your model with loss and optimizers
gan.compile(
    keras.optimizers.Adam(),
    keras.optimizers.Adam(),
    keras.losses.BinaryCrossentropy(from_logits=True)
)

def show_samples(epoch, generator, data, n=100, l_dim=5):
    # save results after every 20 epochs  
    if epoch % 20 == 0:
        z = tf.random.normal(shape=(n, l_dim))
        generated_data = generator(z)
        generated_points_list.append(generated_data)

# list for storing generated points
generated_points_list = []
# a lambda callback
cbk = keras.callbacks.LambdaCallback(on_epoch_end=lambda epoch,logs: show_samples(epoch, gan.generator, data))

# time your training
hist = gan.fit(train_data, epochs=5000, callbacks=[cbk], verbose=False)

# plot the results
plt.plot(hist.history['d_loss'], color='blue', label='disriminator loss')
plt.plot(hist.history['g_loss'], color='red', label='generator loss')
plt.xlabel('Epochs')
plt.ylabel('Losses')
plt.legend()
import numpy as np
import tensorflow.keras as k


class Autoencoder:
    
    def __init__(self, input_shape, conv_filters, conv_kernels, conv_strides, latent_space_dim):

        self.input_shape = input_shape
        self.conv_filters = conv_filters
        self.conv_kernels = conv_kernels
        self.conv_strides = conv_strides
        self.latent_space_dim = latent_space_dim
        
        self.encoder = None
        self.decoder = None
        self.model = None
        
        self.num_conv_layers = len(conv_filters)
        self.shape_before_bottleneck = None
        
        self._build()

    
    def summary(self):
        self.encoder.summary()
    
    def _build(self):
        self._build_encoder()
        #self._build_decoder()
        #self._build_autoencoder()
        
    
    def _build_encoder(self):
        encoder_input = self._add_encoder_input()
        conv_layers = self._add_conv_layers(encoder_input)
        bottleneck = self._add_bottleneck(conv_layers)
        self.encoder = k.Model(encoder_input, bottleneck, name = "encoder")
        
        
    def _add_encoder_input(self):
        return k.layers.Input(shape=self.input_shape, name="encoder_input")
    
    
    def _add_conv_layers(self, encoder_input):
        x = encoder_input
        for i in range(self.num_conv_layers):
            x = self._add_conv_layer(i, x)
        return x
    
    
    def _add_conv_layer(self, layer_index, x):
        "Add a convolutional layer consisting of: Conv2D + ReLU + batch normalization"
        
        layer_number = layer_index + 1 # I do not want to have layer 0
        
        conv_layer = k.layers.Conv2D(
            filters = self.conv_filters[layer_index], 
            kernel_size = self.conv_kernels[layer_index],
            strides = self.conv_strides[layer_index],
            padding = 'same',
            activation=k.activations.relu,
            name = "encoder_conv_layer_number_{}".format(layer_number))
        
        x = conv_layer(x)
        x = k.layers.BatchNormalization(name = "encoder_batch_norm_layer_number_{}".format(layer_number))(x)
        
        return x
    
    def _add_bottleneck(self, x):
        "Flatten data and add a bottleneck (Dense layer)"
        self.shape_before_bottleneck = k.backend.int_shape(x)[1:] #store the shape before flatten, because it will be useful for building decoder
        x = k.layers.Flatten()(x)
        x = k.layers.Dense(self.latent_space_dim, name = "encoder_output")(x)
        return x
        

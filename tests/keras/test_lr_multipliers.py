from __future__ import print_function
import pytest
import numpy as np
from keras.utils.test_utils import get_test_data
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
import keras.layers
import keras.optimizers


seed = 42


def test_learning_rate_multipliers_dense():
    '''
    Test learning rate multipliers on Dense layers
    '''
    (X_train, y_train), (X_test, y_test) = get_test_data(nb_train=10,
                                                         nb_test=1,
                                                         input_shape=(4,),
                                                         classification=True,
                                                         nb_class=2)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    np.random.seed(seed)
    model0 = Sequential()
    model0.add(keras.layers.Dense(output_dim=5, input_dim=4, activation='relu'))
    model0.add(keras.layers.Dense(output_dim=2, activation='softmax'))
    model0.compile(loss='categorical_crossentropy', optimizer='sgd')
    (m0w0_ini,m0b0_ini) = model0.layers[0].get_weights()
    (m0w1_ini,m0b1_ini) = model0.layers[1].get_weights()
    model0.train_on_batch(X_train, y_train)
    (m0w0_end,m0b0_end) = model0.layers[0].get_weights() 
    (m0w1_end,m0b1_end) = model0.layers[1].get_weights()
    
    np.random.seed(seed)
    model1 = Sequential()
    model1.add(keras.layers.Dense(output_dim=5, input_dim=4, activation='relu',
                                  W_learning_rate_multiplier=0.0, b_learning_rate_multiplier=0.0))
    model1.add(keras.layers.Dense(output_dim=2, activation='softmax',
                                  W_learning_rate_multiplier=0.5, b_learning_rate_multiplier=0.5))
    model1.compile(loss='categorical_crossentropy', optimizer='sgd')
    (m1w0_ini,m1b0_ini) = model1.layers[0].get_weights()
    (m1w1_ini,m1b1_ini) = model1.layers[1].get_weights()
    model1.train_on_batch(X_train, y_train)
    (m1w0_end,m1b0_end) = model1.layers[0].get_weights() 
    (m1w1_end,m1b1_end) = model1.layers[1].get_weights()

    # This should be ~0.0 
    np.testing.assert_almost_equal(np.mean((m1w0_end - m1w0_ini)), 0.0, decimal=2)
    np.testing.assert_almost_equal(np.mean((m1b0_end - m1b0_ini)), 0.0, decimal=2)

    # This should be ~0.5
    np.testing.assert_almost_equal(np.mean((m1w1_end - m1w1_ini)/(m0w1_end - m0w1_ini)), 0.5, decimal=2)
    np.testing.assert_almost_equal(np.mean((m1b1_end - m1b1_ini)/(m0b1_end - m0b1_ini)), 0.5, decimal=2)


def test_learning_rate_multipliers_conv():
    '''
    Test learning rate multipliers on Convolutional layers
    '''

    np.random.seed(seed)
    X_train = np.random.rand(10,3,10,10)
    y_train = np.random.rand(10,1,6,6)

    np.random.seed(seed)
    model0 = Sequential()
    model0.add(keras.layers.Convolution2D(5,3,3,
                                          input_shape=(3,10,10), 
                                          border_mode='valid', 
                                          activation='relu'))
    model0.add(keras.layers.Convolution2D(1,3,3,
                                          border_mode='valid'))
    model0.compile(loss='mse', optimizer='sgd')
    (m0w0_ini,m0b0_ini) = model0.layers[0].get_weights()
    (m0w1_ini,m0b1_ini) = model0.layers[1].get_weights()
    model0.train_on_batch(X_train, y_train)
    (m0w0_end,m0b0_end) = model0.layers[0].get_weights() 
    (m0w1_end,m0b1_end) = model0.layers[1].get_weights()

    np.random.seed(seed)
    model1 = Sequential()
    model1.add(keras.layers.Convolution2D(5,3,3,
                                          input_shape=(3,10,10), 
                                          border_mode='valid', 
                                          W_learning_rate_multiplier=0.0, b_learning_rate_multiplier=0.0,
                                          activation='relu'))
    model1.add(keras.layers.Convolution2D(1,3,3,
                                          W_learning_rate_multiplier=0.5, b_learning_rate_multiplier=0.5,
                                          border_mode='valid'))
    model1.compile(loss='mse', optimizer='sgd')
    (m1w0_ini,m1b0_ini) = model1.layers[0].get_weights()
    (m1w1_ini,m1b1_ini) = model1.layers[1].get_weights()
    model1.train_on_batch(X_train, y_train)
    (m1w0_end,m1b0_end) = model1.layers[0].get_weights() 
    (m1w1_end,m1b1_end) = model1.layers[1].get_weights()

    # This should be ~0.0
    np.testing.assert_almost_equal(np.mean((m1w0_end - m1w0_ini)), 0.0, decimal=2)
    np.testing.assert_almost_equal(np.mean((m1b0_end - m1b0_ini)), 0.0, decimal=2)

    # This should be ~0.5
    np.testing.assert_almost_equal(np.mean((m1w1_end - m1w1_ini)/(m0w1_end - m0w1_ini)), 0.5, decimal=2)
    np.testing.assert_almost_equal(np.mean((m1b1_end - m1b1_ini)/(m0b1_end - m0b1_ini)), 0.5, decimal=2)


if __name__ == '__main__':
    pytest.main([__file__])

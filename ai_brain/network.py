import torch.nn as nn
import torch.nn.functional as F
import tensorflow as tf

# >Creating the architecture of the Neural Network (our NN is a class)
#
#   >nn.Module = (using inheritance)
#   >we inherit the attributes and functions of the parent class Module

'''
>>> nn.Module = Base class for all neural network modules.
>>> Your models should also subclass this class. 
'''


'''    
    'init' will contain the following:
    
     1) 5 input neurons = 5 dimensions of the encoded vector of input state (3 signals, orientation and -orientation)
     2) one output layer = move that the AI will take
     3) hidden layers
     4) self = object that is going to be created from this class
     5) nb_action (corresponds to the output layer) = the three actions (left, right, straight)

     >>> self.[something] = variable attached to the object
'''


class Network(nn.Module):

    def __init__(self, input_layer, action):
        # self.conv1 = nn.Conv2d(1, 20, 5) # Module documentation
        # self.conv2 = nn.Conv2d(20, 20, 5) # Module documentation

        super(Network, self).__init__()  # basic initialization given that we need to use nn.Module
        self.input_layer = input_layer  # input/output neurons
        self.hidden_layer1 = 32
        self.hidden_layer2 = 64
        self.hidden_layer = 128
        self.action = action

        # Linear = linear FUNCTION to connect all the NODES from the layer1 to the layer2/
        # second argument '30' = number of neurons we want to have in the second layer
        self.first_conn = nn.Linear(self.input_layer,
                                             self.hidden_layer)  # input/hidden layer conn

        self.second_conn = nn.Linear(self.hidden_layer,
                                             self.action)  # hidden/output layer conn

    # gets states => returns Q-val
    # state = 5-tuple of (3 sensors, or, -or)
    def forward(self, state):

        x = F.relu(self.first_conn(state))  # Module documentation
        #  return F.relu(self.conv2(x)) # Module documentation

        '''
         >> 'forward' function ACTIVATES the neurons in the neural network (signals)
         >> we will use a RECTIFIER FUNCTION because we do not have linear values (rectify = breaking the linearity)'''

        x = F.relu(self.first_conn(state))  # x = hidden neurons

        '''we DO NOT NEED output neurons, we need Q VALUES (we are using Deep Q Learning)
        q_value = OUTPUT NEURONS (but Q values basically)
        using a SOFTMAX (and q_value) we can get the desired action
        x = LEFT side of the connection (basically the 'x' that we calculated above) '''
        # self.second_conn.bfloat16(self)
        # self.second_conn = tf.keras.layers.Dense(32, activation=tf.keras.activations.softmax)
        #  model.add(tf.keras.layers.Dense(units=num_classes, activation=tf.nn.softmax))
        #  model.compile(optimizer=keras.optimizers.Adam(), loss=keras.losses.categorical_crossentropy,
        #              metrics=['accuracy'])
        #  hist = model.fit(x_train_nn, y_train_nn, batch_size=batch_size, epochs=epochs,
        #                 validation_data=(x_test_nn, y_test_nn))
        Q_val = self.second_conn(x)
        return Q_val

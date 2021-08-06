# Self Driving 2D Car using Neuronal Networks

<img alt="This Project" width="650px" src="https://media1.giphy.com/media/pEFZpjHViGS5oPgafQ/giphy.gif?cid=790b76116f137695cee9dbed09df2392cdff4277249330c2&rid=giphy.gif&ct=g" />

Installation
-
1) (unpack the pip freeze environment) \
   __pip install -r requirements.txt__
2) Run _run.py_



# Documentation

![image](https://user-images.githubusercontent.com/73531247/124481054-2b8f7c00-dda8-11eb-9a74-bbe5c5e12251.png)


## Workflow

Network) 
   - Make a nn.Module instance
   - input layer, hidden layer1+2, output layer, action
   - first_connection, second_connection (both linear, between consecutive layers)
     (these RELU functions activate the neurons)
   - **forward()** = gets states, activate the neurons, returns Q-val ( using RELU and second_connection(x) )


 
Experience Replay)
![image](https://user-images.githubusercontent.com/73531247/124481395-832de780-dda8-11eb-91d9-ccee8da508e6.png)
    - get 100 random states out of 100k memory states
    
DQN)
   - its objects are learning _models_
   - **last_state** = input_layer + 1 dimension = TENSOR(input_layer).unsqueeze(0) <- add a fake dim
   - the network is based on learning models which take the input (input_layer, action, gamma)
   - _learn( batch_state, batch_next_state, batch_reward, batch_action )_ : 
      >> Get the output of the input state (model.gather on dim 1 <- action dim)
      >> Get the max Q-val of next_output with detach
      >> calculate target, apply loss, optimizer, backpropagation, reinit. the optimizer
   - _update_( reward, new_signal )
      >> new_state given new_signal (with unsqueeze(0))
      >> push it into memory
      >> get action
      >> update reward window and calculate the score


## Algorithms used:
- Artificial, Convolutional and Recurrent Neuronal Networks
- Deep Q-Learning
- Markov Action Selection Policy
- Stochastic Gradient Descent for Weight Adjustments
- Backpropagation (Loss comparison between current and last state)
- RELU's, Softmax, Reward Mechanism
(underlying game made in pygame)

## Class 'dqn'

# Variables
- the **input of the NN** are the STATES encoded in the VECTOR of 5 dimensions (3 sign, orient, -orient)
- **state** = VECTOR of 5-tuple (fake dim, last state, new state, last action, last reward)
- **tensor** = an ARRAY with a **gradient** (which needs one more dimension - for the batch size)
- we use _tensors_ because the Network only **takes batches, not arrays*
- **last_state** = BATCH TENSOR with 1)input_layer & 2)a fake dimension
        self.last_state = torch.Tensor(input_layer).unsqueeze(0)
        (**unsqueeze**: returns a new tensor with a dimension added at position 'n') \
        _>>> torch.unsqueeze(x, 0) \
         tensor([[ 1,  2,  3,  4]]) \
         >>> torch.unsqueeze(x, 1) \
         tensor([[ 1], \
               [ 2], \
               [ 3], \
               [4]])

- **gamma** = discount factor
- **model** = instance object of class Network(input_layer, action)
- **memory** = instance object of class ReplayMemory(100000) <- 100k transitions = 100k states (5-tuples) 
- **actions** = either 0/1/2 referring to 0, 20, -20 
- **orientation** = either 0, 20, -20

# select_action()
- **Softmax** - we get an action (give a Q value outputted by our NN) \
  one Q-value for each action (left, straight, right) \
         SOFTMAX = choose the best action to play, while also experimenting the other possible actions \
       SOFTMAX = distribution of probabilities for each the Q-values & Q-state action \
       Softmax => assigns the biggest prob. to the highest Q-value \
       
- **1 state => 3 actions** => 3 Q-values: Q-state action1, Q-state action2, Q-state action3 \
       With these 3 Q-values we will generate a distribution of probabilities \
       One prob. for one q-value \
       
- **temp** gives the certainty quotient
- **multinomial** gets 'n' random pytorch tensors


## Training the Neuronal Network
      ----------------------------------
      TRAINING THE DEEP NEURONAL NETWORK
      ----------------------------------
     
      Approach:
      > forward propagation
      > after, backpropagation
      > get the OUTPUT and TARGET
      > COMPARE the output to target and get the last error
      > BACK-PROPAGATE the last error into the neuronal network
      > use stochastic GRADIENT DESCENT to UPDATE the WEIGHTS according to how much they contributed to the last error
     
      > We take it into BATCHES because a transition is a
       tuple of 5 elements: first fake dimension, current state, next state, current reward, current action
   
      > We use this because with simple consecutive transitions, the model would not learn anything
      > with the current state vs. next state => we compute the LOSS
      
# learn()

**outputs = self.model(batch_state).gather(1, batch_action.unsqueeze(1)).squeeze(1)**
- we need the output of the input state
- => we get the MODEL output of the input state (not the model, but the output)
- after, we only extract theh action 
- (batch_action) does NOT have a fake dimension, as batch_state does
- unsqueeze(1) = dim of action, unsqueeze(0) = fake dimension of the state
- **.gather(dim,index)
- 2D array -> dim=0 is rows, dim=1 is columns
- 3D array -> dim=0 is image, dim=1 is rows, dim=2 is columns
- **index** -> index _tensor_ corresponding to the values in the value _tensor_
- **unsqueeze** - mentioned above
- **squeeze(n)** - returns a tensor with all dimension of input of size 'n' removed
- squeeze(1) = we kill the batch as we want the result in an array (we do not work with batches anymore)

--------------------------------------
**next_outputs = self.model(batch_next_state).detach().max(1)[0]**
- we calculate next_state because we need to compute the target
- like in the max (with 'a' underneath)
- next_output = maximum of values for next_state given all possible actions (the 'a' under max)
- batch_next_state = all the states in all the transitions taken from a sample
- we 'detach' it to take all the results, in order to apply the max function
- the index (1) from max(1)[0] = index of action
- the index [0] from max(1)[0] = index corresponding to the state (of next state)
- result = we get the maximum of the Q-values of the next state represented by the index zero according
to all the actions that are represented by the action with index 1

**target = reward + gamma * (max Q-value of the next state, according to the action)**
td_loss = F.smooth_l1_loss(outputs, target)
td_loss.backward(retain_graph=True) and self.optimizer.step() <- reinitialize the optimizer after every iteration
------------------------------
## update(self, reward, new_signal)
- unsqueeze(0) = add the FAKE dimension to the first position
- new_state = torch.Tensor(new_signal).float().unsqueeze(0)
**action = self.select_action(new_state)**


## Class Network

- Inherits from torch.nn.Module
- has a constructor __init__ to which we assign the values of the NN (such as number of neurons, layers, reward windows etc.)
- 
- td = temporal difference
- outputs = predictions
- target = the target computed above
- self.first_conn = nn.Linear(self.input_layer, self.hidden_layer)  # input/hidden layer linear connection (connects all neurons between 2 layers)

**forward()**
- x = F.relu(self.first_conn(state))  # Module documentation
- >> 'forward' function ACTIVATES the neurons in the neural network (signals)
  >> we will use a RECTIFIER FUNCTION because we do not have linear values (rectify = breaking the linearity)'''
- Q_val = self.second_conn(x)

**sample()**
    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)
        
             >>> map(function, object_to_apply_the_function_to)
             
             1) lambda functions will convert (all) our samples into a TORCH variable         
             2) variable = convert from torch to a variable that will contain the tensor and the gradient
             3) For each BATCH (that is contained in a sample)
                => we concatenate (CAT) each batch with respect to the first dimension
            
             4) we do this to align the (for each row) state, action, reward for every time 't'
             5) 0 = first dimension

             We return a list of batches, where every element is a PYTORCH VARIABLE  
             
## Experience Replay

- The agent learns only using long time correlations, not one time stamps. The states need to be independent from one another => we will implement MARKOV DP (as it uses independent states)

'''
 Steps:
 1) We create a memory of these 100 states (Transitions)
 2) We sample these states (we take random batches of these 100 transitions to make our next update)
'''

>>> It will grow until 10k events and it will remain at that value
>>> => We delete the first element (rolling window)

![image](https://user-images.githubusercontent.com/73531247/124480940-0f8bda80-dda8-11eb-841f-6231c87f10e8.png)
![image](https://user-images.githubusercontent.com/73531247/124481017-22061400-dda8-11eb-92d2-06f04c4d7e1f.png)


## Genomes and NEAT algorithm
- Bored right now, may do this later

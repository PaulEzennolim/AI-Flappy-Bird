AI Flappy Bird

Project overview:

This project implements a Flappy Bird game enhanced with an AI that learns to play the game efficiently. The AI uses the 
NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve and improve its performance over successive generations.

Extra information about the config_feedfoward.txt file:

fitness_criterion: is a parameter that allows us to specify the method for determining the "best" birds within the 
population. This criterion can be set to either min, max, or mean. When set to max, for example, the algorithm 
selects birds with the highest fitness scores as the best performers. These birds are prioritized for breeding in 
subsequent generations, while those with lower fitness scores are typically removed from the population. This approach 
ensures that the genetic material of the highest-performing individuals is passed on, gradually improving the overall 
fitness of the population over successive generations.

fitness_threshold: represents the fitness level that, once achieved by any bird in the population, triggers the 
termination of the program. For instance, if a bird achieves a fitness level of 100, it indicates that it has reached 
a sufficient performance level. At this point, further generations may not be necessary because the program's objective 
has been adequately fulfilled. Therefore, whenever a bird's fitness level meets or exceeds the fitness_threshold, the 
program will halt its execution. This ensures that the algorithm stops once it achieves satisfactory performance, 
preventing unnecessary computation.

NEAT (NeuroEvolution of Augmenting Topologies) categorizes the diverse architectures of bird populations into distinct species. 
For instance, birds featuring unconventional traits like 2 or 3 hidden layers or unusual nodes form one species, while those 
conforming to a standard structure of 3 nodes and one output neuron constitute another species. Setting reset_on_extinction = 
False indicates that if a species becomes extinct during the evolution process, the algorithm will not introduce a new population 
to replace it. This approach maintains the existing population structure without introducing new variations after species 
extinction.

NEAT treats all members of the population as genomes, each with its own set of properties such as nodes and genes. 
Nodes represent both input and output points within the neural network, while genes denote the connections linking 
these nodes. The DefaultGenome defines the initial blueprint for every genome in the population. This means that each 
bird in the population starts with predefined values for activation_default, activation_mutate_rate, and 
activation_options. These settings establish the starting conditions for how activation functions are assigned and 
mutated during the evolutionary process.

activation_mutate_rate: determines the likelihood of randomly changing the activation function for nodes in the neural 
network. For instance, setting activation_mutate_rate to 0.1 means that there is a 10% chance that whenever a new 
population member is created, its activation functions will be randomly altered to a different type. This mutation 
allows for exploration of different activation functions across generations, enhancing the evolutionary process of 
neural networks.

activation_options: specifies the range of activation functions available for selection when activation_mutate_rate 
triggers a mutation. It defines the pool from which activation functions can be randomly chosen during the evolution 
of neural networks. For example, if activation_options includes options like 'tanh', 'relu', and 'sigmoid', then these 
functions are candidates for activation function mutation based on the specified mutation rate. This flexibility allows 
the neural network's architecture to explore various activation functions, thereby enhancing its adaptability and 
performance in evolving environments.

bias_max_value and bias_min_value: determine the allowable range for bias values in the initial setup of neural 
networks. These values specify the maximum and minimum biases that can be randomly assigned to nodes when creating 
the networks. For instance, setting bias_max_value to 30.0 and bias_min_value to -30.0 ensures that biases across the 
network fall within this range during initialization. This randomness in bias assignment helps in exploring different 
configurations and initial conditions for neural networks, which can influence their performance and adaptability in 
various tasks and environments. bias_mutate_power: This parameter controls the magnitude of change that can occur to 
biases during mutation. A higher value increases the potential range of change, allowing biases to vary more 
significantly between generations. bias_mutate_rate: This parameter defines the probability that biases will undergo 
mutation during the breeding process. For example, a rate of 0.7 indicates a 70% chance that biases will be mutated 
when creating new individuals in the population. Together, these parameters influence how biases evolve over successive
generations, affecting the diversity and optimization of neural networks in NEAT algorithms. Adjusting these values can
impact the exploration-exploitation balance, determining how much and how often biases are modified to potentially
improve performance in solving complex tasks.

max_stagnation: determines the maximum number of consecutive generations in NEAT where no improvement in fitness is 
observed before a species is considered stagnant and potentially removed from the population. For instance, 
if max_stagnation = 20, it means that if there are 20 consecutive generations where the fitness of the best-performing 
individuals (birds) within a species does not increase, that species will be identified as stagnant. Stagnant species 
are typically subject to removal or reinitialization in order to foster diversity and promote the discovery of better 
solutions through evolution. This mechanism helps NEAT algorithms maintain evolutionary progress by preventing the
persistence of ineffective or suboptimal genetic lineages, encouraging the exploration of new genetic combinations and 
network architectures that may lead to improved performance on the given task.

This explanation aims to give you a better understanding of the config_feedforward.txt file and the overall project.

Thank you for taking the time to check out this project! Your interest and support mean the world to me.

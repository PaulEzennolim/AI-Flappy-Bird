# AI Flappy Bird

## Project Overview

This project features a Flappy Bird game enhanced with an AI that learns to play using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The AI evolves its performance across generations, improving its ability to navigate obstacles.

## Requirements

* Pygame: For game visuals and interactions.

* NEAT-Python: For implementing the NEAT algorithm.

## Setup and Installation

1. Open a command prompt/terminal.

2. Run:

pip install pygame

pip install neat-python

## Understanding the NEAT Algorithm

NEAT Documentation: https://neat-python.readthedocs.io/en/latest/config_file.html

NEAT Article: https://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf

## Configuration Details

* fitness_criterion: Defines how the best birds are selected based on their fitness scores (e.g., max, mean). Higher scores prioritize certain birds for breeding.

* fitness_threshold: The fitness level that, when reached, ends the simulation, indicating a successful performance.

* Species Management:

  * NEAT categorizes birds into species based on network architecture.

  * reset_on_extinction: If False, does not replace extinct species, maintaining current population diversity.

* Genome Configuration:

  * activation_mutate_rate: Probability of mutating activation functions in nodes.
  * activation_options: Pool of activation functions available for mutation.
  * bias_max_value & bias_min_value: Range for initial bias values.
  * bias_mutate_power: Scale of bias changes during mutation.
  * bias_mutate_rate: Likelihood of bias mutation during reproduction.
  * max_stagnation: Maximum generations without fitness improvement before a species is considered stagnant.

This setup encourages exploration and prevents stagnation by promoting diversity in genetic traits and network structures.

Thank you for taking the time to check out this project! Your interest and support mean the world to me.
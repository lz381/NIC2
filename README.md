# Goal Saving Virutal Creature

## Table of Contents
* [General Info](#general-info)
* [Installation Instructions](#installation)
* [Usage](#usage)
* [Technologies](#technologies)

## General Info
This is an evolutionary algorithm (EA) that aims to train a robot to save goals and produce an 'optimised' robot. This can then be tested against a testbench of randomly generated shots to evaluate its generalisability. The simulator used is [Pyrosim](https://github.com/ccappelle/pyrosim). For more information on pyrosim, documentation is available [here](https://ccappelle.github.io/pyrosim).

The project is broken down into 2 main parts:

- Training using our developed genetic algorithm to produce a robot
- Testing against randomly generated shots (i.e. not in the training) to test for overfitting


## Installation

Only linux and Mac OS machines are currently supported.

Slight changes have been made to the source of one file to alter the behaviour of a particular sensor used in the simulations.

Please follow the installation instructions for pyrosim [here](https://github.com/ccappelle/pyrosim). Please be aware that the 'raysensor.cpp' file must be modified before running :
```sh
$ sh build.sh
```
If pyrosim has been installed before altering the source code, you must first uninstall it, change the code and then rebuild it, and finally reinstall.

If using a windows machine, it is recommended to use a virtual machine to run linux and follow the instructions for linux based systems. Although this will increase runtimes considerably, this has been the most consistent method found so far. 

After successfully installing pyrosim with the updated .cpp file, clone this repository and continue onto the Usage section. 

## Usage

The main genetic algorithm can be run through ```ga.py```, which will print out the generation number and the fitness values of that generation in a list. The number of generations can be set in ```constants.py```, along with various other parameters including:

- Evaluation time of each simulation
- Population size
- Number of environments for each individual to be trained in (1 <= n <= 10)
- Enabling a slightly faster vectorised mutation function
- Elistism rate 
- Which fitness function should be used 
- The seed to be used for both the python random library and numpy random library
- Enabling crossover
- Enabling adaptive mutation

Running ```ga.py``` will also produce six files, as csv containing the fitness values of every individual in each generation as well as the ID of the original parent of that solution, created in generation zero. There will also be five .p files which are pickle binary dumps of the best robot in various generations throughout the whole runtime of the genetic algorithm. Specifying the filename of the robot you wish to view in ```playback.py``` and running will replay that specific simulation.

To test a solution saved in a pickle file against randomly generated shots, run the ```run_testbench.py``` file from the command line in the following format:
```sh
$ python run_testbench.py <PICKLE_FILENAME.p> <NUMBER OF TRIALS> <NUMBER OF SHOTS>
```
If no arguments are defined for the number of trails and shots, they are set to 10 and 100, respectively, by default. Running will output a list of average scores in each trial. Generally, results tending towards 1000 perform better than those tending towards 0. 

It is useful to note that:

- Fitness functions and mutation function are defined in ```individual.py```
- Robot morphology and neuron allocation is in ```robot.py```
- Training environemnts are in ```environment.py```
- Tournament selection and elistism are found in ```population.py```

## Technologies
- Python 3.6+
- Pyrosim
- C++



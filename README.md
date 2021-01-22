# Using a genetic algorithm as a gameplay mechanic to play Chrome Dino game🦖
 
### In the game, we implemented our own genetic algorithm which mimics the process of natural evolution that is selection, mutation and crossover. In the framework, the population of Dino evolves iteratively in each generation to increase the fitness of Dino to jump over all the cacti.

### Information

Technical documentation of this project is available at url:   https://github.com/prakharsdev/ChromeDino/blob/master/UsingGeneticAlgorithmAsAGamePlayMechanicToPayChromeDinoGame.pdf

### Environment

```
python=3.8 is used
```

### Requirements
```
pip install -r requirements.txt
```

### Execution (approach 1)

Once you clone the repo, you can execute `ChromeDino` using below command

```
python GeneticChromeDino.py
```

### Execution logs (approach 1)

Can be found in file executionlog.txt


### Execution (approach 2: NEAT Algorithm)
To bring some intelligence in the game, NEAT Algroithm is used. For the algorithm implementation, [NEAT-Python](https://neat-python.readthedocs.io/en/latest/index.html) library is used. To try out A.I. learning to play the game, run a command
```
python NEATChromeDino.py
```
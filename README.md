# Learning_GA

### Work in Progress
pathfinder:
  main.py is a simple path finding genetic algorithm
  needs:
    - pygame
car:
  main.py starts the graphics
  only renders every 10th generation
  needs:
    - pygame
    - box2d
    - objgraph

Written in python 3.6
## Three Branches
- main
  - contains initial attempt that uses single parent and complete random replacement during mutation stage
- two_parent
  - expands to include two parents using uniform crossover
- addative_method
  - uses code from two_parent
  - changes mutations to simply subtract or add a small amount to gene rather than randomly override

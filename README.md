# Learning_GA

### Work in Progress

main.py is a simple path finding genetic algorithm

basicGA.py contains a prototype genetic algorithm that solves for the binary number 11111b

## Three Branches
- main
  - contains initial attempt that uses single parent and complete random replacement during mutation stage
- two_parent
  - expands to include two parents using uniform crossover
- addative_method
  - uses code from two_parent
  - changes mutations to simply subtract or add a small amount to gene rather than randomly override

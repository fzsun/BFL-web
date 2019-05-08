# Modules

* s_bfl.py: module for sorghum-bfl model
* s_bfl_utility.py: various utilities for s_bfl
* tsp.py: a traveling salesman problem module

# Usage

## TSP

In Python
```python
from tsp import tsp
my_tsp = tsp()
my_tsp.from_num_cities(3)
my_tsp.solve()
print(my_tsp.all_data_)
```

## s_bfl

In cmd (terminal), read CLI usage
```sh
$ python s_bfl.py -h
usage: s_bfl.py [-h] [--jit] [-t T] [--seed S] [-o O] input_file sysnum
...
```
Run an example
```sh
$ python s_bfl.py example_input.yaml 9 -o example_output.yaml
```

In Python
```python
from s_bfl import s_bfl
output = s_bfl('example_input.yaml', 9, out_file='example_output.yaml')
print(output)
```
Note, important functions are documented in code.



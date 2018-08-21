# BFL-web
A Flask-based web application for BFL

# Installation

Install Anaconda Python 3.5 version at https://www.anaconda.com/download/

Install the latest Gurobi, follow the instruction at http://www.gurobi.com/downloads/get-anaconda
Or use command

```
conda config --add channels http://conda.anaconda.org/gurobi
conda install gurobi
```

Install Flask and Waitress
```
conda install flask waitress
```

# Usage

For development, `cd` to the project folder, then use `python myapp.py` to start the server.

A Waitress production server can be started by `python production.py`.


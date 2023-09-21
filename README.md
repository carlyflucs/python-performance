# Python Performance
This repository contains code used for a demonstration of different python 
performance improvement techniques on a simulation/highly iterative class.

## Models ##
The "model" folder contains different versions of a simulated shopping trip
where the user is shopping for a list of items with a chance to
- find the item
- reach the item on the shelf
- be blocked waiting behind a granny or grandpa
and a time duration picked from a normal distribution for the time taken to
find the item and any wait time.

### Versions ###
Each version introduces a new optimisation technique
Simulations can be run with the simulate.py script.
To run v0 the command would be:
`python3 -m simulate v0`

The profile_v0.sh file will run the simulation with profiling and create a 
flamegraph of the results using flameprof

## Setting up a virtual environment ###
You can set up a virtual environment with the required dependencies with the below steps.
### Create the virtual environment
`python3 -m venv env`

### Activate the virtual environment
`source env/bin/activate`

### Install the latest pip
`python3 -m pip install --upgrade pip`

### Install our required dependencies
`python3 -m pip install -r requirements.txt`

Then use the following commend to activate the virtual environment
`source env/bin/activate`
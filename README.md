# Octopus AI Workshop edition

This branch is intended to be used for learning. It contains unfinished code that you will need to write to make it usable. 
Working finished version are to be found in the *finished* branch (might not exist yet) 
 

## Requirements
- Docker version ~ 18.09
- Docker-compose version ~ 1.21
- *Preferably a type of bash shell and some basic Linux programs like wget, unzip*  

## Usage
1. Clone this repository
2. Launch `init.sh` to download the models' weights and time-series data _or_ [download them manually](#manual-data-and-models-download) 
3. Run `docker-compose up -d`
4. Run `docker-compose ps` and make sure that all the containers are Up   
5. Run `docker-compose logs control` and find the token provided by the jupyter
6. Open `localhost:8888` and copy the token there
7. Experiment!


## Testing
**test.ipynb** was created for testing purposes. To open it, complete the steps above and then run all the cells in this notebook.  
If no errors were encountered, the project was set up properly. Tensorflow Warnings are fine.

## Manual data and models download
The project contains a number of different models and one data source.  
* You can download the data by following the link [here](https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip)   
For the system to work properly you will need to create the folder **data** and extract the contents of the zip archive there   
* Models' weights will be downloadable later  
// _Contents of this archive should be placed inside of the **models** folder that you will need to also create_ // 

## Launching the electricity control package
1. Run `docker exec -ti octopus_ws_emitter python emitter_main.py` in a separate terminal
2. Run `docker exec -ti octopus_ws_control python control_main.py` in a separate terminal

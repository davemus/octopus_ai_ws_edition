#!/usr/bin/env bash
mkdir -p data
mkdir -p models
wget "https://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip" -O ./data/household_power_consumption.zip
unzip -d data data/household_power_consumption.zip
rm data/household_power_consumption.zip
#wget "asd" -O models/models.zip
#unzip -d models models/models.zip
#rm models/models.zip

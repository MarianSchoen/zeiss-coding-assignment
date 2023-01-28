# written by Marian Schoen 

# This script is used to extract the zip file, and investigate both data sets. 
# There are a some informative console + pdf outputs. 
# All information gained from this script is reported in the Readme

import os, sys
from zipfile import ZipFile
from functions import read_clg_data

# Part 1: extract the zip file, handle a potentially missing file, and fix repository structure
# (this has been copy n pasted into the 'src/funtions.py')

if os.path.exists("data"): 
    folder = "./data/"
else: 
    folder = "../data/"

file = "DataScienceCodingChallenge.zip"
path = folder + file 

if os.path.isfile(path): 
    file_handler = ZipFile(path, "r")
    file_handler.extractall(folder)
    file_handler.close()
    # the data is extracted into a "__MACOSX" folder. This is either due to my setup, or the way the zip file is created. 
    # the following shell call extracts everything into "folder", and removes the unwanted "__MACOSX/" directory.
    os.popen("cp -r " + folder + "__MACOSX/* " + folder + "; rm -R " + folder + "__MACOSX/")
else: 
    sys.exit("There is no file at " + path + ". Please check the Readme in the data folder.")    

# update the path to not including the ".zip" ending: 
path = path[:-4]

# Part 2: take a first look into the time series data set

import pandas as pd 

time_series_data = path + "/data/sample_temperature_data_for_coding_challenge.csv"


ts = pd.read_csv(time_series_data)

# data columns are "index" (generated from pandas), "source_id", "datetime", "property_name", "temperature"

#TODO: split the datetime into day and time, both for understanding and visualization

ts["temperature"].describe()

# notice 1:
# source_id holds only 1 entry: 
# pd.crosstab(ts["source_id"], ts["source_id"])

from plotnine import ggplot, aes, geom_point, theme, element_text

first_plot = ggplot(ts) + aes(x = "datetime", y = "temperature", color = "property_name") + geom_point() + theme(axis_text_x = element_text(angle = 70, hjust = 1, size = 3))

#TODO: x axis is unreadable!
first_plot.save(filename = "../results/time_series_plot.pdf")

# notes: 
# (i) for a few time points, there are multiple entries: 
sum(ts.duplicated(subset = ["datetime"]))

# (ii) there are a lot of very low "15" entries 
pd.crosstab(ts.duplicated(subset = ["datetime"]), ts["temperature"])
pd.crosstab(ts.duplicated(subset = ["datetime"]), ts["property_name"])

ts.loc[ts.duplicated(subset = ["datetime"]), "temperature"].describe()


# Part 3: take a first look into the customer lead generator data

clg = read_clg_data()

# notes: 
# (i) b_specialisation* seems to be one-hot-encoded

# (ii) column "b_in_kontakt_gewesen" + "b_gekauft_gesamt" are labels 
# -> I assume that we want to predict the "b_gekauft_gesamt" column, 
# which is a [0,1]/TRUE, FALSE variable. 

pd.crosstab(clg["b_gekauft_gesamt"], clg["b_in_kontakt_gewesen"]) 

# => there are 3716 "0", and 57 "1" entries => heavily 
# skewed/inbalanced distributed
# -> Additionally, there are only 95 contacts in total, 38 did not
#  lead to sellings, 57 did. 

# I assume that we want to identify those rows (=> samples) in 
# dataset that are similar to the "in kontakt gewesen" + "gekauft_gesamt" 
# samples. 
# additionally, we want to identify those featuers that are predictive whether 
# "gekauft_gesamt". With that model, we may additionally identify those samples that potentially should be contacted. Vice versa we can identify those samples, which that should potentially not be contacted. 
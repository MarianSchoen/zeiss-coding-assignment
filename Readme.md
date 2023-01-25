# Coding Challenge
This project is part of my (Marian Schön) application as a data scientist at Zeiss. 

# Structure

There are 3 main folders - data, src, results. 
Scripts are stored in `./src`, automatically generated results in `./results`, the `./data` folder is empty as I do not want to share external data. 

# The Challenges

## Time Series Data 

Data consists 1000 samples (= rows) and 5 features (= columns), including 1 index column. `source_id` holds in total 1 level "MICDEV001", and is therefore not used. `temperature` holds numeric entries  

[min: 32.9, mean: 29.5, median: 32.9, max: 39.4]

There are many "15.0" entries, that - from a first glance - do not fit into the rest of the data.
For this, see the pdf at [`results/time_series_plot.pdf`](results/time_series_plot.pdf).  

The `datetime` has year-moth-day-Thour:min:sec:millisec format. For 284 time points there are duplicated entries. 279 of the 284 duplicated entries are labelled as "cooling_temperature" in the `property_name`column. 
The duplicated entries have a 

[min: 14.9, mean: 21.4, median: 20.9, max: 33.9] 

This suppports my first impression of potentially incorrect double measurements of the device. 

My approach would be to learn a moving window temperature prediction model. This model takes as an input the temperatures at time points x-10 : x-1 to predict the temperature at x. I'd do that with a moving window approach, this means that the first sample would be predicting time point 11, the second sample would be predicting time point 12, and so on. 

Things that need to be considered for this approach: 

- I'd use a weigthed regression approach like: 
$t_x = \beta_0 + \sum_{c = x-10}^{x-1} \beta * t_c$. 
In words this means that the temperature at time point x is estimated as a weighted sum of the previuos time points, plus an offset $\beta_0$. The $\beta$ are shared between all models.
- data needs to be splitted in test and train data, this can either be done uniformly, or cyling wise. In the `results/time_series_plot.pdf`, there seem to be cycling high/low temperatures. Maybe we can use cycle 1,3,5,... for training and 2,4,5 for testing. This would ensure a cleaner train/test split which is necessary due to the moving window approach.
- I don't know whether the last 10 time points are sufficient to predict the current temperature, maybe we need more or less. From the start, we should take the number of time points as an input parameter - let's name it p -, and test different values later on
- Predicting the current temperature is obviously affected whether the previous period was a heating or cooling temperature. This adds a new parameter to our model, that indicates whether the p temperatures before are cooling or heating. 
- I already assumed that the double measurement points are potentially wrong - I'd not use them for test or training. Later on, we can predict those time points and see whether one of the duplicated time points fits our model better. 

## Custom Lead Generator
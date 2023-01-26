# Coding Challenge
This project is part of my (Marian Schön) application as a data scientist at Zeiss. 

# Structure

There are 3 main folders - data, src, results. 
Scripts are stored in `./src`, automatically generated results in `./results`, the `./data` folder is empty as I do not want to share external data. 
Please paste the provided zip file into the `./data`/` folder. 

# The Challenges

## Time Series Data 

Data consists of 1000 samples (= rows) and 5 features (= columns), including 1 index column. `source_id` holds in total 1 level "MICDEV001", and is therefore not used. `temperature` holds numeric entries  

[min: 32.9, mean: 29.5, median: 32.9, max: 39.4]

There are many "15.0" entries, that - from a first glance - do not fit into the rest of the data.
For this, see the pdf at [`results/time_series_plot.pdf`](results/time_series_plot.pdf).  

The `datetime` has year-moth-day-Thour:min:sec:millisec format. For 284 time points, there are duplicated entries. 279 of the 284 duplicated entries are labelled as "cooling_temperature" in the `property_name`column. 
The duplicated entries have a 

[min: 14.9, mean: 21.4, median: 20.9, max: 33.9] 

This supports my first impression of potentially incorrect double measurements of the device. 

My approach would be to learn a moving window temperature prediction model. This model takes as an input the temperatures at time points x-10 : x-1 to predict the temperature at x. I'd do that with a moving window approach, this means that the first sample would be predicting time point 11, the second sample would be predicting time point 12, and so on. 

Things that need to be considered for this approach: 

- For a start, I'd use a weighted regression approach like:  
$t_x = \beta_0 + \sum_{c = x-10}^{x-1} \beta * t_c$  
In words, this means that the temperature at time point x is estimated as a weighted sum of the previous time points, plus an offset $\beta_0$. All $\beta$ are shared between all time points/models. 
- data needs to be split into test and train data, this can either be done uniformly or cycling-wise. In the `results/time_series_plot.pdf`, there seem to be cycling high/low temperatures. Maybe we can use cycles 1,3,5, ... for training and 2,4,5 for testing. This would ensure a cleaner train/test split which is necessary due to the moving window approach.
- I don't know whether the last 10 time points are sufficient to predict the current temperature, maybe we need more or less. From the start, we should take the number of time points as an input parameter - let's name it p -, and test different values later on
- Predicting the current temperature is obviously affected by whether the previous period was a heating or cooling temperature. This adds a new parameter to our model, that indicates whether the p temperatures before are cooling or heating. 
- I already assumed that the double measurement points are potentially wrong - I'd not use them for test or training. Later on, we can predict those time points and see whether one of the duplicated time points fits our model better. 

As my talent for time series is laying dormant, I decided not to analyse this data set first. Hopefully, we can come back later to this problem, share ideas and implement it!

## Custom Lead Generator

This data set consists of 3773 rows (=> samples), and 26 columns. There are 23 feature columns, one `fakeID` column, and 2 boolean variables `b_in_kontakt_gewesen` and `b_gekauft_gesamt`. As indicated in the description pdf, I assume that those are the important labels for this dataset. I assume that `b_in_kontakt_gewesen` means whether this sample has been contacted, and `b_gekauft_gesamt` indicates whether there was a sale. In total, there have been 95 contacts, 57 of which led to a sale. There was no sale without a contact previously. 

For this challenge, I state the following two main questions: 

1. Identify those unvisited samples that are similar to visited samples that have led to a sale.  For the moment I call these `potential sales candidates`. This includes identifying features that indicate that there will be a sale, `potential sales features`. 
2. Identify those features that characterise samples which did not lead to a sale, even though they have been visited. Let's call these `potential reject candidates`. As above, this includes identifying features that serve as `potential sale inhibitors`. 

This means, that I train 2 different models. 
Once, I predict whether there was a sale or not (`b_gekauft_gesamt`). In this approach, I disregard the `b_in_kontakt_gewesen` feature. 

Things, that need to be considered for this approach: 

- There are only 95 samples to train/optimise a model on. Therefore, I will use leave-one-out cross-validation to increase the test set. With the cross-validation, I check the test/training error ratio, to detect over-fitting, and calibrate the regularization parameter. 
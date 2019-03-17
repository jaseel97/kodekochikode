# Kode Kochi Kode Hackathon code Repo

## What is it?

Tool to predict places where most buying and selling of real estate would happen based on historic data.
Done during the 24 hour Kode Kochi Kode Hackathon at [Rajagiri School of Engineering and Technology \(RSET\)](https://www.rajagiritech.ac.in/) 

## Specifics

Given 5 years of Manhattan's real-estate transactions, we tasked ourselves with prediting the top locations for the next couple of years, sales wise.
The steps we have to carry out:
- Explore the dataset
- Clean the data
- Create a ML model to predict values

The R files: 
- [Analysis](./uni_bi_variate_analysis.R) [@jaseel97](https://github.com/jaseel97)
- [Cleaning](./Residential_Data_Clean.R)  [@Joeavaikath](https://github.com/Joeavaikath)
- [Aggregation](./AggregationR.R)         [@Joeavaikath](https://github.com/Joeavaikath)

The python files for the Neural Network(NN): \(all [@George V Jose](https://github.com/GeorgeVJose)\)
- [Prediction NN](./forecast_model.py)
- [Final score computation](./final_val_compute.py)

## End result

A 4 year trained model failed to validate reasonably on the 5th year. However, we noticed that the trends themselves were preserved i.e. increase for increase, decrease for decrease. Since our aim was getting the best locations, we didn't need exact sale value predictions.


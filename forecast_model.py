import keras
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import MinMaxScaler

filename = 'AggregatedData/Data_Combined.csv'
df = pd.read_csv(filename)

locs = df['Neighbourhood'].unique()
drop_locations = ['HARLEM-WEST', 'JAVITS CENTER', 'SOUTHBRIDGE', 'MANHATTAN-UNKNOWN', 'ROOSEVELT ISLAND']
locations = []
for x in locs:
    if x not in drop_locations:
        locations.append(x)
print(locations)

def get_volumes():
    data = {}
    for location in locations:
        # print(location)
        vol = df.loc[df['Neighbourhood'] == location, 'Mean'].values
        data[location] = vol
    return data

data = get_volumes()

yr_split = 4
split = (yr_split*12)

def gen_test_train(split):
    train_data = {}
    test_data = {}
    for location in locations:
        vol = data[location]
        train = vol[:split]
        test = vol[split:]
        
        train_data[location] = train
        test_data[location] = test
    return (train_data, test_data)

train_data, test_data = gen_test_train(split)

look_back = 3
batch_size = 10

def create_generator(data_dict):
    generators = {}
    for location in data_dict.keys():
        # print(location)
        val = data_dict[location].reshape((-1,1))
        gen = TimeseriesGenerator(val, val, length=look_back, batch_size=batch_size)
        # print(gen)
        generators[location] = gen
    return generators

train_generator = create_generator(train_data)
test_generator = create_generator(test_data)
print("Generator Created")

# Neural Network

def build_network(look_back):
    model = Sequential()
    model.add(
        LSTM(10,
            input_shape = (look_back, 1)
        )
    )
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_network(look_back)

trained_models = {}
for location in train_generator.keys():
    generator = train_generator[location]
    # print(generator)
    model.fit_generator(generator, epochs=10, verbose=0)
    trained_models[location] = model
    model.reset_states()


def prediction(test_generator, trained_models):
    predictions = {}
    for location in test_generator.keys():
        model = trained_models[location]
        pred = model.predict(test_generator[location])
        predictions[location] = pred
    return predictions

predictions = prediction(test_generator, trained_models)

test_location = locations[0]
print(test_data[test_location])
print(predictions[test_location])



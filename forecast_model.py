import keras
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from plotly.offline import plot
# import plotly.io as pio

import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

filename = 'AggregatedData/Data_Combined.csv'
df = pd.read_csv(filename)
df['Mean'] = df['Mean'].astype('int32')

scaler = MinMaxScaler()
scaler.fit(df['Mean'].values.reshape((-1,1)))
df['Mean'] = scaler.transform(df['Mean'].values.reshape((-1,1))).reshape(-1)

scaler = MinMaxScaler()
scaler.fit(df['Count'].values.reshape((-1,1)))
df['Count'] = scaler.transform(df['Count'].values.reshape((-1,1))).reshape(-1)


locs = df['Neighbourhood'].unique()
drop_locations = ['HARLEM-WEST', 'JAVITS CENTER', 'SOUTHBRIDGE', 'MANHATTAN-UNKNOWN', 'ROOSEVELT ISLAND']
locations = []
for x in locs:
    if x not in drop_locations:
        locations.append(x)
print(locations)
# locations = [locations[0]]

def get_volumes():
    data = {}
    for location in locations:
        vol = df.loc[df['Neighbourhood'] == location, 'Count'].values
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
batch_size = 5

def create_generator(data_dict):
    generators = {}
    for location in data_dict.keys():
        val = data_dict[location].reshape((len(data_dict[location]),1))
        gen = TimeseriesGenerator(val, val, length=look_back, batch_size=batch_size)
        generators[location] = gen
    return generators

train_generator = create_generator(train_data)
test_generator = create_generator(test_data)
# print("Generator Created")

# Neural Network

def build_network(look_back):
    model = Sequential()
    model.add(
        LSTM(5,
            input_shape = (look_back, 1)
            # return_sequences=True
        )
    )
    # model.add(
    #     LSTM(5,
    #         input_shape = (look_back, 1)
    #     )
    # )
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

model = build_network(look_back)

trained_models = {}
for i,location in enumerate(train_generator.keys()):
    generator = train_generator[location]
    model.fit_generator(generator, epochs=50, verbose=0)
    trained_models[location] = model
    model.reset_states()
    print("Model for {}. \t\t\tTrained: {}/{}".format(location, i+1, len(train_generator.keys())))


def prediction(test_generator, trained_models):
    predictions = {}
    for location in test_generator.keys():
        model = trained_models[location]
        generator = test_generator[location]
        pred = model.predict_generator(generator)
        predictions[location] = pred.reshape((-1))
    return predictions

predictions = prediction(test_generator, trained_models)

test_location = locations[0]
print(scaler.inverse_transform(test_data[test_location].reshape((-1,1))))
print((scaler.inverse_transform(predictions[test_location].reshape((-1,1)))))

def plot_loc(loc, i):
    train = train_data[loc]
    test = test_data[loc]
    predict = predictions[loc]

    trace1 = go.Scatter(
        x = np.arange(len(train)),
        y = train,
        mode = 'lines',
        name = 'Train'
    )
    trace2 = go.Scatter(
        x = np.arange(len(train), len(train)+len(test)),
        y = test,
        mode = 'lines',
        name = 'Test'
    )
    trace3 = go.Scatter(
        x = np.arange(len(train), len(train)+len(test)),
        y = predict,
        mode = 'lines',
        name = 'Prediction'
    )
    layout = go.Layout(
        title=loc
    )
    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    # pio.write_image(fig, file='Images/plot-{}'.format(i), format='png')
    # filename = "image-1"
    plot([trace1, trace2, trace3], image='jpeg', auto_open=False)

i=2
plot_loc(locations[i], i)
# for i, location in enumerate(locations):
#     plot_loc(location, i)
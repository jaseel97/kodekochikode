import keras
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.plotly as py
from keras.layers import LSTM, Dense
from keras.models import Sequential
from keras.preprocessing.sequence import TimeseriesGenerator
from plotly.offline import plot

import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

filename = 'AggregatedData/Data_Combined.csv'
df = pd.read_csv(filename)
df['Mean'] = df['Mean'].astype('int32')

scaler = MinMaxScaler()
scaler.fit(df['Mean'].values.reshape((-1,1)))
df['Mean'] = scaler.transform(df['Mean'].values.reshape((-1,1))).reshape(-1)

# scaler = MinMaxScaler()
# scaler.fit(df['Count'].values.reshape((-1,1)))
# df['Count'] = scaler.transform(df['Count'].values.reshape((-1,1))).reshape(-1)


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
        vol = df.loc[df['Neighbourhood'] == location, 'Mean'].values
        data[location] = vol
    return data

data = get_volumes()

look_back = 3
batch_size = 5

def create_generator(data_dict):
    generators = {}
    for location in data_dict.keys():
        val = data_dict[location].reshape((len(data_dict[location]),1))
        gen = TimeseriesGenerator(val, val, length=look_back, batch_size=batch_size)
        generators[location] = gen
    return generators

train_generator = create_generator(data)

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



def predict(location, num_predictions):
    model = trained_models[location]
    prediction_values = data[location][-look_back:]

    for _ in range(num_predictions):
        x = prediction_values[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]
        # print(out)
        prediction_values = np.append(prediction_values, out)

    prediction_values = prediction_values[look_back:]
    prediction_values = scaler.inverse_transform(prediction_values.reshape((-1,1)))
    prediction_values = prediction_values.reshape(-1)
    # print(">>>",prediction_values)

    return prediction_values

num_predictions = 6
predictions = {}
for location in locations:
    predictions[location] = predict(location, num_predictions)

data_final = [[i, np.mean(predictions[i])] for i in locations]
df_final = pd.DataFrame(data_final, columns=['Location', 'Value'])
df_final = df_final.sort_values('Value', ascending=False)
print(df_final)
df_final.to_csv("final_stat_mean.csv")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_squared_log_error, median_absolute_error, explained_variance_score
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input
import time

# Production
# from model.cropHealth import calculateHealth
# from model.knn_function import knn_impute

# Development
from cropHealth import calculateHealth
from knn_function import knn_impute

def predict(data_input, crop, hectare, data=None, optimums=None, retrain=False): # data and optimums are not used
    # Production data
    # data = pd.read_csv('model/processed_data/model_data_soil_moisture.csv')
    # optimums = pd.read_csv('model/optimums.csv')

    # Development data
    data = pd.read_csv('processed_data/model_data_soil_moisture.csv')
    optimums = pd.read_csv('optimums.csv')

    data = pd.DataFrame(data)
    optimums = pd.DataFrame(optimums)

    crops = [
        'maize',
        'maize_comm',
        'maize_non_comm',
        'wheat',
        'groundnuts',
        'sunflowerseed',
        'sorghum',
        'soybeans',
        'barley',
        'canola',
        'oats'
    ]
    crops = [c + '_ton_per_hectare' for c in crops]

    def create_sequences(X, y, seq_length): # X is the input data, y is the output data
        Xs, ys = [], []
        for i in range(len(X) - seq_length):
            Xs.append(X[i:i+seq_length])
            ys.append(y[i+seq_length])
        return np.array(Xs), np.array(ys)

    def preprocess_data(df, crop): # df is the data, crop is the crop to predict
        other_crops = [c for c in crops if c != crop]

        df = df.drop(columns=other_crops)
        df = df[df[crop].notnull()]
        return df

    def train_model(X_train, y_train, seq_length): # X_train is the input data, y_train is the output data
        model = Sequential()
        model.add(Input(shape=(seq_length, X_train.shape[2])))
        model.add(LSTM(50, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=250, validation_split=0.2, batch_size=24)
        return model

    def predict_yield(data_input, crop, hectare, retrain=False):
        times = []
        start_time = time.time()

        crop = crop + '_ton_per_hectare'

        # Preprocess the data
        df = preprocess_data(data, crop)
        X = df.drop(columns=['date', crop])
        y = df[crop]

        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()
        X_weighted = scaler_X.fit_transform(X)
        y_weighted = scaler_y.fit_transform(y.values.reshape(-1, 1))

        seq_length = 12
        X_seq, y_seq = create_sequences(X_weighted, y_weighted, seq_length)

        X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

        end_time = time.time()
        times.append(end_time - start_time)
        start_time = time.time()

        if retrain:
            model = train_model(X_train, y_train, seq_length)
            model.save(crop + '_yield_prediction_model_v2.keras')
        else:
            try:
                model = load_model(crop + '_yield_prediction_model_v2.keras')
            except:
                model = train_model(X_train, y_train, seq_length)
                model.save(crop + '_yield_prediction_model_v2.keras')

        end_time = time.time()
        times.append(end_time - start_time)
        start_time = time.time()

        y_pred = model.predict(X_test)
        y_pred = scaler_y.inverse_transform(y_pred)
        y_test = scaler_y.inverse_transform(y_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        msle = mean_squared_log_error(y_test, y_pred)
        medae = median_absolute_error(y_test, y_pred)
        evs = explained_variance_score(y_test, y_pred)

        # print("\n\033[92m" + "Model evaluation" + "\033[0m")
        # print(f"Mean Squared Error: {mse}")
        # print(f"R-squared: {r2}")
        # print(f"Mean Absolute Error: {mae}")
        # print(f"Mean Squared Log Error: {msle}")
        # print(f"Median Absolute Error: {medae}")
        # print(f"Explained Variance Score: {evs}")

        X_input = pd.DataFrame([data_input])
        combined_df = pd.concat([df, X_input], ignore_index=True)
        df_imputed = knn_impute(combined_df)
        X_input = df_imputed.tail(1)
        X_input = X_input.drop(columns=[crop])
        X_input = X_input[X.columns]

        X_input_seq = []
        for i in range(seq_length):
            X_input_seq.append(X_input.values.flatten())
        X_input_seq = np.array(X_input_seq).reshape((1, seq_length, X_input.shape[1]))

        X_input_seq = scaler_X.transform(X_input_seq.reshape(-1, X_input.shape[1]))
        X_input_seq = X_input_seq.reshape((1, seq_length, X_input.shape[1]))

        yield_input = model.predict(X_input_seq)
        yield_input = scaler_y.inverse_transform(yield_input)

        total_yield = hectare * yield_input[0][0]

        health = calculateHealth(df_imputed, crop.split('_')[0], 10, optimums)
        # health is a dictionary with keys 'crop', and 'health_score' where 'health_score' is an Array of health scores
        # 'numpy.ndarray' object has no attribute 'tail'
        health_score = health['health_score'][-1]

        columns = X.columns

        # Select last entry of X_input_seq
        X_input_seq = X_input_seq[0][-1]

        # Create a DataFrame from X_input_seq
        X_input_seq = pd.DataFrame([X_input_seq], columns=columns)

        # Convert to dictionary
        X_input_seq = X_input_seq.to_dict(orient='records')[0]

        end_time = time.time()
        times.append(end_time - start_time)

        result = {
            'yield_per_hectare': yield_input[0][0],
            'yield': total_yield,
            'health_score': health_score,
            'statistics': {
                'mean_squared_error': mse,
                'r_squared': r2,
                'timing': {
                    'preprocessing': times[0],
                    'training': times[1],
                    'prediction': times[2]
                }
            },
            # 'fitness': X_input_seq,
        }

        # Change all '' to "" for JSON compatibility
        result = str(result).replace("'", '"')

        # Convert to dictionary
        result = eval(result)

        return result
    return predict_yield(data_input, crop, hectare, retrain)

result = predict({
    'date': '2023-01-01',
    'cloud_cover': 43.1,
    'precipitation': 89.4,
    'maximum_temperature': 29.1, 
    'minimum_temperature': 15.5,
    'vapour_pressure': 15.1
}, "wheat", 4, None, None, True)

print(result)
import json
import argparse
from pathlib import Path

import xgboost as xgb
import numpy as np
import pandas as pd

from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score

def _extremegboost(args):

    # Open and reads file "data"
    with open(args.data) as data_file:
        data = json.load(data_file)
    
    # The excted data type is 'dict', however since the file
    # was loaded as a json object, it is first loaded as a string
    # thus we need to load again from such string in order to get 
    # the dict-type object.
    data = json.loads(data)

    x_train = data['x_train']
    y_train = data['y_train']
    x_val = data['x_val']
    y_val = data['y_val']

    
    # Initialize XGB with objective function
    parameters = {"objective": 'reg:squarederror',
                "n_estimators": 100,
                "verbosity": 0}

    model = xgb.XGBRegressor(**parameters)
    model.fit(x_train, y_train)
        
    # generate predictions
    y_pred_train = model.predict(x_train).reshape(-1,1)
    y_pred = model.predict(x_val).reshape(-1,1)
        
    # calculate errors
    rmse_train = mean_squared_error(y_pred_train, y_train, squared=False)
    rmse_val = mean_squared_error(y_pred, y_val, squared=False)
    print(f"rmse training: {rmse_train:.3f}\t rmse validation: {rmse_val:.3f}")

    
    #Extracting ref and prod from 'data'
    ref_data = data['ref_data']
    prod_data = data['prod_data']
    X_train_full = data['x_train_full']
    X_prod = data['x_prod']

    column_names = ["id", "data", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "...", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15"]

    //ref_data and prod_data was stored as numpy.darray, therefore, converting back to pandas DataFrame.
    ref_data = pd.DataFrame.from_records(ref_data)
    ref_data.columns = column_names

    prod_data = pd.DataFrame.from_records(prod_data)
    prod_data.columns = column_names

    ref_data['prediction'] = model.predict(X_train_full)
    prod_data['prediction'] = model.predict(X_prod)
    ref_data['price_log'] = np.log1p(ref_data['price'])
    prod_data['price_log'] = np.log1p(prod_data['price'])

    ref_data_final_numpy = ref_data.to_numpy()
    prod_data_final_numpy = prod_data.to_numpy()

    evidently_data = {
        'ref_data' : ref_data_final_numpy.tolist(),
        'prod_data' : prod_data_final_numpy.tolist()
    }

    # Creates a json object based on `evidently_data`
    evidently_data_json = json.dumps(evidently_data)

    # Saves the json object into a file
    with open(args.evidently_data, 'w') as out_file:
        json.dump(evidently_data_json, out_file)


if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--data', type=str)
    parser.add_argument('--evidently_data', type=str)

    args = parser.parse_args()

    # Creating the directory where the output file will be created (the directory may or may not exist).
    Path(args.evidently_data).parent.mkdir(parents=True, exist_ok=True)
    
    _extremegboost(args)
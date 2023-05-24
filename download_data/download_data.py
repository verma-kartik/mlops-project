import json
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

def _download_data(args):

    # Gets and split dataset
    url='https://drive.google.com/file/d/1e83nTKyy9UiiparbtiLMTbF1HC40lr0r/view?usp=share_link'
    url='https://drive.google.com/uc?id=' + url.split('/')[-2]
    df = pd.read_csv(url)
    df[['grade','view','waterfront']] = df[['grade','view','waterfront']].astype('object')

    # Delete entry with 33 bedrooms
    df = df[df["bedrooms"] != 33]

    features = ['sqft_living','grade', 'sqft_above', 'sqft_living15',
           'bathrooms','view','sqft_basement','lat','long','waterfront',
           'yr_built', 'bedrooms']
    
    #creating two datasets for evidently.ai API
    ref_data = df[:15000]
    prod_data = df[15000:]

    X_train, X_val, y_train, y_val = train_test_split(ref_data[features], ref_data['price'], test_size=0.2, shuffle=True, random_state=42)

    categorical = ['grade', 'view', 'waterfront']
    ohe = OneHotEncoder(handle_unknown = 'ignore')
    ohe = ohe.fit(X_train[categorical])

    def preprocessing(X, y, ohe):
        # Convert grade, view, waterfront to type object
        X[['grade','view','waterfront']] = X[['grade','view','waterfront']].astype('object')
        
        # log transform the target varibale 
        y = np.log1p(y)
        
        # define categorical and numerical varibales 
        categorical = ['grade', 'view', 'waterfront']
        numerical = ['sqft_living', 'sqft_above', 'sqft_living15',
            'bathrooms','sqft_basement','lat','long','yr_built',
            'bedrooms']
        
        # one-hot encode categorical variables
        X_cat = ohe.transform(X[categorical]).toarray()
        
        # define numerical columns 
        X_num = np.array(X[numerical])
        
        # concatenate numerical and categorical variables
        X = np.concatenate([X_cat, X_num], axis=1)
        
        print('Shape after one-hot encoding')
        print(f'X shape: {X.shape}')
        
        return X, y
    
    X_train, y_train = preprocessing(X_train, y_train, ohe)
    X_val, y_val = preprocessing(X_val, y_val, ohe)
    X_prod, y_prod = preprocessing(prod_data[features], prod_data['price'], ohe)

    X_train_full, y_train_full = preprocessing(ref_data[features], ref_data['price'], ohe)

    ref_data_numpy = ref_data.to_numpy()
    prod_data_numpy = prod_data.to_numpy()

    # Creates `data` structure to save and 
    # share train, val and prod datasets.
    data = {'x_train' : X_train.tolist(),
            'y_train' : y_train.tolist(),
            'x_train_full' : X_train_full.tolist(),
            'y_train_full' : y_train_full.tolist(),
            'x_val' : X_val.tolist(),
            'y_val' : y_val.tolist(),
            'x_prod' : X_prod.tolist(),
            'y_prod' : y_prod.tolist(),
            'ref_data' : ref_data_numpy.tolist(),
            'prod_data' : prod_data_numpy.tolist()}

    # Creates a json object based on `data`
    data_json = json.dumps(data)

    # Saves the json object into a file
    with open(args.data, 'w') as out_file:
        json.dump(data_json, out_file)

if __name__ == '__main__':
    
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)
    
    args = parser.parse_args()
    
    # Creating the directory where the output file will be created 
    # (the directory may or may not exist).
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    _download_data(args)
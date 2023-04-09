import json
import argparse
from pathlib import Path
from collections import namedtuple
import os

import pandas as pd
from google.cloud import storage
from IPython.display import display, HTML

from evidently.dashboard import Dashboard
from evidently.pipeline.column_mapping import ColumnMapping
# packages for interactive dashboards
from evidently.dashboard.tabs import DataDriftTab, DataQualityTab, NumTargetDriftTab, RegressionPerformanceTab


def _evidently_monitoring(args):

    # Open and reads file "data"
    with open(args.evidently_data) as data_file:
        evidently_data = json.load(data_file)

    evidently_data = json.loads(evidently_data)

    ref_data = evidently_data['ref_data']
    prod_data = evidently_data['prod_data']

    column_names = ["id", "data", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors", "waterfront", "view", "...", "grade", "sqft_above", "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long", "sqft_living15", "sqft_lot15", "prediction", "price_log"]

    ref_data = pd.DataFrame.from_records(ref_data)
    ref_data.columns = column_names

    prod_data = pd.DataFrame.from_records(prod_data)
    prod_data.columns = column_names


    # Define the data drift dashboard using the DataDriftTab.
    column_mapping = ColumnMapping()
    target = 'price_log'
    numerical_features = ['sqft_living', 'sqft_above', 'sqft_living15',
            'bathrooms','sqft_basement','lat','long',
            'yr_built','bedrooms']
    categorical_features = ['grade', 'view', 'waterfront']
    column_mapping.target = target
    column_mapping.prediction = 'prediction'
    column_mapping.numerical_features = numerical_features
    column_mapping.categorical_features = categorical_features

    print(column_mapping)

    data_drift_dashboard = Dashboard(tabs=[DataDriftTab(verbose_level=1)])
    data_drift_dashboard.calculate(ref_data, prod_data, column_mapping=column_mapping)

    #data_drift_dashboard.show()

    #Tried to show report in Kubeflow Visualization but no output.
    '''
    data_drift_dashboard_filename = "data_drift.html"
    local_dir = "/tmp/artifact_downloads"
    if not os.path.exists(local_dir):
        os.mkdir(local_dir)
    static_html_path = os.path.join(local_dir, data_drift_dashboard_filename)
    data_drift_dashboard.save(static_html_path)
    with open(static_html_path, "r") as f:
        f.read()
    '''

    #Saving html reports to GCP Bucket associated with the pipeline.
    def save_to_bucket(name_in_bucket: string, name_in_system: string):
        # Setting credentials using the downloaded JSON file
        client = storage.Client.from_service_account_json(json_credentials_path='<path_to_JSON_file')
        # Creating bucket object
        bucket = client.get_bucket('mlops-assignment-kv-kubeflowpipelines-default')
        # Name of the object to be stored in the bucket
        object_name_in_gcs_bucket = bucket.blob(name_in_bucket)
        # Name of the object in local file system
        object_name_in_gcs_bucket.upload_from_filename(name_in_system)

    data_drift_dashboard.save('data_drift.html')
    save_to_bucket('datadrift.html', './data_drift.html')



    #Define the target drift dashboard using the NumTargetDriftTab.
    column_mapping = ColumnMapping()

    target = 'price_log'
    column_mapping.target = target
    column_mapping.numerical_features = numerical_features
    column_mapping.categorical_features = categorical_features

    target_drift_dashboard = Dashboard(tabs=[NumTargetDriftTab(verbose_level=1)])
    target_drift_dashboard.calculate(ref_data, prod_data, column_mapping=column_mapping)

    target_drift_dashboard.save('target_drift.html')

    save_to_bucket('targetdrift.html', './target_drift.html')



    #Define the performance of a regression model using the RegressionPerformanceTab
    model_performance_dashboard = Dashboard(tabs=[RegressionPerformanceTab(verbose_level=1)])
    model_performance_dashboard.calculate(ref_data, prod_data, column_mapping=column_mapping)
    
    model_performance_dashboard.save('model_perfomance.html')

    save_to_bucket('modelperfomance.html', './model_perfomance.html')


if __name__ == '__main__':

    # Defining and parsing the command-line arguments
    parser = argparse.ArgumentParser(description='My program description')
    parser.add_argument('--evidently_data', type=str)

    args = parser.parse_args()

    _evidently_monitoring(args)



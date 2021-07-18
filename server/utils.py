import pickle, gzip
import json
import pandas as pd
from collections import OrderedDict

__col_info = None
__model = None
__pipeline = None

def set_col_info(file):
    print("Loading data columns...")
    global __col_info

    with open("./artifacts/" + file, 'rb') as f:
        __col_info = json.load(f, object_pairs_hook=OrderedDict)

    print("Data columns successfully loaded")

def get_col_info():
    return __col_info

def get_data_columns():
    return get_col_info()['data_columns']

def set_model(file):
    print("Loading model...")
    global __model

    with open("./artifacts/" + file, 'rb') as f:
        with gzip.open("model/randforest_model_optimized.pickle", 'rb') as f:
            p = pickle.Unpickler(f)
            __model = p.load()

    print("Model successfully loaded")

def get_model():
    return __model

def set_pipeline(file):
    print("Loading pipeline...")
    global __pipeline

    with open("./artifacts/" + file, 'rb') as f:
        __pipeline = pickle.load(f)

    print("Pipeline successfully loaded")

def get_pipeline():
    return __pipeline

def make_prediction(model, pipeline, test_matrix):
    """Takes a model, pipieline, and test_matrix. Test matrix is
    transformed by the pipeline and fed into the model. A yes/no string
    is returned according to the prediction"""
    
    test_matrix = pd.DataFrame(test_matrix, columns=get_data_columns())
    test_matrix = pipeline.transform(test_matrix)
    prediction = model.predict(test_matrix)
    if (prediction == 1):
        return "Yes"
    else:
        return "No"

# Main function to test utils functionality
if __name__ == "__main__":
    set_col_info('data_columns.json')
    set_pipeline('pipeline.pickle')
    set_model('randforest_model.pickle')

    test_answers=[[123, 3, 5, 10, 2, 1, 50, 20, 1, 2, 0, 5, 1, 1]]

    print(make_prediction(get_model(), get_pipeline(), test_answers))
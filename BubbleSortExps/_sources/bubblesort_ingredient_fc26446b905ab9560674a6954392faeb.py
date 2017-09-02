import numpy as np
from sacred import Ingredient

data_ingredient = Ingredient('bubblesort_input_dataset')

@data_ingredient.config
def cfg():
    filename = 'bubblesort_input_dataset.csv'
    normalize = False

@data_ingredient.capture
def load_data(filename, normalize):
    data = np.genfromtxt(filename, delimiter=' | ')
    data = np.delete(data, 0 ,0)

    if normalize:
        data -= np.mean(data)

    return data
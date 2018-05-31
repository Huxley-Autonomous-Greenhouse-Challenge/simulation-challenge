impotrt pandas as pd
import tensorflow as tf
import os
import math
import numpy as np
from email_utils import send_mail, read_mail
from time import sleep
from xlsx_utils import load_xlsx, get_variables, set_variables, print_sheet
from score import score
from tensorflow.python.data import Dataset
from sklearn import metrics

# Use gradient descent as the optimizer for training the model.
my_optimizer=tf.train.GradientDescentOptimizer(learning_rate=0.1)
my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)

# TODO: get features from elsewhere like get_variables()
profit_filePath = os.path.join(os.getcwd(), 'profit.csv')
profit_dataframe = pd.read_csv(profit_filePath, header=None)

# Define the input feature: total_rooms.
my_features_filepath = os.path.join(os.getcwd(), 'params.csv')
my_features = pd.read_csv(my_features_filepath)

target = profit_dataframe
target.columns = [
    'Profit'
]

# TODO pick features to optimize
# Configure a numeric feature column for total_rooms.
feature_columns = [tf.feature_column.numeric_column(column) for column in my_features.columns]

# Configure the linear regression model with our feature columns and optimizer.
# Set a learning rate of 0.0000001 for Gradient Descent.
linear_regressor = tf.estimator.LinearRegressor(
    feature_columns=feature_columns,
    model_dir="model",
    optimizer=my_optimizer
)

def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):
    """Trains a linear regression model of one feature.
    Args:
      features: pandas DataFrame of features
      targets: pandas DataFrame of targets
      batch_size: Size of batches to be passed to the model
      shuffle: True or False. Whether to shuffle the data.
      num_epochs: Number of epochs for which data should be repeated. None = repeat indefinitely
    Returns:
      Tuple of (features, labels) for next data batch
    """
    # Convert pandas data into a dict of np arrays.
    features = {key:np.array(value) for key,value in dict(features).items()}

    # Construct a dataset, and configure batching/repeating.
    ds = Dataset.from_tensor_slices((features,targets)) # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)

    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    print(features, labels)
    return features, labels


_ = linear_regressor.train(
    input_fn = lambda:my_input_fn(my_features, target),
    steps=100
)

# Create an input function for predictions.
# Note: Since we're making just one prediction for each example, we don't 
# need to repeat or shuffle the data here.
prediction_input_fn =lambda: my_input_fn(my_features, target, num_epochs=1, shuffle=False)

# Call predict() on the linear_regressor to make predictions.
predictions = linear_regressor.predict(input_fn=prediction_input_fn)

# Format predictions as a NumPy array, so we can calculate error metrics.
predictions = np.array([item['predictions'][0] for item in predictions])
print(predictions)
# Print Mean Squared Error and Root Mean Squared Error.
mean_squared_error = metrics.mean_squared_error(predictions, target)
root_mean_squared_error = math.sqrt(mean_squared_error)
print("Mean Squared Error (on training data): %0.3f" % mean_squared_error)
print("Root Mean Squared Error (on training data): %0.3f" % root_mean_squared_error)

# def main(simulations=10):
#     # loop over the desired number of epochs
#     for epoch in np.arange(0, simulations):
#         print ("Run #" + str(epoch))
        # v1 = get_variables()
        # v2 = set_variables(v1)

        # # Check to make sure we are getting and setting the same variables
        # if v1 != v2:
        #     print('Warning! get_variables() is returning different results than set variables().')

        # # pick the next set of variables
        # # send_mail()
        # # print('Request sent waiting for response')
        # # sleep(30)
        # read_mail()

        # profit_filePath = os.path.join(os.getcwd(), 'profit.csv');
        # profit_dataframe = pd.read_csv(profit_filePath)

        # print(profit_dataframe)

# main()

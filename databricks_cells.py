# NOTE: Ensure that you install the below packages before proceeding:
# $pip install snowflake-connector-python
# $pip install xgboost-cpu
# $pip install pandas
# $pip install scikit-learn
# $pip install python-dotenv
# $pip install matplotlib
#
# Additionally, you will have to create an .env in your directory 
# containing the "MY_USER", "MY_PW" AND "MY_ACC" enviornmental variables.
#

#Connecting Databricks workspace to Snowflake database
import os
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from xgboost import plot_importance
from matplotlib import pyplot

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv('MY_USER'),
    password=os.getenv('MY_PW'),
    account=os.getenv('MY_ACC')
)

#Querying the table containing the airline data from the connected Snowflake database
query = "SELECT * FROM AIRLINE_SATISFACTION.PUBLIC.AIRLINE_SATISFACTION_CHARACTERISTICS"
#Table will be stored in a pandas dataframe
df = pd.read_sql(query, conn)

# NOTE: Since XGBClassifier will be utilized, there is no need to normalize the data, as the XGBoost model utilizes decision trees. 
# Decision trees process features one at a time, so a difference in scale between two different features is insignificant to the model's decision making process.
# First, we will address NAN values in one of the columns by filling these values 
# with the average of all other values in the column in order to prevent errors and limit distorting the data.
# Since the dataset contains some NA values in the ARRIVAL_DELAY_MINUTES column, 
# these NA values will be filled in with the average of all other values as to minimize skewing the data. 
average_arrival_delay = df['ARRIVAL_DELAY_MINUTES'].mean()
df = df.fillna(average_arrival_delay)
df['ARRIVAL_DELAY_MINUTES']=df.ARRIVAL_DELAY_MINUTES.astype('int64')

#Removing categorical columns which already have an associated numerically encoded column.
categorical_columns = ['CUSTOMER_TYPE', 'TRAVEL_TYPE', 'CLASS_TYPE', 'SATISFACTION']
df = df.drop(categorical_columns, axis=1)

# Select all columns except the SATISFACTION_ONEHOT for features
X = df[df.columns[:-1]]
Y = df['SATISFACTION_ONEHOT']

# Dataset partitioning
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=425)

# Initializing and training model
model = XGBClassifier(random_state=425)
model.fit(X_train, Y_train)

# Evaluating model
Y_pred = model.predict(X_test)
mse = mean_squared_error(Y_test, Y_pred)
acc = accuracy_score(Y_test, Y_pred)
print()
print('Mean Squared Error: ', mse)
print('Accuracy Score: ', acc)
print()

#Visualization
#Displays 10 random samples of the model's prediction in comparison to the actual output
results = pd.DataFrame({
    'Actual': Y_test,
    'Predicted': Y_pred
})
results = results.replace(0, "neutral/dissatisfied")
results = results.replace(1, "satisfied")
print()
print(results.sample(10))
print()

#Plotting relative importance of all features in model's decision making process.
plot_importance(model)
pyplot.show()



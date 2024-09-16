# Airline Satisfaction Classifier
A machine learning model capable of classifying whether a passenger will be satisfied with an airline or not given a variety of data such as passenger age and ticket class. I utilized Snowflake for database storage and basic preprocessing and Databricks for preprocessing on dataframes and ML model training, testing and visualization.

[**Databricks Notebook**](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/4158641153318707/3185215408621267/2729803409437195/latest.html)

## 1.) Dataset Preparation and Basic Preprocessing
The [Airline Satisfaction dataset](https://www.kaggle.com/datasets/teejmahal20/airline-passenger-satisfaction) from **Kaggle** was chosen for training, which includes 129,880 entries and 20+ features, which I found to be both sufficiently large and complex.

<img width="2091" alt="image" src="https://github.com/user-attachments/assets/b1d7a0e6-003e-4558-a199-f2511a7b791e">

The dataset was uploaded to **Snowflake** as a csv file, and saved as a table within a database dedicated to this project. Basic preprocessing such as removing features unnecessary for training and creating encoded versions of categorical data columns to allow for the ML model to train on all of the desired features. 

![image](https://github.com/user-attachments/assets/0b416f44-d312-44a9-87e4-29a9a0a73105)

## 2.) Dataset Connection and Further Preprocessing
The **Snowflake** database was then connected to a **Databricks** workspace, and imported as a pandas dataframe. Further preprocessing operations such as filling in NAN values to prevent training errors, dropping categorical data columns and partitioning the dataset into a training set and testing set were performed.

NAN values were only found in one column, and were filled in with the average of all other values in the column in order to avoid distorting the dataset. Since there are 393 instances of NA values out of 129,880 total datapoints, I believe this alteration did not distort the dataset by a significant margin.

Since a [XGBClassifier](https://github.com/dmlc/xgboost) will be used for training, no normalization is required to be performed, as XGBoost utilizes decision trees. Decision trees analyze features individually, so the difference in scale across different variables is unimportant to the model's accuracy.

<img width="2258" alt="image" src="https://github.com/user-attachments/assets/c49b422c-4efb-4465-a85b-765773edc04d">

## 3.) XGBClassifier Training and Testing
The XGBoost library was used to initialize and train the model. Metrics from the scikit-learn library were used to evaluate the MSE (Mean Squared Error) and the accuracy.

The XGBoost model was selected, as it is better for larger datasets and generally outperforms Random Forest models, which are also commonly used for classifier models. While Random Forest models are easier to interpret, I am mainly interested in maximizing the model's accuracy, a preference which is best suited for the XGBoost model.

![image](https://github.com/user-attachments/assets/0c863e48-4fdb-4cba-8d15-1fc5226ae7bd) ![image](https://github.com/user-attachments/assets/1fbd5000-7736-4319-9f1e-826ceb6c9bb7)

## 4.) Visualization
The plot_importance() function from the XGBoost library was used to plot the importance of each feature, which is determined by the relative frequency at which each feature was used to make decisions during the training process.

![image](https://github.com/user-attachments/assets/ddd3974e-4d52-45f5-ab44-d0cabd4d6260)

## 5.) Conclusion
Given the accuracy score calculated above (~0.964), I believe the XGBClassifier to be an effective model for predicting airline satisfaction given the features provided in the dataset.

Additionally, according to the feature importance figure above, I conclude that flight distance and age are the most important features in predicting airline satisfaction by a considerable margin. I believe flight distance and age to be significant indicators, as any positive or negative aspects of a certain airline are only further emphasized by the length of a flight and also the age of the passenger. Many of the features are ratings of various on-flight ammenities, which hold a greater importance the longer the flight is. Similar logic can be used to explain the importance of age, as the older a passenger is, the more likely they would prefer higher quality ammenities.

While passenger age and flight distance are not variables airlines have direct control over, I believe it would be in their best interest to put greater emphasis on properly serving elderly passengers and passengers on long-distance flights.

Besides these features, wifi rating and arrival delay appear to be the most important features amongst variables within the airlines' direct control. I believe this to be the case as wifi is often offered as a paid service, and as a result, customers may be more sensitive to poor wifi quality as opposed to other on-flight services which are included with the ticket, such as food and drink or entertainment. I believe arrival delay is a significant feature, as frequent delays can have a significant negative impact on customers, such as missing connecting flights and other scheduled public transportation such as airport buses.











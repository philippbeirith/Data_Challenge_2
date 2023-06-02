import pandas as pd
import xgboost as xg
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

import sqlite3



sqliteConnection = sqlite3.connect('data/crime_data')        
read_in = pd.read_sql_query("""SELECT *
                            FROM street
                            WHERE Month >= 2020-01""", sqliteConnection)  
data = read_in[read_in['Month'] >= '2020-01']

save = data

#######################
# Data Formatting     #
#######################

data = data.sort_values(by=['LSOA name', 'Month'])
monthle = LabelEncoder()
monthle.fit(data['Month'])
data['Month'] = monthle.transform(data['Month'])

LSOAle = LabelEncoder()
LSOAle.fit(data['LSOA name'])
data['LSOAencoded'] = LSOAle.transform(data['LSOA name'])


preprocess = data[['Month', 'LSOAencoded', 'Crime type', 'Index']]
preprocess.sort_values(by=['LSOAencoded', 'Month'])
preprocess = preprocess.groupby(['LSOAencoded', 'Month', 'Crime type']).count()

#This is to group by first LSOAcode and then month to achieve counts of different crimes
processed = preprocess.unstack(level=2)
processed = processed.fillna(0)
processed = processed['Index']

#Here the target column is created and the Burglary values are shifted by 1 index, such that for each month, gets
#the previous month's burglary amount. Then the first months are dropped, since we have garbage in those fields.
processed['target'] = -1
prevburglary = -1
for index in processed.index:
    if(prevburglary == -1):
        prevburglary = processed['Burglary'][index[0]][index[1]]
    else:
        processed['target'][index[0]][index[1]] = prevburglary
        prevburglary = processed['Burglary'][index[0]][index[1]]

for index in processed.index:
    if(index[1] == 0):
        processed = processed.drop([index])

#Here we reset the index, such that the LSOAcodes and months no longer are indexes, so that we can use them as features.
processed = processed.reset_index().sort_values(by=['Month', 'LSOAencoded'])

processed['Year'] = np.floor(processed['Month'] / 12)
processed['Month'] = processed['Month'] % 12

y_true = processed[(processed['Month'] + processed['Year']*12) > 30]['target']

#Here we are scaling the features, to accomodate XGBoost's requirements for features. We are creating vectors for machine learning.
features = ['LSOAencoded', 'Year', 'Month', 'Anti-social behaviour', 'Bicycle theft', 'Burglary', 'Criminal damage and arson', 
            'Drugs', 'Other crime', 'Other theft', 'Possession of weapons', 'Public order', 'Robbery', 'Shoplifting',
           'Theft from the person', 'Vehicle crime', 'Violence and sexual offences']
scaler = MinMaxScaler()
array = processed[features]
array[features] = scaler.fit_transform(processed[features])

y_true.reset_index()

#Assigning the training and testing datasets, with a circa 80-20 split
X_train = array[:6319]
y_train = processed[(processed['Month'] + processed['Year']*12) <= 30]['target']
X_test = array[6319:]
y_test = processed[(processed['Month'] + processed['Year']*12) > 30]['target']

#######################
#        Model Setup  #
#######################

# create model
model = xg.XGBRFRegressor(n_estimators=200, max_depth=12, learning_rate=1)#objective='binary:logistic')
# fit model
model.fit(X_train, y_train)
# make predictions
preds = model.predict(X_test)
preds

#Create output dataframe
output = processed[(processed['Month'] + processed['Year']*12) > 30][['Year', 'Month', 'LSOAencoded', 'target']]
output['predictions'] = preds
output
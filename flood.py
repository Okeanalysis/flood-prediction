import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score
import xgboost as xgb


flood = pd.read_csv('train.csv')
x = flood.iloc[:, 1:-1].values
y= flood.iloc[:, -1].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
model = xgb.XGBRegressor(objective= 'reg:squarederror',random_state=0)
param_grid={
    'learning_rate': [0.01, 0.1, 0.3],
    'max_depth': [3, 5, 7],
    'min_child_weight': [1, 3, 5],
    'gamma': [0.0, 0.1, 0.2],
    'reg_alpha': [0.0, 0.1, 0.5],
    'reg_lambda': [0.0, 0.1, 0.5]
}
grid_search= GridSearchCV(estimator= model, param_grid=param_grid, cv=3,scoring='r2')
grid_search.fit(x_train, y_train)
best_params = grid_search.best_params_
print("Best parameters:", best_params)

# Train the model with the best parameters
model.set_params(**best_params)
model.fit(x_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(x_test)

# Calculate R-squared score
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

test= pd.read_csv('test.csv')
test_ids= test['id']
way= test.drop('id',axis=1)
prediction= model.predict(way)
result= pd.DataFrame({'id':test_ids,'prediction':prediction})
result.to_csv('submission.csv',index=False)

#%%     Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics


#%%     Variables

file_path = "data\sleep_study\cmu-sleep.csv"

features = [ 'avg_together_percentage',
               'avg_working_percentage',
                 'number_of_people'
               ]

col_to_predict = 'avg_happy_rating'


#%%
data = pd.read_csv(file_path)

data = data.drop('cohort', axis=1)
print(data.dtypes)

#%%
# Compute the correlation matrix
correlation_matrix = data.corr()

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Matrix')
plt.show()

# %%    Scaling
scaler = StandardScaler()
data[features] = scaler.fit_transform(data[features])

#%%     Split the data

X = data[features]
y = data[col_to_predict]  # or 'happy_percentage'
# Drop rows with NaN in either X or y
combined = pd.concat([X, y], axis=1)  # Combine X and y into one DataFrame
combined = combined.dropna()  # Drop rows where any value is NaN
# Split back into X and y
X = combined[features]
y = combined[col_to_predict]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#%% 
#%%     Train the model
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X_train, y_train)



#%% evaluate the model
predictions = model.predict(X_test)
mae = metrics.mean_absolute_error(y_test, predictions)
r2 = metrics.r2_score(y_test, predictions)
print(f"MAE: {mae}, R²: {r2}")


#%% Extract key features
feature_importance = model.feature_importances_
plt.barh(features, feature_importance)
plt.title('Feature Importance')
plt.show()

# %%

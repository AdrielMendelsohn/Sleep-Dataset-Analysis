
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


import cleaning

#     Variables

features = [ "TotalSleepTime",
               "bedtime_mssd",
                 "midpoint_sleep",
                 "study",
                  "daytime_sleep"
               ]

col_to_predict = "score"

def clean_model_data(file_path):

  data = pd.read_csv(file_path)

  # Make new feature - weighted score (0-100)

  data["score"] = data.groupby("study")["term_gpa"].transform(lambda x: 25 * x)
  # Scaling according to specific Universities scores
  data["score_scaled"] = data.groupby("study")["term_gpa"].transform(
      lambda x: 100 * (x - x.min()) / (x.max() - x.min())
  )
  #  Clean the data
  data = data.drop("cohort", axis=1)

  data = cleaning.drop_blanks_and_nulls(data)


  data = data.apply(pd.to_numeric, errors="coerce")

  data = data[data["study"] != 5]
  # Delete outliers
  data = data[data["bedtime_mssd"]<= 5]
  data = data[data["daytime_sleep"]<= 150]

  #   Scaling
  scaler = StandardScaler()
  data[features] = scaler.fit_transform(data[features])

  return data

def train_model(data):
  #     Split the data
  X = data[features]
  y = data[col_to_predict]  # or 'happy_percentage'

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

  #     Train the model
  model = RandomForestRegressor(random_state=42)
  model.fit(X_train, y_train)

  # evaluate the model
  predictions = model.predict(X_test)
  mae = metrics.mean_absolute_error(y_test, predictions)
  r2 = metrics.r2_score(y_test, predictions)
  print(f"MAE: {mae}, R²: {r2}")
  return model

def predict_user_input(model):
    """Get user input for features, preprocess them, and make predictions using the trained model."""
    print("\nProvide the following inputs for prediction:")
    user_inputs = []

    # Prompt the user to enter values for each feature
    for feature in features:
        while True:
            try:
                value = float(input(f"Enter value for {feature} (in minutes): "))
                user_inputs.append(value)
                break
            except ValueError:
                print(f"Invalid input. Please enter a numeric value for {feature}.")

    # Convert inputs to a DataFrame
    user_data = pd.DataFrame([user_inputs], columns=features)

    # Apply the same scaling used during training
    scaler = StandardScaler()
    scaled_user_data = scaler.fit_transform(user_data)

    # Make the prediction
    prediction = model.predict(scaled_user_data)
    print(f"\nPredicted {col_to_predict}: {prediction[0]:.2f}")

    return prediction[0]



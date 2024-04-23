import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

data = pd.read_csv('/Users/Bindiya/SER517/mergedData.csv')
data['started_at'] = pd.to_datetime(data['started_at'])

def get_part_of_day(hour):
    return (
        "Morning" if 5 <= hour <= 11
        else "Afternoon" if 12 <= hour <= 17
        else "Evening" if 18 <= hour <= 22
        else "Night"
    )

data['time_of_the_day'] = data['started_at'].dt.hour.apply(get_part_of_day)

# Extract 'day_of_the_week'
data['day_of_the_week'] = data['started_at'].dt.day_name()

# Determine 'season'
def get_season(month):
    return (
        "Winter" if month in (12, 1, 2)
        else "Spring" if month in (3, 4, 5)
        else "Summer" if month in (6, 7, 8)
        else "Autumn"
    )

data['season'] = data['started_at'].dt.month.apply(get_season)

# One-hot encode categorical variables
encoder = OneHotEncoder(drop='first', sparse=False)  # drop='first' to avoid multicollinearity
categorical_features = data[['member_casual', 'time_of_the_day', 'day_of_the_week', 'season']]
encoded_features = encoder.fit_transform(categorical_features)

encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names(['member_casual', 'time_of_the_day', 'day_of_the_week', 'season']))

data = pd.concat([data.drop(['member_casual', 'time_of_the_day', 'day_of_the_week', 'season'], axis=1), encoded_df], axis=1)

X = data.drop('rideable_type', axis=1)
y = data['rideable_type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

conf_matrix = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{conf_matrix}")

class_report = classification_report(y_test, y_pred)
print(f"Classification Report:\n{class_report}")
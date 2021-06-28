from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor


data = pd.read_csv('data/f_dataset.csv')
try:
    data.drop('Unnamed: 0',axis=1,inplace=True)
except:
    pass

features = ['time','age','nb_of_runs','main_platform','main_genre','engine','developer','publisher']
label = 'TAS_time'

X = data[features]
y = data[label]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
X_train.reset_index(inplace=True,drop=True)
X_test.reset_index(inplace=True,drop=True)
y_train.reset_index(inplace=True,drop=True)
y_test.reset_index(inplace=True,drop=True)

# Create a categorical boolean mask
categorical_feature_mask = X_train.dtypes == object
# Filter out the categorical columns into a list for easy reference later on in case you have more than a couple categorical columns
categorical_cols = X_train.columns[categorical_feature_mask].tolist()

ohe = OneHotEncoder(handle_unknown='ignore', sparse = False)

df = ohe.fit_transform(X_train[categorical_cols])

#Create a Pandas DataFrame of the hot encoded column
ohe_df = pd.DataFrame(df, columns = ohe.get_feature_names(input_features = categorical_cols))
#concat with original data and drop original columns
df_ohe = pd.concat([X_train, ohe_df], axis=1).drop(columns = categorical_cols, axis=1)

# The following code is for your newdf after training and testing on original df
# Apply ohe on newdf
cat_ohe_new = ohe.transform(X_test[categorical_cols])
#Create a Pandas DataFrame of the hot encoded column
ohe_df_new = pd.DataFrame(cat_ohe_new, columns = ohe.get_feature_names(input_features = categorical_cols))
#concat with original data and drop original columns
df_ohe_new = pd.concat([X_test, ohe_df_new], axis=1).drop(columns = categorical_cols, axis=1)



xgr = GradientBoostingRegressor(random_state=0,learning_rate=0.051,max_depth=4,criterion='friedman_mse',loss='lad')
model = xgr.fit(df_ohe,y_train)


# predict on df_ohe_new
predict = model.predict(df_ohe_new)

print(predict)
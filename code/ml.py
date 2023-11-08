import pandas as pd
import gtfs_kit as gk
import helper #homemade function file helper.py
import warnings
import numpy as np
from lazypredict.Supervised import LazyRegressor
from sklearn.model_selection import train_test_split

main_dataset = pd.read_csv("../processed_files/main_dataset.csv", index_col=[0])
main_dataset.head(1)

print(main_dataset.shape )
X = main_dataset.drop(['ritardo_totale'], axis=1)
Y = main_dataset['ritardo_totale']
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 64)

#reg = LazyRegressor(verbose=0, ignore_warnings=True, custom_metric=None)
#models,pred = reg.fit(X_train, X_test, y_train, y_test)
#models

print(models)
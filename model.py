import pandas as pd
import numpy as np

DACIA_PATH = "/home/serhat/Desktop/dacia/"

def load_dacia_data(csv_name):
    return pd.read_csv(DACIA_PATH+csv_name+".csv")

#%% Preprocessing
from sklearn.model_selection import StratifiedShuffleSplit

def preprocessing(dacia):
    
    dacia = dacia.fillna(0)
    
    unnecessary_column_names = ["marka","Unnamed: 0","ilan_no","aciklama","ilan_tarihi","cekis","plaka","kimden",
                           "durum","baslik"]
    for col in dacia.columns: 
        count = (dacia[col] == 0).sum()
        if count > 800:
            unnecessary_column_names.append(col) 
    
    dacia = dacia.drop(unnecessary_column_names,axis = 1)
    
    train = pd.get_dummies(data=dacia, columns=['seri','model_1',"model_2","sehir","yakıt","kasa_tipi","motor_gucu",
                                            "motor_hacmi","renk","vites"])
    train = train.replace(to_replace=["Evet","Hayır"],value=[1,0])
    train["fiyat"] = 1000 * train["fiyat"]

    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    
    for train_index, test_index in split.split(train, dacia["seri"]):
        strat_train_set = train.loc[train_index]
        strat_test_set = train.loc[test_index]
        
    y_train =  strat_train_set["fiyat"]
    x_train = strat_train_set.drop(["fiyat"],axis = 1)

    y_test = strat_test_set["fiyat"]
    x_test = strat_test_set.drop(["fiyat"],axis = 1)
    
    return x_train,y_train,x_test,y_test

#%%
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import cross_val_score


# def forest_reg(x_train,y_train,x_test,y_test):
    
#     forest_reg = RandomForestRegressor(n_estimators=60,max_features=100)
#     forest_reg.fit(x_train,y_train)
#     scores = cross_val_score(forest_reg, x_test, y_test,scoring="neg_mean_squared_error", cv=10)
#     rmse_scores = np.sqrt(-scores)
    
#     print("Random Forest Regressor CV(10) RMSE Score : ",rmse_scores)
#%%



#%%
from sklearn.ensemble import RandomForestRegressor
import pickle

dacia = load_dacia_data("dacia_df")

x_train,y_train,x_test,y_test = preprocessing(dacia)
# forest_reg(x_train,y_train,x_test,y_test)

forest_reg = RandomForestRegressor(n_estimators=60,max_features=100)
forest_reg.fit(x_train,y_train)

filename = 'finalized_RFR_model.sav'
pickle.dump(forest_reg, open(filename, 'wb'))
 
























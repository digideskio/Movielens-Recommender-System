'''
Created on May 31, 2015

@author: Greg
'''

import pandas as pd
import sqlite3
from build_dataframe import build_dataframe

#comes from user_profile module
user_dict = {'50':5,
             '258': 4,
             '100':4,
             '181':5,
             '294':5,
             '286':4,
             '288':5, 
             '1':4,
             '300':4,
              '121':4, 
             '174':5, 
             '127':1, 
             '56':5,
              '7':5, 
             '98':3,
              '237':5, 
             '117':4, 
             '172':4, 
             '222':5, 
             '204':3}

#comes from Movie_Data_Frames module
rated_movies = ('50', '258', '100', '181', '294', '286', '288', '1', '300', '121', '174', '127', '56', '7', '98', '237', '117', '172', '222', '204')
df = build_dataframe(user_dict)


def build_evaluation_file(user_dict, k):
    """Takes dict input of user ratings and returns csv of to calculate error"""
    try:
        new_df = pd.DataFrame(list(user_dict.items()),columns = ['Movie ID', 'Ratings'])
        user_tr = new_df.set_index(['Movie ID']) #Application user's movie ratings in data frame
        
        #Create transposed versions of these dataframes in order to use the correlation method available in Pandas
        
        
        #df is the queried dataframe built using the build_dataframe function in line 35
        mean_df = df.fillna(df.mean())#fill missing ratings with the mean rating across other users for each film.
        df_tr = mean_df.transpose()

        #Create objects to be used to calculate correlations
        user_list = pd.Series(df.index.values)

        # user_list = user_list[:-1]#################Why?
        corr_list = pd.Series() #Series of correlations between user and dataset users
            
        for i in user_list: # i is the user id for all users we are comparing to
            try:
                corr_value = user_tr['Ratings'].corr(df_tr[i]) #find correlation value between ratings vector for each user and the application custer
                corr_list.set_value(i, corr_value) 
            except Exception as e:
                print(e)
           
        #Concatenate calculated correlations to the end of the existing user dataframe.  So each user has a correlation with app user
        mean_df.loc[:,-1] = corr_list  #User Correlation Column
        mean_df.columns.values[-1] = "User_Cor" 
        
        #Define K-number for neighbors
        
        df_knn = mean_df.sort([-1], ascending = False) #Sort the correlations for NU1 and NU2 to find K-NN
        
        mean_df.to_csv("Ratings with Correlations.csv", header = True)  

    except Exception as e:
        import sys 
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)
        print(e)
build_evaluation_file(user_dict, 3)
print('done')

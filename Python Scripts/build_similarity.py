'''
Created on May 11, 2015

@author: Greg
'''
import pandas as pd
from build_profile import build_profile
from build_dataframe import build_dataframe

def build_similarity(user_dict, df, k):
    """Takes dict input of user ratings, dataframe for users who rated movies, and K value for neighbors and returns the k nearest neighbors in the user Database"""
    try:
        new_df = pd.DataFrame(list(user_dict.items()),columns = ['Movie ID', 'Ratings']) #create dataframe for dictionary of user ratings
        user_tr = new_df.set_index(['Movie ID']) #Application user's movie ratings in data frame
        user_tr = user_tr.astype(float) 
        #df is the queried dataframe built using the build_dataframe function in line 35
        mean_df = df.fillna(df.mean())#fill missing ratings with the mean rating across other users for each film.
        df_tr = mean_df.transpose()#Create transposed versions of the dataframe in order to use the correlation method available in Pandas
        df_tr = df_tr.astype(float)#set type as float for correlation calculation
        
        #Create objects to be used to calculate correlations
        user_list = pd.Series(df.index.values)
        corr_list = pd.Series() #Series of correlations between user and dataset users
            
        for i in user_list: # i is the user id for all users we are comparing to
            try:  
                corr_value = user_tr['Ratings'].corr(df_tr[i]) #find correlation value between ratings vector for each user and the application custer
                corr_list.set_value(i, corr_value)  #create list of correlation values
            except Exception as e:
                print(e)
                print('error in build similarity')
           
        #Concatenate calculated correlations to the end of the existing user dataframe.  So each user has a correlation with app user
        mean_df.loc[:,-1] = corr_list  #User Correlation Column
        mean_df.columns.values[-1] = "User_Cor" 
        df_knn = mean_df.sort([-1], ascending = False) #Sort the correlations for NU1 and NU2 to find K-NN
        knn = {}
        for i in range(k):
            knn[df_knn.iloc[:k,:].index[i]] = df_knn.iloc[i,-1]
        return(knn) #knn contains the user IDs of neighbors and the correlation values 
    except Exception as e:
        import sys 
        tb = sys.exc_info()[2]
        print(tb.tb_lineno)
        print(e)


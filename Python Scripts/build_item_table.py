'''
Created on Jun 4, 2015

Create database table of correlations between items (movies) to query based on user profile

@author: Greg
'''
import sqlite3
import pandas as pd 


def build_item_table():
    '''takes no argument, returns nothing. Purpose is to add table to db with correlations between items'''
    con_lite = sqlite3.connect("Movies.db")
    cur = con_lite.cursor()
    try:  
        print('Calculating similarities between all movies...')
        all_movies = cur.execute("""
             SELECT DISTINCT movieID, COUNT(*)
             FROM Ratings
             GROUP BY movieID
             HAVING COUNT(*) > 35""")   
        
        movies = all_movies.fetchall() #This query gets movie IDs for all movies in dataset to act as columns for DataFrame
        movie_list = []
        for i in movies:
            movie_list.append(i[0])               
        movie_frame = pd.DataFrame(columns = movie_list)       
        all_ratings = cur.execute("""
             SELECT userID, movieID, Rating
             FROM Ratings
             WHERE movieID IN """+ str(tuple(movie_list)) + """;""")   
        
        ratings = all_ratings.fetchall() # This query gets all ratings for all movies to put in a DataFrame
        con_lite.commit()
        con_lite.close()

        match_count = 0 
        for r in ratings:
            try:
                movie_frame.loc[r[0],r[1]] = r[2]
                match_count += 1
            except Exception as e:
                print(e)

        mean_df = movie_frame.fillna(movie_frame.mean())
        corr_movies = mean_df.corr()
        
        #Put correlations into data frame so they can transferred to database for offline storage
        c_table =pd.DataFrame(columns = ['ID', 'Correlation'])
        temp_table = pd.DataFrame(columns = ['ID','Correlation'])
        for i in movie_list:
            temp_table['ID'] = str(i)
            temp_table['Correlation'] = corr_movies[i]
            c_table = c_table.append(temp_table)
        c_table = c_table.fillna(movie_list[0])#The first ID was NA for some reason, filled with the first ID to fix this           
        
        con_lite = sqlite3.connect("Movies.db")
        cur = con_lite.cursor()
        c_table.to_sql(name='MovieCorr',con= con_lite,schema='ID text, Correlation float', if_exists='replace', index_label='ID1') #create table in DBfrom data frame
        mean_df.to_csv("All Movies Ratings.csv", header = True)  
        corr_movies.to_csv("All Movies Correlated.csv", header = True)         
    except Exception as e:
        print(e)  
        print('error in build_item_table') 
    con_lite.commit()
    con_lite.close()

print(build_item_table())

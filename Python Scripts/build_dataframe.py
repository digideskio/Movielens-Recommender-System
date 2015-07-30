'''
Created on May 8, 2015

@author: Greg
'''
import sqlite3
import pandas as pd 
from build_profile import build_profile

def build_dataframe(rated_movies):
    '''Accepts dict of 20 movie IDs in the MovieLens Dataset'''
    rated_movies = list(rated_movies.keys()) #List of movie IDs that the app user rated

    con_lite = sqlite3.connect("Movies.db") # created in build_db
    cur = con_lite.cursor()
    try:  
        users = cur.execute("""
            SELECT userID, movieID, Rating
            FROM Ratings
            WHERE movieID IN
            """ + str(tuple(rated_movies)) + """ 
            ORDER BY userID""")   #Query to Database based on items rated by the app's user
        users = users.fetchall()
        rated_movie_frame = pd.DataFrame(columns = rated_movies) #create dataframe for user profile to store other users ratings
        for user in users:
            try:
                if user[1] in rated_movies:
                    rated_movie_frame.loc[user[0],user[1]] = user[2] #Assigns the rating (user2) to user id row (user0) and item column(user1)
            except Exception as e:
                print(e) 
        return(rated_movie_frame)
    except Exception as e:
        print(e)  
        print('error in build dataframe') 
    con_lite.commit()
    con_lite.close()
    


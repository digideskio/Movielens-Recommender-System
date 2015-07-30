'''
Created on May 31, 2015

@author: Greg
'''
import pandas as pd
import sqlite3
from build_profile import build_profile
from build_dataframe import build_dataframe
from build_similarity import build_similarity


def sortCollection(c):
    '''returns a list of lists, if c is a list, or a list of tuples, if c is a dict, sorted in decreasing order of the elements of index 1 or according to decreasing order of values.'''
    #Function created by Professor Gian Mario Besana  Ph.D. of DePaul
    import operator
    if type(c) is dict:
        c = list(c.items())
    return(sorted(c, key =operator.itemgetter(1), reverse=True))

def find_movies(user_dict, neighbors):
    rated_tup = tuple(user_dict.keys())
    k_neighbors = tuple(neighbors.keys())
    con_lite = sqlite3.connect("Movies.db")
    cur = con_lite.cursor()
    try:     
        users = cur.execute("""
            SELECT Ratings.movieID,Ratings.userID, Ratings.Rating
            FROM Ratings, Movies
            WHERE userID IN """ + str(k_neighbors) + """
            AND Ratings.movieID NOT IN """ + str(rated_tup) + """
            AND Ratings.movieID = Movies.movieID
            ORDER BY Rating DESC; """) #Query returns movies that the neighbors rated that the app user did not
        
        predicted_ratings = {}
        k_corrs = {}
        for i in users:
            if i[0] not in predicted_ratings:
                predicted_ratings[i[0]] = neighbors[i[1]] * i[2]  #Calculates weight from neighbor correlation value brought into function
                k_corrs[i[0]] = neighbors[i[1]]  #create list to track which neighbors rated the film in a dict with key for each movie 
            else:
                predicted_ratings[i[0]] = predicted_ratings[i[0]] + (neighbors[i[1]] * i[2]) # This adds the rating weighted by the other user's correlation value
                k_corrs[i[0]] += neighbors[i[1]]
        
        final_ratings = {}  #Calculates weighted average for each predicted rating
        for i in predicted_ratings:
            final_ratings[i] = predicted_ratings[i] / k_corrs[i]

        return(sortCollection(final_ratings))
    except Exception as e:
        print(e)
        print('error in find movies')
    con_lite.commit()
    con_lite.close()
    




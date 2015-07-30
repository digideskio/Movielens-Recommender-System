'''
Created on Jun 5, 2015

@author: Greg
'''
import sqlite3
from build_profile import build_profile
from find_movies import sortCollection

def item_item(user_dict, k):
    con_lite = sqlite3.connect("Movies.db")
    cur = con_lite.cursor()
    try:     
        all_items = tuple(user_dict.keys())             
        items = cur.execute("""
                SELECT ID Predicted, ID1, Correlation 
                FROM MovieCorr
                WHERE ID1 IN """ + str(all_items) + """
                AND Predicted NOT IN """ + str(all_items) + """
                AND Correlation <> 1
                AND Correlation > 0
                ORDER BY Predicted DESC, Correlation DESC; """) 
        
        all = items.fetchall()
        counter_dict = {}
        predicted_ratings = {}
        k_corrs = {}
        for i in all:  
            if i[0] not in counter_dict:
                counter_dict[i[0]] = 1
            else:
                counter_dict[i[0]] += 1
            
            if counter_dict[i[0]] < k: 
                if i[0] not in predicted_ratings:
                    predicted_ratings[i[0]] = user_dict[i[1]] * i[2]  #Calculates weight from correlation value brought into function
                    k_corrs[i[0]] = i[2]  #create list to track which neighbors rated the film in a dict with key for each movie 
                else:
                    predicted_ratings[i[0]] = predicted_ratings[i[0]] + (user_dict[i[1]] * i[2]) # This adds the rating weighted by the other user's correlation value
                    k_corrs[i[0]] += i[2]
        final_ratings = {}
        for i in predicted_ratings:
            final_ratings[i] = predicted_ratings[i] / k_corrs[i]               
        return(sortCollection(final_ratings))       
    except Exception as e:
        print(e)
        print('error in item_item')
    con_lite.commit()
    con_lite.close() 

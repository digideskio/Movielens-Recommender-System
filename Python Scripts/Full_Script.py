'''
Created on Jun 3, 2015

@author: Greg
'''
from build_profile import build_profile
from build_dataframe import build_dataframe
from build_similarity import build_similarity
from find_movies import find_movies
from genres import select_genres
from item_item import item_item

#####################initial setup #########################################
build_db() # Create Database from flat MovieLens files
build_item_table() #Create new table in DB for item-item filtering

def display_films(movie_list):
    '''Prints Movie List for user 10 films at a time and gives user option to exit'''
    cont = 'y'
    multiple = 1
    for film in range(len(movie_list)):
        if (film < (10 * multiple) and cont.lower()) == 'y':
            print(final_picks[film])
        elif len(final_picks) > 10:
            cont = input("Enter 'y' if you would like to see more films:\n ")
            if cont.lower()  == 'y':
                multiple +=1
            else:
                return(print("Thank you for using this service."))
                break

while True:
    user_dict = build_profile() #Function prompts uses to rate 20 movies.  The films presented have the largest number of reviews in the database
    k = eval(input("How many neighbors should be used for the recommendations? (k)")) #This is used for User CF and Item CF
    print("This should take a few seconds...finding great movies for you!")
    movie_df = build_dataframe(user_dict) #The dataframe is based on a query in the database getting ratings for all users who rated the same movies as the application's user
    cf_neighbors = build_similarity(user_dict, movie_df, k)#returns the nearest neighbors for the app user and their correlations 
    cf_movies = find_movies(user_dict,cf_neighbors) #returns movies with predicted ratings for the user
    
    final_picks = select_genres(cf_movies)#gives the app's user the choice to request films of a certain genre
    print(display_films(final_picks)) 
    
    e = input("I hoped those movies look good.  I'm going to try another way to find movies for you, press enter to start the process:\n")
    print("This should take a few seconds...finding great movies for you!")
    item_movies = item_item(user_dict, k) #Returns movies that are similar to items rated by the app user along with predicted rating
    
    final_picks = select_genres(item_movies)#gives the app's user the choice to request films of a certain genre
    print(display_films(final_picks))       
    
    
    e = input("I hoped those movies look good. \n Press 0 if you would like to exit or any key to start the process over:\n\n")
    if e == '0':
        print('Thank you!  Goodbye!')
        break
    
'''
Created on Jun 6, 2015

@author: Greg
'''

import sqlite3
from find_movies import sortCollection
from operator import itemgetter

def select_genres(movie_tuples):
    '''accepts list of movie ids, prompts user for genre preferences and then gives movies in that genre'''
        #Add function to allow user to chose genre 
        #Use this as an alternative way to build user profile with genre preferences 
    con_lite = sqlite3.connect("Movies.db")
    cur = con_lite.cursor()
    movie_dict = {}
    for i in movie_tuples:
        movie_dict[i[0]] = i[1]   
    movie_list = list(movie_dict.keys())
    try:   
        input('''\nYour profile is built and I have movies to recommend you, but I need to know if you are in the mood for a certain type of film.
        
I will show a list of all the movie genres available.  Please enter the number of the genre you would like to see films for.
        
Press any key to see the list of genres: \n 
        ''')
        all_genres = ['0. Any Genre', '1. Action','2. Adventure','3. Animation',"4. Children's",'5. Comedy','6. Crime','7. Documentary','8. Drama','9. Fantasy','10. Film-Noir','11. Horror','12. Musical','13. Mystery','14. Romance','15. Sci-Fi','16. Thriller','17. War','18. Western']
        for i in all_genres:
            print(i, end = '\n')    
        all_g = {    
                1:'Action',
                2:'Adventure',
                3:'Animation',
                4:'Children',
                5:'Comedy',
                6:'Crime',
                7:'Documentary',
                8:'Drama',
                9:'Fantasy',
                10:'FilmNoir',
                11:'Horror',
                12:'Musical',
                13:'Mystery',
                14:'Romance',
                15:'SciFi',
                16:'Thriller',
                17:'War',
                18:'Western'   }
        
        while True:
            try: 
                genre = input('''Which genre would you like to watch?\n''')
                if eval(genre) >=1 and eval(genre) <=18:
                    picked_genre = all_g[eval(genre)]
                    items = cur.execute("""
                        SELECT DISTINCT Title, Year, Movies.movieID
                        FROM Genres, Movies
                        WHERE Genres.movieID  = Movies.movieID
                        AND Movies.movieID IN """ + str(tuple(movie_list)) + """
                        AND """ + str(picked_genre) + """ = 1; """) 
                    picked_movies = items.fetchall() 
                    if len(picked_movies) == 0:
                        print('Sorry! I do not have any films to recommend in that genre, please choose again.\n')    
                    else:
                        break
                elif eval(genre) == 0: 
                        items = cur.execute("""
                        SELECT DISTINCT Title, Year, Movies.movieID
                        FROM Genres, Movies
                        WHERE Genres.movieID  = Movies.movieID
                        AND Genres.movieID IN """ + str(tuple(movie_list)) + """ """)
                        picked_movies = items.fetchall() 
                        break
                else:
                    print('Please enter a number from 1 to 18 for the genre you would like to see films for!')                        
            except Exception as e:
                print('Something went wrong - please enter a number from 1 to 18 to select the genre you would like to see films for!')
                print(e)
    except Exception as e:
        print(e)
        print('error in genres')
    
    con_lite.commit()
    con_lite.close()
    picked_list = []
    for i in picked_movies:  
        l = list(i)
        l[2] = movie_dict[i[2]]
        picked_list.append(l)
        
    picked_list = sorted(picked_list, key=itemgetter(2), reverse = True)
    return(picked_list)
    

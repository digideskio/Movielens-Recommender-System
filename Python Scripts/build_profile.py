'''
Created on Jun 3, 2015

@author: Greg
'''
import sqlite3

def build_profile():
    '''Builds a user profile with movie ratings in order to create collaborative based recommendations
            Returns Dictionary of movie IDs and corresponding Ratings.'''
    con = sqlite3.connect('Movies.db')#Load movie data into DB
    cur = con.cursor()
    try:
        cur.execute("""SELECT Ratings.movieID, title, year, COUNT(*) FROM Ratings, Movies
                   WHERE Movies.movieID = Ratings.movieID
                   GROUP BY Ratings.movieID ORDER BY COUNT(*) DESC LIMIT 100;""")
        input("""Hello! I would like to recommend movies for you, but I need you to first rate 20 films you have seen before.
        
Please rate the following films 1-5 with 5 being the highest.  If you have not seen the film before, enter a 0.
                
Press any key to continue:\n""")              
        user_profile = {}
        movies_reviewed = 0 
        rating_list = [0,1,2,3,4,5]
        for i in cur:
            print('\n' +i[1] + ', Released: ' + str(i[2]))
            while True:
                try:
                    rating = input("How do you rate {}? (1 - 5):\n\n".format(i[1]))
                    if eval(rating) in rating_list:
                        break
                    else:
                        print('Sorry! That is an invalid rating, please enter a value 0 - 5.')
                except:
                    print("Sorry! Something went wrong with your rating, please enter a value 0 - 5.")           
            if eval(rating) != 0:
                user_profile[i[0]] = int(rating)   #build dictionary with movie ID key and rating value
                movies_reviewed += 1
                if movies_reviewed == 20:
                    print("Great! You gave {} a rating of {}.  Your profile is complete!.".format(i[1],rating))
                    break
                print("Great! You gave {} a rating of {}.  You have {} movies left to review to complete your profile!.\n".format(i[1], rating, 20 - movies_reviewed))
            else:
                print("Looks like you missed that one.  Here is another film to rate.  Please enter a rating 1 - 5 if you have seen the film.")
    except Exception as e:
        print(e)
    con.commit()
    con.close()  
    return(user_profile)


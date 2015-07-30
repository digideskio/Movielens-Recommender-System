import sqlite3
import sys
import os

def find_data_file(filename):  #This function comes from CX Freeze website to use with external data when converting to EXE
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)

#used to find the file location for data distributed with script
r = find_data_file('ratings.data')
i = find_data_file('items.item')

def build_db():
    con = sqlite3.connect('Movies.db')#Create database to store movie and rating info for easy storage and querying
    cur = con.cursor()
    try:    
        cur.execute("DROP TABLE IF EXISTS Ratings")#create tables in DB
        cur.execute("CREATE TABLE Ratings (userID text, movieID text, Rating integer, timeStamp integer)")
        cur.execute("DROP TABLE IF EXISTS Movies")
        cur.execute("CREATE TABLE Movies (movieID text PRIMARY KEY, Title text, Year integer)")
        cur.execute("DROP TABLE IF EXISTS Genres")
        cur.execute("""CREATE TABLE Genres (movieID text, Unknown integer, Action integer, Adventure integer, Animation integer,Children integer,
        Comedy integer, Crime integer, Documentary integer, Drama integer, Fantasy integer, FilmNoir integer,
        Horror integer,Musical integer,Mystery integer,Romance integer,SciFi integer,Thriller integer,War integer,Western integer)""")
        print('Loading Ratings...')
        ratings = open(r)
        for line in ratings:
            insertTuple = tuple(line[:-1].split('\t'))
            cur.execute("INSERT INTO Ratings VALUES (?, ?, ?, ?)", insertTuple)
        print('Ratings Loaded') 
        print('Loading Movies...')   
        movies = open(i)
        for line in movies:
            tempList = line[:-1].split('|')
            if tempList[1] != "unknown": #Transform Genre data to prepare to load into table
                genreList = tempList[5:]
                genreList.insert(0, tempList[0])
                insertTuple = tuple(genreList)
                cur.execute("INSERT INTO genres VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", insertTuple)
               
                movieString = tempList[1]
                tempList[1] = movieString[:movieString.rindex('(')-1] #Separates movie title into attribute
                tempList[2] = eval(tempList[2][-4:]) #Uses year from date column from dataset
                insertTuple = tuple(tempList[:3])
                cur.execute("INSERT INTO movies VALUES (?, ?, ?)", insertTuple)       
        print('Movies Loaded')   
    except Exception as e:
        print(e)
    con.commit()
    con.close()

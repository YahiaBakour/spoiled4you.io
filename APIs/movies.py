from imdb import IMDb
import json
import re

class movies:
    def __init__(self):
        pass

    # create an instance of the IMDb class
    def getmoviesuggestions(self,MovieName):
        returnlist = []
        Spoilers = []
        ia = IMDb()
        movies = ia.search_movie_advanced(MovieName,results=5)
        for movie in movies:
            #returnlist.append({'title':movie['title'] ,'image' : movie['cover']})
            returnlist.append(movie['title'])

        return returnlist

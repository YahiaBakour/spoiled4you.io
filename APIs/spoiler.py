from imdb import IMDb
import sys
sys.path.append("APIs")
from Wikipedia import wikipedia
import json
import re

class Spoiler:
    def __init__(self):
        self.ListOfKeyWords = ['film','movie','cinema','feature','flick','picture']

    # Utility classes
    def ContainsYear(self,S):
        return bool(re.search('.*([1-3][0-9]{3})', S))

    def ContainsKeyWord(self,S):
        for keyword in self.ListOfKeyWords:
            if(keyword in S):
                return True
        return False


    # create an instance of the IMDb class
    def GenerateImdbSpoiler(self,MovieName):
        Spoilers = []
        ia = IMDb()
        movies = ia.search_movie_advanced(MovieName)
        movie = ia.get_movie(movies[0].movieID, info=['reviews'])
        reviews = movie.get('reviews', [])
        for review in reviews:
            Spoilers.append(review['content'])
        return Spoilers

    def GenerateWikipediaSpoiler(self,MovieName):
        spoiler = ""
        search_results = wikipedia.search(MovieName)
        if(len(search_results) == 1):
            plot = wikipedia.page(MovieName).section("Plot")
            if(plot is None):
                return wikipedia.page(search_results[0])
            return plot

        for possible_movie in search_results:
            if(self.ContainsYear(possible_movie) and self.ContainsKeyWord(possible_movie)):
                print(possible_movie)
                spoiler = wikipedia.page(MovieName).section("Plot")
                if(spoiler is None):
                    spoiler = wikipedia.page(MovieName).summary
            else:
                spoiler = wikipedia.page(MovieName).section("Plot")
                if(spoiler is not None):
                    return spoiler
                spoiler = wikipedia.page(MovieName).summary
        return spoiler

# print(GenerateWikipediaSpoiler("Goonies"))


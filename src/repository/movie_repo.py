from src.repository.repository_exception import RepositoryException
from src.domain.movie import Movie
import pickle
from src.domain.struct import Iterable, sort_data, filter_data


class MovieRepo:

    def __init__(self):
        self._movie_data = Iterable()

    def add_movie(self, movie):
        """
        function that adds a movie
        :param movie:
        :return:
        """
        for x in self._movie_data:
            if int(x.movie_id) == movie.movie_id:
                raise RepositoryException("The movie id already exists!")
        self._movie_data.append(movie)

    def remove_movie(self, movie_id):
        """
        function that removes a movie
        :param movie_id:
        :return:
        """
        for x in self._movie_data:
            if x.movie_id == movie_id:
                self._movie_data.remove(x)
                return
        raise RepositoryException("The movie id doesn't exist!")

    def update_movie(self, movie):
        """
        function that updates a movie
        :param movie:
        :return:
        """
        for x in self._movie_data:
            if x.movie_id == movie.movie_id:
                x.title = movie.title
                x.description = movie.description
                x.genre = movie.genre
                return
        raise RepositoryException("The movie id doesn't exist!")

    @staticmethod
    def compare_func(a, b):
        """
        function to compare
        :param a:
        :param b:
        :return: True or False
        """
        return int(a.movie_id) <= int(b.movie_id)

    def list_movie(self):
        """
        function that lists the movies
        :return: the list of movies
        """
        if len(self._movie_data) == 0:
            raise RepositoryException("There are no movies!")
        else:
            #return self._movie_data
            sort_data(self._movie_data, self.compare_func)
            return self._movie_data

    def existent_movie_id(self, movie_id):
        """
        function that checks if the movie_id exists
        :param movie_id:
        :return: True or False
        """
        for x in self._movie_data:
            if x.movie_id == movie_id:
                return True
        return False

    def search_movie_id(self, movie_id):
        """
        function that searches for a movie by movie_id
        :param movie_id:
        :return: the movie with that movie_id
        """
        if self.existent_movie_id(movie_id) == False:
            raise RepositoryException("The movie id doesn't exist!")
        else:
            #for x in self._movie_data:
                #if x.movie_id == movie_id:
                    #return x
            found = filter_data(self._movie_data, lambda x: x.movie_id == movie_id)
            return found[0]

    def search_title(self, title):
        """
        function that searches for a movie by title
        :param title:
        :return: the list of matches
        """
        matching = []
        for x in self._movie_data:
            #if x.title.lower() == title.lower() or title.lower() in x.title.lower():
                #matching.append(x)
            matching = filter_data(self._movie_data, lambda x: x.title.lower() == title.lower() or title.lower() in x.title.lower())
        if len(matching) == 0:
            raise RepositoryException("There is no match for a title!")
        else:
            #return matching
            sort_data(matching, self.compare_func)
            return matching

    def search_description(self, description):
        """
        function that searches for a movie by description
        :param description:
        :return: the list of matches
        """
        matching = []
        for x in self._movie_data:
            #if x.description.lower() == description.lower() or description.lower() in x.description.lower():
                #matching.append(x)
            matching = filter_data(self._movie_data, lambda x: x.description.lower() == description.lower() or description.lower() in x.description.lower())
        if len(matching) == 0:
            raise RepositoryException("There is no match for a description!")
        else:
            #return matching
            sort_data(matching, self.compare_func)
            return matching

    def search_genre(self, genre):
        """
        function that searches for a movie by genre
        :param genre:
        :return: the list of matches
        """
        matching = []
        for x in self._movie_data:
            #if x.genre.lower() == genre.lower() or genre.lower() in x.genre.lower():
                #matching.append(x)
            matching = filter_data(self._movie_data, lambda x: x.genre.lower() == genre.lower() or genre.lower() in x.genre.lower())
        if len(matching) == 0:
            raise RepositoryException("There is no match for a genre!")
        else:
            #return matching
            sort_data(matching, self.compare_func)
            return matching


class TextMovieRepo(MovieRepo):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            movie_id, title, description, genre = line.split(maxsplit=3, sep=';')
            movie = Movie(int(movie_id), title.rstrip(), description.rstrip(), genre.rstrip())
            self._movie_data.append(movie)

    def _save_file(self):
        f = open(self._file_name, "wt")
        for movie in self._movie_data:
            f.write(str(movie.movie_id) + ";" + movie.title + ";" + movie.description + ";" + movie.genre + "\n")
        f.close()

    def add_movie(self, movie):
        super(TextMovieRepo, self).add_movie(movie)
        self._save_file()

    def remove_movie(self, movie_id):
        super(TextMovieRepo, self).remove_movie(movie_id)
        self._save_file()

    def update_movie(self, movie):
        super(TextMovieRepo, self).update_movie(movie)
        self._save_file()

    def list_movie(self):
        return super(TextMovieRepo, self).list_movie()

    def existent_movie_id(self, movie_id):
        return super(TextMovieRepo, self).existent_movie_id(movie_id)

    def search_movie_id(self, movie_id):
        return super(TextMovieRepo, self).search_movie_id(movie_id)

    def search_title(self, title):
        return super(TextMovieRepo, self).search_title(title)

    def search_description(self, description):
        return super(TextMovieRepo, self).search_description(description)

    def search_genre(self, genre):
        return super(TextMovieRepo, self).search_genre(genre)


class BinMovieRepo(MovieRepo):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        try:
            self._movie_data = pickle.load(f)
        except EOFError:
            pass

    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._movie_data, f)
        f.close()

    def add_movie(self, movie):
        super(BinMovieRepo, self).add_movie(movie)
        self._save_file()

    def remove_movie(self, movie_id):
        super(BinMovieRepo, self).remove_movie(movie_id)
        self._save_file()

    def update_movie(self, movie):
        super(BinMovieRepo, self).update_movie(movie)
        self._save_file()

    def list_movie(self):
        return super(BinMovieRepo, self).list_movie()

    def existent_movie_id(self, movie_id):
        return super(BinMovieRepo, self).existent_movie_id(movie_id)

    def search_movie_id(self, movie_id):
        return super(BinMovieRepo, self).search_movie_id(movie_id)

    def search_title(self, title):
        return super(BinMovieRepo, self).search_title(title)

    def search_description(self, description):
        return super(BinMovieRepo, self).search_description(description)

    def search_genre(self, genre):
        return super(BinMovieRepo, self).search_genre(genre)

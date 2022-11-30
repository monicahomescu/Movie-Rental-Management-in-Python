class Movie:

    def __init__(self, movie_id, title, description, genre):
        self.__movie_id = movie_id
        self.__title = title
        self.__description = description
        self.__genre = genre

    @property
    def movie_id(self):
        return self.__movie_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def genre(self):
        return self.__genre

    @title.setter
    def title(self, new_title):
        self.__title = new_title

    @description.setter
    def description(self, new_description):
        self.__description = new_description

    @genre.setter
    def genre(self, new_genre):
        self.__genre = new_genre

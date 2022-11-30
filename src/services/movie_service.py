from src.domain.movie import Movie
from src.repository.repository_exception import RepositoryException
from src.services.undo_redo_service import Call, Operation, CascadeOperation
import random


class MovieService:

    def __init__(self, movie_repository, undo_redo_service):
        self.__movie_repo = movie_repository
        self.__undo_redo_serv = undo_redo_service

    def generate_movies(self):
        """
        function that generates movies
        :return:
        """
        list_movie_id = ['13', '49', '32', '48', '90', '34', '9', '18', '15', '22', '5', '2', '76', '35', '60', '38',
                         '4', '87', '7', '8']
        list_info = [
            ["Little Women", "The March sisters struggle to improve their various flaws as they grow into adults.",
             "Drama"],
            ["Fools Rush In",
             "Three months after a one-night stand with Isabel Fuentes in Las Vegas, New York City real estate developer Alex Whitman learns she is pregnant.",
             "Romance"],
            ["The Call",
             "A veteran operator for an emergency call-center, Jordan saves lives daily as part of her job, but when a young woman's frantic report of a prowler ends tragically, Jordan is devastated.",
             "Thriller"],
            ["Freaky",
             "When seventeen-year-old Millie Kessler becomes the latest target of the Butcher, the town's infamous serial killer, her senior year becomes the least of her worries.",
             "Horror"],
            ["The Guilty",
             "A troubled police detective demoted to 911 operator duty scrambles to save a distressed caller during a harrowing day of revelations -- and reckonings.",
             "Thriller"],
            ["Greenland",
             "John Garrity, his estranged wife and their young son embark on a perilous journey to find sanctuary as a planet-killing comet hurtles toward Earth.",
             "Action"],
            ["Mickey Blue Eyes",
             "English art dealer Michael Felgate is dumbfounded to learn that his girlfriend cannot accept his marriage proposal because her entire family is involved with the Mafia.",
             "Comedy"],
            ["No Escape",
             "American businessman Jack Dwyer, wife Annie and their two young daughters arrive in Southeast Asia and quickly learn that they're right in the middle of a political uprising.",
             "Action"],
            ["The Proposal",
             "Faced with deportation to her native Canada, high-powered book editor Margaret Tate says she's engaged to marry Andrew Paxton, her hapless assistant.",
             "Comedy"],
            ["A Quiet Place", "A family must live in silence to avoid mysterious creatures that hunt by sound.",
             "Horror"],
            ["Two Weeks Notice",
             "Dedicated environmental lawyer Lucy Kelson goes to work for billionaire George Wade as part of a deal to preserve a community center.",
             "Romance"],
            ["Notting Hill",
             "William Thacker is a London bookstore owner whose humdrum existence is thrown into romantic turmoil when famous American actress Anna Scott appears in his shop.",
             "Romance"],
            ["Knight and Day",
             "June Havens chats up her charming seatmate on a flight out of Kansas, but she doesn't realize that she will soon land in the middle of an international adventure.",
             "Comedy"],
            ["10 things i hate about you",
             "Kat Stratford is beautiful, smart and quite abrasive to most of her fellow teens, meaning that she doesn't attract many boys.",
             "Romance"],
            ["Black Widow",
             "Natasha Romanoff, aka Black Widow, confronts the darker parts of her ledger when a dangerous conspiracy with ties to her past arises.",
             "Action"],
            ["The Hitman's Bodyguard",
             "The world's top protection agent is called upon to guard the life of his mortal enemy, one of the world's most notorious hit men.",
             "Action"],
            ["Mamma Mia!",
             "Donna, an independent hotelier in the Greek islands, is preparing for her daughter's wedding with the help of two old friends.",
             "Musical"],
            ["The Theory Of Everything",
             "In the 1960s, Cambridge University student and future physicist Stephen Hawking falls in love with fellow collegian Jane Wilde.",
             "Drama"],
            ["All The Bright Places",
             "After meeting each other, two teenagers struggle with the emotional and physical scars of their pasts.",
             "Romance"],
            ["The Imitation Game",
             "In 1939, newly created British intelligence agency MI6 recruits Cambridge mathematics alumnus Alan Turing to crack Nazi codes.",
             "War"],
        ]
        for i in range(0, 20):
            movie_id = random.choice(list_movie_id)
            list_movie_id.remove(movie_id)
            random_info = random.choice(list_info)
            list_info.remove(random_info)
            title = random_info[0]
            description = random_info[1]
            genre = random_info[2]
            movie = Movie(movie_id, title, description, genre)
            self.__movie_repo.add_movie(movie)

    def add_movie(self, movie):
        """
        function that adds a movie
        :param movie:
        :return:
        """
        self.__movie_repo.add_movie(movie)
        undo_call = Call(self.__movie_repo.remove_movie, movie.movie_id)
        redo_call = Call(self.__movie_repo.add_movie, movie)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def remove_movie(self, movie_id):
        """
        function that removes a movie
        :param movie_id:
        :return:
        """
        self.__movie_repo.remove_movie(movie_id)

    def update_movie(self, movie):
        """
        function that updates a movie
        :param movie:
        :return:
        """
        old = self.search_movie_id(movie.movie_id)
        new = movie
        self.__movie_repo.update_movie(movie)
        undo_call = Call(self.__movie_repo.update_movie, old)
        redo_call = Call(self.__movie_repo.update_movie, new)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def list_movie(self):
        """
        function that lists the movies
        :return: the list of movies
        """
        return self.__movie_repo.list_movie()

    def search_movie_id(self, movie_id):
        """
        function searches for a movie by movie_id
        :param movie_id:
        :return: the movie with that movie_id
        """
        return self.__movie_repo.search_movie_id(movie_id)

    def search_title(self, title):
        """
        function that searches for a movie by title
        :param title:
        :return: the list of matches
        """
        return self.__movie_repo.search_title(title)

    def search_description(self, description):
        """
        function that searches for a movie by description
        :param description:
        :return: the list of matches
        """
        return self.__movie_repo.search_description(description)

    def search_genre(self, genre):
        """
        function that searches for a movie by genre
        :param genre:
        :return: the list of matches
        """
        return self.__movie_repo.search_genre(genre)

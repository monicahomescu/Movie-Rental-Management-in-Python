from src.domain.movie import Movie
from src.domain.client import Client
from src.domain.rental import Rental
from src.repository.repository_exception import RepositoryException
from src.services.undo_redo_service import Call, Operation, CascadeOperation
import datetime
import random


class RentalService:

    def __init__(self, rental_repository, movie_repository, client_repository, undo_redo_service):
        self.__rental_repo = rental_repository
        self.__movie_repo = movie_repository
        self.__client_repo = client_repository
        self.__undo_redo_serv = undo_redo_service

    def generate_rentals(self):
        """
        function that generates rentals
        :return:
        """
        list_movie_id = ['13', '49', '32', '48', '90', '34', '9', '18', '15', '22', '5', '2', '76', '35', '60', '38',
                         '4', '87', '7', '8']
        list_client_id = ['13', '49', '32', '48', '90', '34', '9', '18', '15', '22', '5', '2', '76', '35', '60', '38',
                          '4', '87', '7', '8']
        list_dates = [['2021-12-01', '2022-01-01', '2021-12-29'], ['2021-11-01', '2021-12-01', '2021-11-20'],
                     ['2021-01-01', '2021-02-01', '2021-03-01'], ['2021-09-23', '2021-10-01', 'not returned yet'],
                     ['2021-12-29', '2022-01-01', 'not returned yet'], ['2021-05-01', '2021-05-13', '2021-05-10'],
                     ['2021-06-01', '2021-07-13', '2021-07-20'], ['2021-08-29', '2021-10-01', 'not returned yet'],
                     ['2021-04-01', '2021-04-27', '2021-04-20'], ['2021-11-28', '2021-11-29', 'not returned yet']]
        for i in range(0, 10):
            rental_id = str(i+1)
            movie_id = random.choice(list_movie_id)
            list_movie_id.remove(movie_id)
            client_id = random.choice(list_client_id)
            list_client_id.remove(client_id)
            dates = random.choice(list_dates)
            list_dates.remove(dates)
            rented_date = dates[0]
            due_date = dates[1]
            returned_date = 'not returned yet'
            rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
            self.__rental_repo.rent_movie(rental)
            returned_date = dates[2]
            rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
            if returned_date != 'not returned yet':
                self.__rental_repo.return_movie(rental)

    def movie_rentals(self, movie_id):
        """
        function that gets all rentals with that movie_id
        :param movie_id:
        :return: the list of rentals
        """
        return self.__rental_repo.movie_rentals(movie_id)

    def client_rentals(self, client_id):
        """
        function that gets all rentals with that client_id
        :param client_id:
        :return: the list of rentals
        """
        return self.__rental_repo.client_rentals(client_id)

    def rent_movie(self, rental):
        """
        function that rents a movie
        :param rental:
        :return: the updated list of rentals
        """
        self.__rental_repo.rent_movie(rental)
        undo_call = Call(self.__rental_repo.remove_rental, rental.rental_id)
        redo_call = Call(self.__rental_repo.rent_movie, rental)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def return_movie(self, rental):
        """
        function that returns a movie
        :param rental:
        :return:
        """
        self.__rental_repo.return_movie(rental)
        undo_call = Call(self.__rental_repo.reverse_rental, rental.rental_id)
        redo_call = Call(self.__rental_repo.return_movie, rental)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def list_rental(self):
        """
        function that lists rentals
        :return: the list of rentals
        """
        return self.__rental_repo.list_rental()

    def remove_rental(self, rental_id):
        """
        function that removes rental
        :param rental_id:
        :return:
        """
        self.__rental_repo.remove_rental(rental_id)

    def reverse_return(self, rental_id):
        """
        function that reverses rental
        :param rental_id:
        :return:
        """
        self.__rental_repo.reverse_return(rental_id)

    def most_rented_movies(self):
        """
        function that provides the list of movies, sorted in descending order of the number of days they were rented
        :return: the sorted list of movies
        """
        data = dict()
        movies = self.__movie_repo.list_movie()
        for m in movies:
            data[m.movie_id] = 0
        rentals = self.__rental_repo.list_rental()
        for r in rentals:
            nr = self.__rental_repo.rented_days(r.rental_id)
            data[r.movie_id] += nr.days
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        sort = []
        for key in data:
            sort.append(self.__movie_repo.search_movie_id(key[0]))
        return sort

    def most_active_clients(self):
        """
        function that provides the list of clients, sorted in descending order of the number of movie rental days they have
        :return: the sorted list of clients
        """
        data = dict()
        clients = self.__client_repo.list_client()
        for c in clients:
            data[c.client_id] = 0
        rentals = self.__rental_repo.list_rental()
        for r in rentals:
            nr = self.__rental_repo.rented_days(r.rental_id)
            data[r.client_id] += nr.days
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        sort = []
        for key in data:
            sort.append(self.__client_repo.search_client_id(key[0]))
        return sort

    def delayed_days(self):
        """
        function that gets all the movies that are currently rented, for which the due date for return has passed,
        sorted in descending order of the number of days of delay
        :return: the sorted list of rentals
        """
        data = dict()
        rentals = self.__rental_repo.list_rental()
        for r in rentals:
            nr = self.__rental_repo.late_rental(r.rental_id)
            if nr != 0:
                data[r.rental_id] = nr
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        sort = []
        for key in data:
            sort.append(self.__rental_repo.existent_rental_id(key[0]))
        return sort

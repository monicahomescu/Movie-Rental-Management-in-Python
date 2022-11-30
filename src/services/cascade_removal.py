from src.services.undo_redo_service import Call, Operation, CascadeOperation
from src.domain.movie import Movie
from src.domain.client import Client
import datetime


class RemoveControl:

    def __init__(self, movie_service, client_service, rental_service, undo_redo_service, movie_repository,
                 client_repository, rental_repository):
        self.__movie_serv = movie_service
        self.__client_serv = client_service
        self.__rental_serv = rental_service
        self.__undo_redo_serv = undo_redo_service
        self.__movie_repo = movie_repository
        self.__client_repo = client_repository
        self.__rental_repo = rental_repository

    def remove_movie(self, movie_id):
        """
        function that removes movie and its rentals
        :param movie_id:
        :return:
        """
        movie = self.__movie_serv.search_movie_id(movie_id)
        undo_call = Call(self.__movie_repo.add_movie, movie)
        redo_call = Call(self.__movie_repo.remove_movie, movie_id)
        op = CascadeOperation()
        op.add(Operation(undo_call, redo_call))
        self.__movie_serv.remove_movie(movie_id)
        movie_rentals = self.__rental_serv.movie_rentals(movie_id)
        for r in movie_rentals:
            undo_call = Call(self.__rental_repo.rent_movie, r)
            redo_call = Call(self.__rental_serv.remove_rental, r.rental_id)
            op.add(Operation(undo_call, redo_call))
            self.__rental_serv.remove_rental(r.rental_id)
        self.__undo_redo_serv.record(op)

    def remove_client(self, client_id):
        """
        function that removes client and its rentals
        :param client_id:
        :return:
        """
        client = self.__client_serv.search_client_id(client_id)
        undo_call = Call(self.__client_repo.add_client, client)
        redo_call = Call(self.__client_repo.remove_client, client_id)
        op = CascadeOperation()
        op.add(Operation(undo_call, redo_call))
        self.__client_serv.remove_client(client_id)
        client_rentals = self.__rental_serv.client_rentals(client_id)
        for r in client_rentals:
            undo_call = Call(self.__rental_repo.rent_movie, r)
            redo_call = Call(self.__rental_repo.remove_rental, r.rental_id)
            op.add(Operation(undo_call, redo_call))
            self.__rental_serv.remove_rental(r.rental_id)
        self.__undo_redo_serv.record(op)

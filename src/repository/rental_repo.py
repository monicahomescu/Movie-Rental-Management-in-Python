from src.repository.repository_exception import RepositoryException
from datetime import datetime
from src.domain.rental import Rental
import pickle
from src.domain.struct import Iterable, sort_data, filter_data


class RentalRepo:

    def __init__(self, movie_repository, client_repository):
        self._rental_data = Iterable()
        self.__movie_repo = movie_repository
        self.__client_repo = client_repository

    def movie_rentals(self, movie_id):
        """
        function that gets all rentals with that movie_id
        :param movie_id:
        :return: the list of found rentals
        """
        data = []
        for x in self._rental_data:
            if x.movie_id == movie_id:
                data.append(x)
        return data

    def client_rentals(self, client_id):
        """
        function that gets all rentals with that client_id
        :param client_id:
        :return: the list of found rentals
        """
        data = []
        for x in self._rental_data:
            if x.client_id == client_id:
                data.append(x)
        return data

    def rent_movie(self, rental):
        """
        function that rents a movie
        :param rental:
        :return:
        """
        for x in self._rental_data:
            if x.rental_id == rental.rental_id:
                raise RepositoryException("The rental id already exists!")
        if self.__movie_repo.existent_movie_id(rental.movie_id) == False:
            raise RepositoryException("The movie_id doesn't exist!")
        if self.__client_repo.existent_client_id(rental.client_id) == False:
            raise RepositoryException("The client_id doesn't exist!")
        movie_rentals = self.movie_rentals(rental.movie_id)
        client_rentals = self.client_rentals(rental.client_id)
        for x in movie_rentals:
            if x.returned_date == 'not returned yet':
                raise RepositoryException("Movie is not available to be rented!")
        today_date = str(datetime.today().strftime('%Y-%m-%d'))
        today_date = datetime.strptime(today_date, '%Y-%m-%d')
        for x in client_rentals:
            due_date = x.due_date
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
            if x.returned_date == 'not returned yet':
                if today_date > due_date:
                    raise RepositoryException("Client has rentals that have passed the due date!")
            else:
                returned_date = x.returned_date
                returned_date = datetime.strptime(returned_date, '%Y-%m-%d')
                if returned_date > due_date:
                    raise RepositoryException("Client has rentals that have passed the due date!")
        self._rental_data.append(rental)

    def return_movie(self, rental):
        """
        function that returns a movie
        :param rental:
        :return:
        """
        for x in self._rental_data:
            if x.rental_id == rental.rental_id:
                if x.returned_date != 'not returned yet':
                    raise RepositoryException("The rental was already returned!")
                x.returned_date = rental.returned_date
                return
        raise RepositoryException("The rental id doesn't exist!")

    @staticmethod
    def compare_func(a, b):
        """
        function to compare
        :param a:
        :param b:
        :return: True or False
        """
        return int(a.rental_id) <= int(b.rental_id)

    def list_rental(self):
        """
        function that lists the rentals
        :return: the list of rentals
        """
        if len(self._rental_data) == 0:
            raise RepositoryException("There are no rentals!")
        else:
            #return self._rental_data
            sort_data(self._rental_data, self.compare_func)
            return self._rental_data

    def existent_rental_id(self, rental_id):
        """
        function that returns rental with that rental_id
        :param rental_id:
        :return: the rental
        """
        for x in self._rental_data:
            if x.rental_id == rental_id:
                return x
        raise RepositoryException("Rental id does not exist!")

    def remove_rental(self, rental_id):
        """
        function that removes rental
        :param rental_id:
        :return:
        """
        rental = self.existent_rental_id(rental_id)
        self._rental_data.remove(rental)

    def reverse_rental(self, rental_id):
        """
        function that reverses rental
        :param rental_id:
        :return:
        """
        for x in self._rental_data:
            if x.rental_id == rental_id:
                x.returned_date = 'not returned yet'

    def rented_days(self, rental_id):
        """
        function that gets the number of rented days
        :param rental_id:
        :return: the number
        """
        x = self.existent_rental_id(rental_id)
        rented_date = x.rented_date
        rented_date = datetime.strptime(rented_date, '%Y-%m-%d')
        nr = 0
        if x.returned_date == 'not returned yet':
            today_date = str(datetime.today().strftime('%Y-%m-%d'))
            today_date = datetime.strptime(today_date, '%Y-%m-%d')
            if today_date > rented_date:
                nr = today_date - rented_date
            else:
                nr = rented_date - today_date
        else:
            returned_date = x.returned_date
            returned_date = datetime.strptime(returned_date, '%Y-%m-%d')
            if returned_date > rented_date:
                nr = returned_date - rented_date
            else:
                nr = rented_date - returned_date
        return nr

    def late_rental(self, rental_id):
        """
        function that gets number of delayed days
        :param rental_id:
        :return: the number
        """
        x = self.existent_rental_id(rental_id)
        due_date = x.due_date
        due_date = datetime.strptime(due_date, '%Y-%m-%d')
        nr = 0
        if x.returned_date == 'not returned yet':
            today_date = str(datetime.today().strftime('%Y-%m-%d'))
            today_date = datetime.strptime(today_date, '%Y-%m-%d')
            if today_date > due_date:
                nr = today_date - due_date
        else:
            returned_date = x.returned_date
            returned_date = datetime.strptime(returned_date, '%Y-%m-%d')
            if returned_date > due_date:
                nr = returned_date - due_date
        return nr


class TextRentalRepo(RentalRepo):

    def __init__(self, movie_repository, client_repository, file_name):
        super().__init__(movie_repository, client_repository)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            rental_id, movie_id, client_id, rented_date, due_date, returned_date = line.split(maxsplit=5, sep=';')
            self.rent_movie(Rental(int(rental_id), int(movie_id), int(client_id), rented_date.rstrip(), 
                                   due_date.rstrip(), returned_date.rstrip()))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")
        for rental in self._rental_data:
            f.write(str(rental.rental_id) + ";" + str(rental.movie_id) + ";" + str(rental.client_id) + ";" +
                    rental.rented_date + ";" + rental.due_date + ";" + rental.returned_date + "\n")
        f.close()

    def movie_rentals(self, movie_id):
        return super(TextRentalRepo, self).movie_rentals(movie_id)

    def client_rentals(self, client_id):
        return super(TextRentalRepo, self).client_rentals(client_id)

    def rent_movie(self, rental):
        super(TextRentalRepo, self).rent_movie(rental)
        self._save_file()

    def return_movie(self, rental):
        super(TextRentalRepo, self).return_movie(rental)
        self._save_file()

    def list_rental(self):
        return super(TextRentalRepo, self).list_rental()

    def existent_rental_id(self, rental_id):
        return super(TextRentalRepo, self).existent_rental_id(rental_id)

    def remove_rental(self, rental_id):
        super(TextRentalRepo, self).remove_rental(rental_id)
        self._save_file()

    def reverse_rental(self, rental_id):
        super(TextRentalRepo, self).reverse_rental(rental_id)
        self._save_file()

    def rented_days(self, rental_id):
        return super(TextRentalRepo, self).rented_days(rental_id)

    def late_rental(self, rental_id):
        return super(TextRentalRepo, self).late_rental(rental_id)


class BinRentalRepo(RentalRepo):

    def __init__(self, movie_repository, client_repository, file_name):
        super().__init__(movie_repository, client_repository)
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        try:
            self._rental_data = pickle.load(f)
        except EOFError:
            pass

    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._rental_data, f)
        f.close()

    def movie_rentals(self, movie_id):
        return super(BinRentalRepo, self).movie_rentals(movie_id)

    def client_rentals(self, client_id):
        return super(BinRentalRepo, self).client_rentals(client_id)

    def rent_movie(self, rental):
        super(BinRentalRepo, self).rent_movie(rental)
        self._save_file()

    def return_movie(self, rental):
        super(BinRentalRepo, self).return_movie(rental)
        self._save_file()

    def list_rental(self):
        return super(BinRentalRepo, self).list_rental()

    def existent_rental_id(self, rental_id):
        return super(BinRentalRepo, self).existent_rental_id(rental_id)

    def remove_rental(self, rental_id):
        super(BinRentalRepo, self).remove_rental(rental_id)
        self._save_file()

    def reverse_rental(self, rental_id):
        super(BinRentalRepo, self).reverse_rental(rental_id)
        self._save_file()

    def rented_days(self, rental_id):
        return super(BinRentalRepo, self).rented_days(rental_id)

    def late_rental(self, rental_id):
        return super(BinRentalRepo, self).late_rental(rental_id)

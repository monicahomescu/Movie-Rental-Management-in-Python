import unittest
from src.domain.movie import Movie
import movie_repo
from src.domain.client import Client
import client_repo
from src.domain.rental import Rental
import rental_repo


class Test(unittest.TestCase):

    def setUp(self) -> None:
        self.movie_repo = movie_repo.MovieRepo()
        self.client_repo = client_repo.ClientRepo()
        self.rental_repo = rental_repo.RentalRepo(self.movie_repo, self.client_repo)

    def test_add_movie(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.assertEqual(self.movie_repo.list_movie()[0], movie)
        try:
            movie = Movie(1, "Title", "Description", "Genre")
            self.movie_repo.add_movie(movie)
        except Exception as ex:
            self.assertEqual(str(ex), "The movie id already exists!")

    def test_add_client(self):
        client = Client(1, "Bob")
        self.client_repo.add_client(client)
        self.assertEqual(self.client_repo.list_client()[0], client)
        try:
            client = Client(1, "Bob")
            self.client_repo.add_client(client)
        except Exception as ex:
            self.assertEqual(str(ex), "The client id already exists!")

    def test_remove_movie(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.movie_repo.remove_movie(1)
        try:
            self.movie_repo.remove_movie(1)
        except Exception as ex:
            self.assertEqual(str(ex), "The movie id doesn't exist!")

    def test_remove_client(self):
        client = Client(1, "Bob")
        self.client_repo.add_client(client)
        self.client_repo.remove_client(1)
        try:
            self.client_repo.remove_client(1)
        except Exception as ex:
            self.assertEqual(str(ex), "The client id doesn't exist!")

    def test_update_movie(self):
        movie = Movie(1, "Title", "Description", "Genre")
        update = Movie(1, "Film", "Summary", "Type")
        self.movie_repo.add_movie(movie)
        self.movie_repo.update_movie(update)
        self.assertEqual(self.movie_repo.list_movie()[0].movie_id, 1)
        self.assertEqual(self.movie_repo.list_movie()[0].title, "Film")
        self.assertEqual(self.movie_repo.list_movie()[0].description, "Summary")
        self.assertEqual(self.movie_repo.list_movie()[0].genre, "Type")
        try:
            self.movie_repo.update_movie(update)
        except Exception as ex:
            self.assertEqual(str(ex), "The movie id doesn't exist!")

    def test_update_client(self):
        client = Client(1, "Bob")
        update = Client(1, "Jack")
        self.client_repo.add_client(client)
        self.client_repo.update_client(update)
        self.assertEqual(self.client_repo.list_client()[0].client_id, 1)
        self.assertEqual(self.client_repo.list_client()[0].name, "Jack")
        try:
            self.client_repo.update_client(update)
        except Exception as ex:
            self.assertEqual(str(ex), "The client id doesn't exist!")

    def test_list_movie(self):
        try:
            data = self.movie_repo.list_movie()
        except Exception as ex:
            self.assertEqual(str(ex), "There are no movies!")
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        data = self.movie_repo.list_movie()
        self.assertEqual(len(data), 1)
        self.assertEqual(self.movie_repo.list_movie()[0], movie)

    def test_list_client(self):
        try:
            data = self.client_repo.list_client()
        except Exception as ex:
            self.assertEqual(str(ex), "There are no clients!")
        client = Client(1, "Bob")
        self.client_repo.add_client(client)
        data = self.client_repo.list_client()
        self.assertEqual(len(data), 1)
        self.assertEqual(self.client_repo.list_client()[0], client)

    def test_rent_movie(self):
        rental = Rental(1, 2, 3, '01/10/2021', '01/11/2021', 'not returned yet')
        self.rental_repo.rent_movie(rental)
        self.assertEqual(self.rental_repo.list_rental()[0], rental)
        try:
            rental = Rental(1, 2, 3, '01/10/2021', '01/11/2021', 'not returned yet')
            self.rental_repo.rent_movie(rental)
        except Exception as ex:
            self.assertEqual(str(ex), "The rental id already exists!")

    def test_return_movie(self):
        rental = Rental(1, 2, 3, '01/10/2021', '01/11/2021', 'not returned yet')
        self.rental_repo.rent_movie(rental)
        rental = Rental(1, 'x', 'x', 'x', 'x', '01/12/2021')
        self.rental_repo.return_movie(rental)
        self.assertEqual(self.rental_repo.list_rental()[0].returned_date, '01/12/2021')
        try:
            rental = Rental(2, 'x', 'x', 'x', 'x', '01/12/2021')
            self.rental_repo.return_movie(rental)
        except Exception as ex:
            self.assertEqual(str(ex), "The rental id doesn't exist!")

    def test_list_rental(self):
        try:
            data = self.rental_repo.list_rental()
        except Exception as ex:
            self.assertEqual(str(ex), "There are no rentals!")
        rental = Rental(1, 2, 3, '01/10/2021', '01/11/2021', 'not returned yet')
        self.rental_repo.rent_movie(rental)
        data = self.rental_repo.list_rental()
        self.assertEqual(len(data), 1)
        self.assertEqual(self.rental_repo.list_rental()[0], rental)

    def test_search_movie_id(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.assertEqual(self.movie_repo.search_movie_id(1), movie)
        try:
            data = self.movie_repo.search_movie_id(2)
        except Exception as ex:
            self.assertEqual(str(ex), "The movie id doesn't exist!")

    def test_search_title(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.assertEqual(self.movie_repo.search_title('titl')[0], movie)
        self.assertEqual(len(self.movie_repo.search_title('titl')), 1)
        try:
            data = self.movie_repo.search_title('abc')
        except Exception as ex:
            self.assertEqual(str(ex), "There is no match for a title!")

    def test_search_description(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.assertEqual(self.movie_repo.search_description('SCRIP')[0], movie)
        self.assertEqual(len(self.movie_repo.search_description('SCRIP')), 1)
        try:
            data = self.movie_repo.search_description('abc')
        except Exception as ex:
            self.assertEqual(str(ex), "There is no match for a description!")

    def test_search_genre(self):
        movie = Movie(1, "Title", "Description", "Genre")
        self.movie_repo.add_movie(movie)
        self.assertEqual(self.movie_repo.search_genre('Genr')[0], movie)
        self.assertEqual(len(self.movie_repo.search_genre('Genr')), 1)
        try:
            data = self.movie_repo.search_genre('abc')
        except Exception as ex:
            self.assertEqual(str(ex), "There is no match for a genre!")

    def test_search_client_id(self):
        client = Client(1, "Bob")
        self.client_repo.add_client(client)
        self.assertEqual(self.client_repo.search_client_id(1), client)
        try:
            data = self.client_repo.search_client_id(2)
        except Exception as ex:
            self.assertEqual(str(ex), "The client id doesn't exist!")

    def test_search_name(self):
        client = Client(1, "Bob")
        self.client_repo.add_client(client)
        self.assertEqual(self.client_repo.search_name('bO')[0], client)
        self.assertEqual(len(self.client_repo.search_name('bO')), 1)
        try:
            data = self.client_repo.search_name('abc')
        except Exception as ex:
            self.assertEqual(str(ex), "There is no match for a name!")


if __name__ == "__main__":
    unittest.main()

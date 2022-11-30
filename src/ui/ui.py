from src.domain.movie import Movie
from src.domain.client import Client
from src.domain.rental import Rental
from src.repository.movie_repo import MovieRepo, TextMovieRepo, BinMovieRepo
from src.repository.client_repo import ClientRepo, TextClientRepo, BinClientRepo
from src.repository.rental_repo import RentalRepo, TextRentalRepo, BinRentalRepo
from src.services.movie_service import MovieService
from src.services.client_service import ClientService
from src.services.rental_service import RentalService
from src.services.undo_redo_service import UndoRedoService
from src.services.cascade_removal import RemoveControl


class Ui:

    def __init__(self, movie_service, client_service, rental_service, undo_redo_service, remove_control):
        self.__movie_serv = movie_service
        self.__client_serv = client_service
        self.__rental_serv = rental_service
        self.__undo_redo_serv = undo_redo_service
        self.__remove_ctrl = remove_control

    def print_menu(self):
        """
        function that prints the menu
        :return:
        """
        print("-----------------------------------")
        print("exit - end program")
        print("1 - add movie")
        print("2 - add client")
        print("3 - remove movie")
        print("4 - remove client")
        print("5 - update movie")
        print("6 - update client")
        print("7 - list movies")
        print("8 - list clients")
        print("9 - rent movie")
        print("10 - return movie")
        print("11 - list rentals")
        print("12 - search movie by movie_id")
        print("13 - search movie by title")
        print("14 - search movie by description")
        print("15 - search movie by genre")
        print("16 - search client by client_id")
        print("17 - search client by name")
        print("18 - most rented movies")
        print("19 - most active clients")
        print("20 - late rentals")
        print("21 - undo")
        print("22 - redo")
        print("-----------------------------------")

    def add_movie_info(self):
        """
        function that adds a movie
        :return:
        """
        movie_id = input("movie_id = ")
        title = input("title = ")
        description = input("description = ")
        genre = input("genre = ")
        movie = Movie(movie_id, title, description, genre)
        try:
            self.__movie_serv.add_movie(movie)
        except Exception as ex:
            print(ex)

    def add_client_info(self):
        """
        function that adds a client
        :return:
        """
        client_id = input("client_id = ")
        name = input("name = ")
        client = Client(client_id, name)
        try:
            self.__client_serv.add_client(client)
        except Exception as ex:
            print(ex)

    def remove_movie_info(self):
        """
        function that removes a movie
        :return:
        """
        movie_id = input("movie_id = ")
        try:
            self.__remove_ctrl.remove_movie(movie_id)
        except Exception as ex:
            print(ex)

    def remove_client_info(self):
        """
        function that removes a client
        :return:
        """
        client_id = input("client_id = ")
        try:
            self.__remove_ctrl.remove_client(client_id)
        except Exception as ex:
            print(ex)

    def update_movie_info(self):
        """
        function that updates a movie
        :return:
        """
        movie_id = input("movie_id = ")
        title = input("title = ")
        description = input("description = ")
        genre = input("genre = ")
        movie = Movie(movie_id, title, description, genre)
        try:
            self.__movie_serv.update_movie(movie)
        except Exception as ex:
            print(ex)

    def update_client_info(self):
        """
        function that updates a client
        :return:
        """
        client_id = input("client_id = ")
        name = input("name = ")
        client = Client(client_id, name)
        try:
            self.__client_serv.update_client(client)
        except Exception as ex:
            print(ex)

    def list_movie_info(self):
        """
        function that lists movies
        :return:
        """
        try:
            movie = self.__movie_serv.list_movie()
            for x in movie:
                print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " +
                      str(x.description) + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def list_client_info(self):
        """
        function that lists clients
        :return:
        """
        try:
            client = self.__client_serv.list_client()
            for x in client:
                print("Client_id: " + str(x.client_id) + ", Name: " + str(x.name))
        except Exception as ex:
            print(ex)

    def rent_movie_info(self):
        """
        function that rents a movie
        :return:
        """
        rental_id = input("rental_id = ")
        movie_id = input("movie_id = ")
        client_id = input("client_id = ")
        rented_date = input("rented_date = ")
        due_date = input("due_date = ")
        returned_date = 'not returned yet'
        rental = Rental(rental_id, movie_id, client_id, rented_date, due_date, returned_date)
        try:
            self.__rental_serv.rent_movie(rental)
        except Exception as ex:
            print(ex)

    def return_movie_info(self):
        """
        function that returns a movie
        :return:
        """
        rental_id = input("rental_id = ")
        returned_date = input("returned_date = ")
        rental = Rental(rental_id, "x", "x", "x", "x", returned_date)
        try:
            self.__rental_serv.return_movie(rental)
        except Exception as ex:
            print(ex)

    def list_rental_info(self):
        """
        function that lists rentals
        :return:
        """
        try:
            rental = self.__rental_serv.list_rental()
            for x in rental:
                print("Rental_id: " + str(x.rental_id) + ", Movie_id: " + str(x.movie_id) + ", Client_id: " +
                      str(x.client_id) + ", Rented_date: " + str(x.rented_date) + ", Due_date: " + str(x.due_date) +
                      ", Returned_date: " + str(x.returned_date))
        except Exception as ex:
            print(ex)

    def search_movie_id_info(self):
        """
        function that searches for a movie by movie_id
        :return:
        """
        movie_id = input("movie_id = ")
        try:
            x = self.__movie_serv.search_movie_id(movie_id)
            print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " + str(x.description)
                  + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def search_title_info(self):
        """
        function that searches for a movie by title
        :return:
        """
        title = input("title = ")
        try:
            matching = self.__movie_serv.search_title(title)
            for x in matching:
                print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " +
                      str(x.description) + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def search_description_info(self):
        """
        function that searches for a movie by description
        :return:
        """
        description = input("description = ")
        try:
            matching = self.__movie_serv.search_description(description)
            for x in matching:
                print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " +
                      str(x.description) + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def search_genre_info(self):
        """
        function that searches for a movie by genre
        :return:
        """
        genre = input("genre = ")
        try:
            matching = self.__movie_serv.search_genre(genre)
            for x in matching:
                print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " +
                      str(x.description) + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def search_client_id_info(self):
        """
        function that searches for a client by client_id
        :return:
        """
        client_id = input("client_id = ")
        try:
            x = self.__client_serv.search_client_id(client_id)
            print("Client_id: " + str(x.client_id) + ", Name: " + str(x.name))
        except Exception as ex:
            print(ex)

    def search_name_info(self):
        """
        function that searches for a client by name
        :return:
        """
        name = input("name = ")
        try:
            matching = self.__client_serv.search_name(name)
            for x in matching:
                print("Client_id: " + str(x.client_id) + ", Name: " + str(x.name))
        except Exception as ex:
            print(ex)

    def most_rented_movies_info(self):
        """
        function that provides the list of movies, sorted in descending order of the number of days they were rented
        :return:
        """
        try:
            data = self.__rental_serv.most_rented_movies()
            for x in data:
                print("Movie_id: " + str(x.movie_id) + ", Title: " + str(x.title) + ", Description: " +
                      str(x.description) + ", Genre: " + str(x.genre))
        except Exception as ex:
            print(ex)

    def most_active_clients_info(self):
        """
        function that provides the list of clients, sorted in descending order of the number of movie rental days they have
        :return:
        """
        try:
            data = self.__rental_serv.most_active_clients()
            for x in data:
                print("Client_id: " + str(x.client_id) + ", Name: " + str(x.name))
        except Exception as ex:
            print(ex)

    def delayed_days_info(self):
        """
        function that gets all the movies that are currently rented, for which the due date for return has passed,
        sorted in descending order of the number of days of delay
        :return: the sorted list of rentals
        :return:
        """
        try:
            data = self.__rental_serv.delayed_days()
            if len(data) == 0:
                print("There are no late rentals!")
            else:
                for x in data:
                    print("Rental_id: " + str(x.rental_id) + ", Movie_id: " + str(x.movie_id) + ", Client_id: " +
                          str(x.client_id) + ", Rented_date: " + str(x.rented_date) + ", Due_date: " + str(x.due_date) +
                          ", Returned_date: " + str(x.returned_date))
        except Exception as ex:
            print(ex)

    def undo_info(self):
        """
        function that undoes
        :return:
        """
        try:
            self.__undo_redo_serv.undo()
        except Exception as ex:
            print(ex)

    def redo_info(self):
        """
        function that redoes
        :return:
        """
        try:
            self.__undo_redo_serv.redo()
        except Exception as ex:
            print(ex)

    def start(self):
        """
        function that starts the program
        :return:
        """
        self.print_menu()
        self.__movie_serv.generate_movies()
        self.__client_serv.generate_clients()
        self.__rental_serv.generate_rentals()
        while True:
            x = input(">>>")
            if x == 'exit':
                return
            elif x == '1':
                self.add_movie_info()
            elif x == '2':
                self.add_client_info()
            elif x == '3':
                self.remove_movie_info()
            elif x == '4':
                self.remove_client_info()
            elif x == '5':
                self.update_movie_info()
            elif x == '6':
                self.update_client_info()
            elif x == '7':
                self.list_movie_info()
            elif x == '8':
                self.list_client_info()
            elif x == '9':
                self.rent_movie_info()
            elif x == '10':
                self.return_movie_info()
            elif x == '11':
                self.list_rental_info()
            elif x == '12':
                self.search_movie_id_info()
            elif x == '13':
                self.search_title_info()
            elif x == '14':
                self.search_description_info()
            elif x == '15':
                self.search_genre_info()
            elif x == '16':
                self.search_client_id_info()
            elif x == '17':
                self.search_name_info()
            elif x == '18':
                self.most_rented_movies_info()
            elif x == '19':
                self.most_active_clients_info()
            elif x == '20':
                self.delayed_days_info()
            elif x == '21':
                self.undo_info()
            elif x == '22':
                self.redo_info()


f = open("settings.properties")
info = []
for line in f.readlines():
    line = line.split()
    info.append(line[2])
f.close()
repo = info[0]
movies = info[1][1:-1]
clients = info[2][1:-1]
rentals = info[3][1:-1]
if repo == 'inmemory':
    movie_repo = MovieRepo()
    client_repo = ClientRepo()
    rental_repo = RentalRepo(movie_repo, client_repo)
elif repo == 'textfiles':
    movie_repo = TextMovieRepo(movies)
    client_repo = TextClientRepo(clients)
    rental_repo = TextRentalRepo(movie_repo, client_repo, rentals)
else:
    movie_repo = BinMovieRepo(movies)
    client_repo = BinClientRepo(clients)
    rental_repo = BinRentalRepo(movie_repo, client_repo, rentals)

undo_redo_serv = UndoRedoService()
movie_serv = MovieService(movie_repo, undo_redo_serv)
client_serv = ClientService(client_repo, undo_redo_serv)
rental_serv = RentalService(rental_repo, movie_repo, client_repo, undo_redo_serv)

remove_control = RemoveControl(movie_serv, client_serv, rental_serv, undo_redo_serv, movie_repo, client_repo,
                               rental_repo)

ui = Ui(movie_serv, client_serv, rental_serv, undo_redo_serv, remove_control)
ui.start()

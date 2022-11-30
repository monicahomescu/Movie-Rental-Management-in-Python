from src.domain.client import Client
from src.repository.repository_exception import RepositoryException
from src.services.undo_redo_service import Call, Operation, CascadeOperation
import random


class ClientService:

    def __init__(self, client_repository, undo_redo_service):
        self.__client_repo = client_repository
        self.__undo_redo_serv = undo_redo_service

    def generate_clients(self):
        """
        function that generates clients
        :return:
        """
        list_client_id = ['13', '49', '32', '48', '90', '34', '9', '18', '15', '22', '5', '2', '76', '35', '60', '38',
                          '4', '87', '7', '8']
        list_name = ["Bruce Banner", "Peter Parker", "May Parker", "Happy Hogan", "Tony Stark", "Pepper Pots",
                     "Stephen Strange", "Steve Rogers", "James Barnes", "Sam Wilson", "Natasha Romanoff",
                     "Yelena Belova", "Wanda Maximoff", "Clint Barton", "Carol Denvers", "Hank Pym", "James Rhodes",
                     "Shang Chi", "Maria Hill", "Phil Coulson"]
        for i in range(0, 20):
            client_id = random.choice(list_client_id)
            list_client_id.remove(client_id)
            name = random.choice(list_name)
            list_name.remove(name)
            client = Client(client_id, name)
            self.__client_repo.add_client(client)

    def add_client(self, client):
        """
        function that adds a client
        :param client:
        :return:
        """
        self.__client_repo.add_client(client)
        undo_call = Call(self.__client_repo.remove_client, client.client_id)
        redo_call = Call(self.__client_repo.add_client, client)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def remove_client(self, client_id):
        """
        function that removes a client
        :param client_id:
        :return:
        """
        self.__client_repo.remove_client(client_id)

    def update_client(self, client):
        """
        function that updates a client
        :param client:
        :return:
        """
        old = self.__client_repo.search_client_id(client.client_id)
        new = client
        self.__client_repo.update_client(client)
        undo_call = Call(self.__client_repo.update_client, old)
        redo_call = Call(self.__client_repo.update_client, new)
        op = Operation(undo_call, redo_call)
        self.__undo_redo_serv.record(op)

    def list_client(self):
        """
        function that lists the clients
        :return: the list of clients
        """
        return self.__client_repo.list_client()

    def search_client_id(self, client_id):
        """
        function that searches for a client by client_id
        :param client_id:
        :return: the client with that client_id
        """
        return self.__client_repo.search_client_id(client_id)

    def search_name(self, name):
        """
        function that searches for a client by name
        :param name:
        :return: the list of matches
        """
        return self.__client_repo.search_name(name)

from src.repository.repository_exception import RepositoryException
from src.domain.client import Client
import pickle
from src.domain.struct import Iterable, sort_data, filter_data


class ClientRepo:

    def __init__(self):
        self._client_data = Iterable()

    def add_client(self, client):
        """
        function that adds a client
        :param client:
        :return:
        """
        for x in self._client_data:
            if x.client_id == client.client_id:
                raise RepositoryException("The client id already exists!")
        self._client_data.append(client)

    def remove_client(self, client_id):
        """
        function that removes a client
        :param client_id:
        :return:
        """
        for x in self._client_data:
            if x.client_id == client_id:
                self._client_data.remove(x)
                return
        raise RepositoryException("The client id doesn't exist!")

    def update_client(self, client):
        """
        function that updates a client
        :param client:
        :return:
        """
        for x in self._client_data:
            if x.client_id == client.client_id:
                x.name = client.name
                return
        raise RepositoryException("The client id doesn't exist!")

    @staticmethod
    def compare_func(a, b):
        """
        function to compare
        :param a:
        :param b:
        :return: True or False
        """
        return int(a.client_id) <= int(b.client_id)

    def list_client(self):
        """
        function that lists the clients
        :return: the list of clients
        """
        if len(self._client_data) == 0:
            raise RepositoryException("There are no clients!")
        else:
            #return self._client_data
            sort_data(self._client_data, self.compare_func)
            return self._client_data

    def existent_client_id(self, client_id):
        """
        function that checks if the client_id exists
        :param client_id:
        :return: True or False
        """
        for x in self._client_data:
            if x.client_id == client_id:
                return True
        return False

    def search_client_id(self, client_id):
        """
        function that searches for a client by client_id
        :param client_id:
        :return: the client with that client_id
        """
        if self.existent_client_id(client_id) == False:
            raise RepositoryException("The client id doesn't exist!")
        else:
            #for x in self._client_data:
                #if x.client_id == client_id:
                    #return x
            found = filter_data(self._client_data, lambda x: x.client_id == client_id)
            return found[0]

    def search_name(self, name):
        """
        function that searches for a client by name
        :param name:
        :return: the list of matches
        """
        matching = []
        for x in self._client_data:
            #if x.name.lower() == name.lower() or name.lower() in x.name.lower():
                #matching.append(x)
            matching = filter_data(self._client_data, lambda x: x.name.lower() == name.lower() or name.lower() in x.name.lower())
        if len(matching) == 0:
            raise RepositoryException("There is no match for a name!")
        else:
            #return matching
            sort_data(matching, self.compare_func)
            return matching


class TextClientRepo(ClientRepo):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rt")
        for line in f.readlines():
            client_id, name = line.split(maxsplit=1, sep=';')
            self.add_client(Client(int(client_id), name.rstrip()))
        f.close()

    def _save_file(self):
        f = open(self._file_name, "wt")
        for client in self._client_data:
            f.write(str(client.client_id) + ";" + client.name + "\n")
        f.close()

    def add_client(self, client):
        super(TextClientRepo, self).add_client(client)
        self._save_file()

    def remove_client(self, client_id):
        super(TextClientRepo, self).remove_client(client_id)
        self._save_file()

    def update_client(self, client):
        super(TextClientRepo, self).update_client(client)
        self._save_file()

    def list_client(self):
        return super(TextClientRepo, self).list_client()

    def existent_client_id(self, client_id):
        return super(TextClientRepo, self).existent_client_id(client_id)

    def search_client_id(self, client_id):
        return super(TextClientRepo, self).search_client_id(client_id)

    def search_name(self, name):
        return super(TextClientRepo, self).search_name(name)


class BinClientRepo(ClientRepo):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load_file()

    def _load_file(self):
        f = open(self._file_name, "rb")
        try:
            self._client_data = pickle.load(f)
        except EOFError:
            pass

    def _save_file(self):
        f = open(self._file_name, "wb")
        pickle.dump(self._client_data, f)
        f.close()

    def add_client(self, client):
        super(BinClientRepo, self).add_client(client)
        self._save_file()

    def remove_client(self, client_id):
        super(BinClientRepo, self).remove_client(client_id)
        self._save_file()

    def update_client(self, client):
        super(BinClientRepo, self).update_client(client)
        self._save_file()

    def list_client(self):
        return super(BinClientRepo, self).list_client()

    def existent_client_id(self, client_id):
        return super(BinClientRepo, self).existent_client_id(client_id)

    def search_client_id(self, client_id):
        return super(BinClientRepo, self).search_client_id(client_id)

    def search_name(self, name):
        return super(BinClientRepo, self).search_name(name)

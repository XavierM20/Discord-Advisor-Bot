import os
import requests
from dotenv import load_dotenv
from modules.contexts.context import Context
from requests.exceptions import HTTPError, ConnectionError, MissingSchema
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.exceptions import URLUndefinedException, PreconditionException, ServiceUnavailableException, DirectoryNotFoundException
from modules.contexts.directory_entry import DirectoryEntry


class DirectoryContext(Context):
    def __init__(self, name: str, classifier: IntentClassifier):
        super().__init__(name, classifier)
        self.__entries: list = []
        self.__query: str = None

    @property
    def get_query(self):
        return self.__query

    @property
    def get_entries(self):
        return self.__entries

    def set_entries(self, entries):
        self.__entries = entries

    def set_query(self, query):
        self.__query = query.strip()


    def get_directory_info(self):
        base_url = os.getenv("DIRECTORY_SERVICE_URI")
        key = os.getenv("DIRECTORY_API_KEY")
        url = "{}apikey={}&serachCriteria={}".format(base_url, key, self.__query)
        entries = []

        try:
            if self.query is None:
                raise PreconditionException(self.query)

            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            if bool(data) is False or "Error" in data:
                raise DirectoryNotFoundException(self.query)

            for x in data:
                entries.append(DirectoryEntry(x))
            self.entries = entries

        except ConnectionError as ex:
            raise ServiceUnavailableException(ex)

        except MissingSchema as ex:
            raise URLUndefinedException(ex)

    def __str__(self):
        count = 0
        result = ""
        while count < len(self.entries):
            entry = self.entries[count]
            result += "{} {}\nTitle: {}\nEmail: {}\nDepartment: {}\nPhone: {}\nBuilding: {}\n".format(self.entries[count].firstname, self.entries[count].lastname, self.entries[count].title, self.entries[count].email, self.entries[count].department, self.entires[count].phone, self.entries[count].building)
            count += 1
        return result

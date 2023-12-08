import os
import requests
from dotenv import load_dotenv
from modules.contexts.context import Context
from requests.exceptions import HTTPError, ConnectionError, MissingSchema
from modules.classifiers.common.intentclassifier import IntentClassifier
from modules.exceptions import URLUndefinedException, CourseNotFoundException, PreconditionException, ServiceUnavailableException


class CourseContext(Context):
    def __init__(self, name: str, classifier: IntentClassifier):
        super().__init__(name, classifier)
        self.__subject: str = None
        self.__course: str = None
        self.__description: str = None
        self.__title: str = None
        self.__prerequisites: list = []

        # Getters and setters

    @property
    def subject(self) -> str:
        return self.__subject

    def subject(self, inp):
        self.__subject = inp

    @property
    def course(self) -> str:
        return self.__course

    def course(self, inp):
        self.__course = inp

    @property
    def description(self) -> str:
        return self.__description

    def description(self, inp):
        self.__description = inp

    @property
    def title(self) -> str:
        return self.__title

    def title(self, inp):
        self.__title = inp

    @property
    def prerequisites(self):
        return self.__prerequisites

    def prerequisites(self, inp):
        self.__prerequisites = inp

    def get_course_info(self) -> None:
        base_uri = os.getenv("COURSE_SERVICE_URI")
        term = 202280
        url = "{}subject={}&number={}&term={}".format(base_uri, self.subject, self.course, term)

        try:
            if self.course is None:
                raise PreconditionException(self.course)
            if self.subject is None:
                raise PreconditionException(self.subject)
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()

            self.__description = data["attribute"]["description"]
            self.__title = data["attribute"]["title"]
            self.__prerequisites = data["attribute"]["prerequisites"]

        except ConnectionError as ex:
            raise ServiceUnavailableException(ex)

        except HTTPError as ex:
            raise URLUndefinedException(ex)

        except MissingSchema as ex:
            raise ServiceUnavailableException(ex)

        except TypeError as ex:
            raise CourseNotFoundException(ex)


    def __str__(self):
        return f"{self.subject} {self.course}\n{self.title}\n{self.description}"


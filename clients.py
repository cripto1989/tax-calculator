import requests
from exceptions import (
    NotFoundException,
    FailedToCalculateTaxesException,
    ConnectionTimeoutException,
)
import urllib3
from abc import ABC, abstractmethod


class BaseHTTPClient(ABC):

    @abstractmethod
    def get_tax_brackets(self, year: int):
        raise NotImplementedError


class HTTPClient(BaseHTTPClient):
    def __init__(self, config):
        self._host = config["HOST"]

    def get_tax_brackets(self, year: int):
        try:
            response = self._get(f"tax-calculator/tax-year/{year}")
        except (
            requests.exceptions.RequestException,
            urllib3.exceptions.HTTPError,
        ) as request_exception:
            raise ConnectionTimeoutException(request_exception)

        if response.ok:
            return response.json()["tax_brackets"]

        self._handle_response_errors(response)

    def _get(self, *args, **kwargs):
        return self._make_request("get", *args, **kwargs)

    def _make_request(self, method, endpoint, **kwargs):
        url = f"{self._host}/{endpoint}"
        return requests.request(method, url, **kwargs)

    def _handle_response_errors(self, response):
        if response.status_code >= 500:
            raise FailedToCalculateTaxesException(response)

        if response.status_code == requests.codes.not_found:
            raise NotFoundException(response.url, response)

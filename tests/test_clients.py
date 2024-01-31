import pytest
import requests
from unittest.mock import MagicMock
from clients import HTTPClient
from exceptions import (
    NotFoundException,
    FailedToCalculateTaxesException,
    ConnectionTimeoutException,
)


TAX_BRACKETS_RESPONSE = {
    "tax_brackets": [
        {"max": 20000, "min": 0, "rate": 0.15},
        {"max": 40000, "min": 20000, "rate": 0.205},
        {"max": 60000, "min": 40000, "rate": 0.26},
        {"max": 80000, "min": 60000, "rate": 0.29},
        {"min": 80000, "rate": 0.33},
    ]
}

NOT_VALID_YEAR_RESPONSE = {
    "errors": [{"code": "NOT_FOUND", "field": "", "message": "That url was not found"}]
}


@pytest.fixture
def tax_calculator_mock_request(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("clients.requests.request", mock)
    return mock


class TestHTTPClient:
    client = HTTPClient({"HOST": "http://localhost:5000"})

    def test_tax_brackets(self, requests_mock):
        requests_mock.get(
            "http://localhost:5000/tax-calculator/tax-year/2019",
            json=TAX_BRACKETS_RESPONSE,
        )

        tax_brackets = self.client.get_tax_brackets(year=2019)

        assert requests_mock.call_count == 1
        assert requests_mock.request_history[0].method == "GET"
        assert tax_brackets == TAX_BRACKETS_RESPONSE["tax_brackets"]

    def test_not_found_error_raise_exception(self, requests_mock):
        requests_mock.get(
            "http://localhost:5000/tax-calculator/tax-year/2008",
            status_code=requests.codes.not_found,
        )

        with pytest.raises(NotFoundException):
            self.client.get_tax_brackets(year=2008)

    def test_failed_calculate_rate(self, tax_calculator_mock_request):
        response = MagicMock()
        response.ok = False
        response.status_code = 500
        tax_calculator_mock_request.return_value = response

        with pytest.raises(FailedToCalculateTaxesException):
            self.client.get_tax_brackets(year=2020)

    def test_connection_timeout_exception(self, tax_calculator_mock_request):

        tax_calculator_mock_request.side_effect = requests.exceptions.RequestException

        with pytest.raises(ConnectionTimeoutException):
            self.client.get_tax_brackets(year=2020)

import pytest
from taxes import IncomeCalculator
from clients import HTTPClient
from unittest.mock import MagicMock
from unittest import mock


@pytest.fixture
def tax_brackets():
    return MagicMock(
        return_value=[
            {"max": 47630, "min": 0, "rate": 0.15},
            {"max": 95259, "min": 47630, "rate": 0.205},
            {"max": 147667, "min": 95259, "rate": 0.26},
            {"max": 210371, "min": 147667, "rate": 0.29},
            {"min": 210371, "rate": 0.33},
        ]
    )


class TestIncomeCalculator:
    income_calculator = IncomeCalculator(
        client=HTTPClient(config={"HOST": ""}), year=2019
    )

    def test_first_rate(self, monkeypatch, tax_brackets):
        monkeypatch.setattr("clients.HTTPClient.get_tax_brackets", tax_brackets)

        result = self.income_calculator.get_calculation(salary=10000)

        assert result == {
            "details": [
                {
                    "marginal_tax_rate": 0.15,
                    "amount_taxable": 10000,
                    "tax_payable": 1500.0,
                },
                {"marginal_tax_rate": 0.205, "amount_taxable": 0, "tax_payable": 0.0},
                {"marginal_tax_rate": 0.26, "amount_taxable": 0, "tax_payable": 0.0},
                {"marginal_tax_rate": 0.29, "amount_taxable": 0, "tax_payable": 0.0},
                {"marginal_tax_rate": 0.33, "amount_taxable": 0, "tax_payable": 0.0},
            ],
            "total_taxes": 1500.0,
        }

    def test_middle_rate(self, monkeypatch, tax_brackets):
        monkeypatch.setattr("clients.HTTPClient.get_tax_brackets", tax_brackets)

        results = self.income_calculator.get_calculation(salary=200000)

        assert results == {
            "details": [
                {
                    "marginal_tax_rate": 0.15,
                    "amount_taxable": 47630,
                    "tax_payable": 7144.5,
                },
                {
                    "marginal_tax_rate": 0.205,
                    "amount_taxable": 47629,
                    "tax_payable": 9763.945,
                },
                {
                    "marginal_tax_rate": 0.26,
                    "amount_taxable": 52408,
                    "tax_payable": 13626.08,
                },
                {
                    "marginal_tax_rate": 0.29,
                    "amount_taxable": 52333,
                    "tax_payable": 15176.57,
                },
                {"marginal_tax_rate": 0.33, "amount_taxable": 0, "tax_payable": 0.0},
            ],
            "total_taxes": 45711.095,
        }

    def test_last_rate(self, monkeypatch, tax_brackets):
        monkeypatch.setattr("clients.HTTPClient.get_tax_brackets", tax_brackets)

        results = self.income_calculator.get_calculation(salary=220000)

        assert results == {
            "details": [
                {
                    "marginal_tax_rate": 0.15,
                    "amount_taxable": 47630,
                    "tax_payable": 7144.5,
                },
                {
                    "marginal_tax_rate": 0.205,
                    "amount_taxable": 47629,
                    "tax_payable": 9763.945,
                },
                {
                    "marginal_tax_rate": 0.26,
                    "amount_taxable": 52408,
                    "tax_payable": 13626.08,
                },
                {
                    "marginal_tax_rate": 0.29,
                    "amount_taxable": 62704,
                    "tax_payable": 18184.16,
                },
                {
                    "marginal_tax_rate": 0.33,
                    "amount_taxable": 9629,
                    "tax_payable": 3177.57,
                },
            ],
            "total_taxes": 51896.255,
        }

class TaxCalculatorException(Exception):
    def _format_str(self, message):
        return f"Tax Calculator - {message}"

    def __str__(self):
        return self._format_str("Tax Calculator")


class NotFoundException(TaxCalculatorException):
    def __init__(self, url, *args):
        super().__init__(*args)

        self.url = url

    def __str__(self):
        return self._format_str(f"Not found: {self.url}")


class FailedToCalculateTaxesException(TaxCalculatorException):
    def __str__(self):
        return self._format_str(f"Error getting rate")


class ConnectionTimeoutException(TaxCalculatorException):
    def __str__(self):
        return self._format_str(f"Connection timeout")

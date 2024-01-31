from clients import BaseHTTPClient


class IncomeCalculator:

    def __init__(self, client: BaseHTTPClient, year: int):
        self.client = client
        self.year = year        

    def get_calculation(self, salary: int):
        data = []

        for tax in self.client.get_tax_brackets(year=self.year):                                
            rate = tax["rate"]
            minimum = tax.get("min")
            maximum = tax.get("max", float("inf"))
            if minimum < salary < maximum:
                tax_payable = self._get_tax_payable(salary - minimum, rate)
                amount_taxable = salary - minimum
                               
            else:
                amount_taxable = maximum - minimum
                
                if minimum > salary:
                    amount_taxable = 0                

                tax_payable = self._get_tax_payable(amount_taxable, rate)
            
            self._append_values(data, rate, amount_taxable, tax_payable)             
        
        total_taxes = self._get_total_taxes(data)
        return {"details": data, "total_taxes": total_taxes}
    
    def _get_total_taxes(self, data):
        return sum(item["tax_payable"] for item in data)
    
    def _get_tax_payable(self, amount, rate):
        return amount * rate
    
    def _append_values(self, data, rate, amount_taxable, tax_payable):
        data.append(
                {
                    "marginal_tax_rate": rate,
                    "amount_taxable": amount_taxable,
                    "tax_payable": tax_payable,
                }
            )   

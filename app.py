from flask import Flask, request, jsonify
from taxes import IncomeCalculator
from clients import HTTPClient

client = HTTPClient({"HOST": "http://localhost:5000"})


app = Flask(__name__)


@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()

    if "salary" not in data or "year" not in data:
        return jsonify({"error": "salary and year are mandatory in the body"}), 400

    salary = data["salary"]
    year = data["year"]

    calculator = IncomeCalculator(client=client, year=year)
    response = calculator.get_calculation(salary=salary)

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)

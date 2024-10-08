from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Home route with input form
@app.route("/", methods=["GET", "POST"])
def index():
    # Default empty lists
    total_value = []
    end_number = []
    multiplicative_change = []
    chart_data = []
    ranks = []

    if request.method == "POST":
        init_dep = float(request.form["initial_deposit"])
        fractional_reserve_val = float(request.form["fractional_reserve"])

        # Validate fractional reserve value
        if fractional_reserve_val < 0 or fractional_reserve_val > 100:
            error = "Fractional Reserve value % must be between 0 and 100."
            return render_template("tst1.html", error=error)

        if fractional_reserve_val == 0:
            return render_template("tst1.html", result="Infinite money loop has been created.")

        # Calculate banking effect
        result, total_value, end_number, multiplicative_change, chart_data = calculate_banking_effect(init_dep, fractional_reserve_val)

        # Generate ranks
        ranks = list(range(1, end_number + 1)) if end_number > 0 else []

       # Debugging 

        print(f"Chart Data: {chart_data}")
        print(f"Ranks: {ranks}")

        if not isinstance(chart_data, list) or not isinstance(ranks, list):
            print("chart_data or ranks are not lists")
        else:
            print("chart_data and ranks are lists")

        print("Chart Data:", json.dumps(chart_data))  # Should print a valid JSON array
        print("Ranks:", json.dumps(ranks))  # Should print a valid JSON array

        # End-Debugging

        return render_template("tst1.html",
                               result=result,
                               total_value=total_value,
                               end_number=end_number,
                               multiplicative_change=multiplicative_change,
                               chart_data=chart_data,  # Pass Python list directly, no need for json.dumps()
                               ranks=ranks)  # Pass Python list directly, no need for json.dumps()

    return render_template("tst1.html", chart_data=json.dumps(chart_data), ranks=json.dumps(ranks))


# Function to calculate the detailed banking effect
def calculate_banking_effect(init_dep, fractional_reserve_val):
    output = []
    u = init_dep
    rank = 0
    sum_total = u
    chart_data = []  

    while u > 0.01:  
        u *= ((100 - fractional_reserve_val) / 100)  # Calculate new value
        rank += 1
        sum_total += u  
        mltpv = sum_total / init_dep  # Calculate multiplicative value

        # Collect data for chart
        chart_data.append(round(sum_total, 2))

        # Append to output list in reverse order
        output.insert(0, f"#{rank}︱ value: {round(u, 2)}︱ Total: {round(sum_total, 2)}︱ Multiplicative value: {round(mltpv, 4)}")

    # Prepare values for summary statistics
    total_value = round(sum_total, 2)
    end_number = rank
    multiplicative_change = mltpv

    return output, total_value, end_number, round(multiplicative_change, 4), chart_data


if __name__ == "__main__":
    app.run(debug=True)
